# Generated by Django 3.2 on 2023-01-20 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0036_availabledates'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='valentine_offer',
            field=models.BooleanField(default=False),
        ),
    ]
