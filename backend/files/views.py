from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as django_filters
from django.db.models import Q
from datetime import datetime, timedelta
import hashlib
from django.core.files.base import ContentFile
from .models import File
from .serializers import FileSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.conf import settings
import os
from django.http import FileResponse
from rest_framework.decorators import action

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FileFilter(django_filters.FilterSet):
    size_range = django_filters.CharFilter(method='filter_size_range')
    file_type = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = File
        fields = ['file_type', 'size_range']

    def filter_size_range(self, queryset, name, value):
        try:
            min_size, max_size = map(int, value.split(','))
            return queryset.filter(size__gte=min_size, size__lte=max_size)
        except (ValueError, TypeError, AttributeError):
            return queryset

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('-uploaded_at')
    serializer_class = FileSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = FileFilter
    search_fields = ['original_filename']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            # Add case-insensitive search
            queryset = queryset.filter(
                Q(original_filename__icontains=search_query)
            )
        
        return queryset.select_related().prefetch_related()

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate file hash
        file_content = b''
        for chunk in file_obj.chunks():
            file_content += chunk
        
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check for existing file with same hash
        try:
            existing_file = File.objects.get(file_hash=file_hash)
            # Update reference count
            existing_file.reference_count += 1
            existing_file.save()
            
            return Response({
                'message': 'File already exists',
                'file': FileSerializer(existing_file).data,
                'storage_saved': len(file_content)
            }, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            # Create new file from the content
            new_file = ContentFile(file_content)
            new_file.name = file_obj.name
            
            data = {
                'file': new_file,
                'original_filename': file_obj.name,
                'file_type': file_obj.content_type,
                'size': len(file_content),
                'file_hash': file_hash,
                'reference_count': 1
            }
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Delete the actual file from storage
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        
        # Delete the database record
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file_obj = self.get_object()
        file_path = file_obj.file.path
        
        if os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=file_obj.original_filename
            )
            return response
        return Response(
            {'error': 'File not found'},
            status=status.HTTP_404_NOT_FOUND
        )