# Generated by Django 3.2 on 2022-08-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0024_singletrip_countries_covered'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='max_number_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
