# Generated by Django 3.2 on 2022-11-16 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0030_alter_itinerarytransport_transport_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itinerarytransport',
            name='all_round_trip',
        ),
        migrations.RemoveField(
            model_name='itinerarytransport',
            name='driver_included_in_car',
        ),
    ]
