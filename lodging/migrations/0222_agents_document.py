# Generated by Django 3.2 on 2023-08-04 11:27

import core.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0221_auto_20230804_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='agents',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.agent_document_file, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
