# Generated by Django 3.2 on 2022-08-19 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0025_singletrip_max_number_of_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singletrip',
            name='max_number_of_days',
        ),
    ]
