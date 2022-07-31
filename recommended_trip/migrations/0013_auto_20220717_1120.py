# Generated by Django 3.2 on 2022-07-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0012_auto_20220717_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singletrip',
            name='price_budget',
        ),
        migrations.AddField(
            model_name='singletrip',
            name='princing_type',
            field=models.CharField(choices=[('REASONABLE', 'REASONABLE'), ('MID-RANGE', 'MID-RANGE'), ('HIGH-END', 'HIGH-END')], default='REASONABLE', max_length=100),
        ),
    ]