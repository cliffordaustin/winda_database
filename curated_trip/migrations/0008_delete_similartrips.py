# Generated by Django 3.2 on 2022-10-25 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0007_alter_itineraryaccommodation_itinerary'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SimilarTrips',
        ),
    ]