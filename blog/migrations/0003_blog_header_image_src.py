# Generated by Django 3.2 on 2022-10-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20221001_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='header_image_src',
            field=models.URLField(blank=True, null=True),
        ),
    ]
