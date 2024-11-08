# Generated by Django 3.2 on 2022-10-22 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0005_alter_similartrips_curated_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='curatedtriplocations',
            name='nights',
            field=models.IntegerField(blank=True, help_text='How long will the trip be in this location?', null=True),
        ),
        migrations.AddField(
            model_name='itinerarytransport',
            name='all_round_trip',
            field=models.BooleanField(default=False, help_text='Is this an all round trip?'),
        ),
        migrations.AlterField(
            model_name='itinerarytransport',
            name='ending_location',
            field=models.CharField(blank=True, help_text='No need to add this if the transport is an all round trip', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itinerarytransport',
            name='starting_location',
            field=models.CharField(blank=True, help_text='No need to add this if the transport is an all round trip', max_length=255, null=True),
        ),
    ]
