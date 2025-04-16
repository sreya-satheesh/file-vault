# Generated by Django 4.2.20 on 2025-04-14 08:53

from django.db import migrations, models
import files.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=files.models.file_upload_path)),
                ('original_filename', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=100)),
                ('size', models.BigIntegerField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_hash', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('reference_count', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
