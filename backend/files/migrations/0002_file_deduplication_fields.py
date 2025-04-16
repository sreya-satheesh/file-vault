from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_hash',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='file',
            name='reference_count',
            field=models.IntegerField(default=1),
        ),
    ]