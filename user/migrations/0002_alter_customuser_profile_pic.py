# Generated by Django 3.2 on 2022-04-02 14:31

import core.utils
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=core.utils.profile_image_thumbnail),
        ),
    ]
