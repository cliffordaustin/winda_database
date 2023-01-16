# Generated by Django 3.2 on 2023-01-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0031_auto_20221116_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='end_day',
            field=models.IntegerField(blank=True, help_text='Select the end day of this itinerary', null=True),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='start_day',
            field=models.IntegerField(blank=True, help_text='Select the start day of this itinerary', null=True),
        ),
    ]
