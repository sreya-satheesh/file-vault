from django.db import models
import uuid
import os
import hashlib

def file_upload_path(instance, filename):
    """Generate file path for new file upload"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_upload_path)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    reference_count = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        if not self.file_hash and self.file:
            self.file_hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def calculate_hash(self):
        """Calculate SHA-256 hash of the file content"""
        if not self.file:
            return None
        sha256_hash = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()