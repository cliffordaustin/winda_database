# Generated by Django 3.2 on 2022-08-18 02:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0022_singletrip_flight'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='stop_at',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
    ]
