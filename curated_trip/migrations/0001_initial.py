# Generated by Django 3.2 on 2022-10-22 16:33

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lodging', '0158_auto_20221016_2302'),
        ('activities', '0072_auto_20221016_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('number_of_countries', models.IntegerField(default=1)),
                ('total_number_of_days', models.IntegerField(blank=True, null=True)),
                ('essential_information', models.TextField(blank=True, null=True)),
                ('local_guide_available', models.BooleanField(default=False)),
                ('max_number_of_people', models.IntegerField(blank=True, null=True)),
                ('trip_is_carbon_neutral', models.BooleanField(default=False)),
                ('weekend_getaway', models.BooleanField(default=False)),
                ('road_trip', models.BooleanField(default=False)),
                ('cultural', models.BooleanField(default=False)),
                ('lake', models.BooleanField(default=False)),
                ('day_game_drives', models.BooleanField(default=False)),
                ('walking_hiking', models.BooleanField(default=False, verbose_name='Walking/hinking')),
                ('beach', models.BooleanField(default=False)),
                ('family', models.BooleanField(default=False, verbose_name='Families')),
                ('romantic', models.BooleanField(default=False)),
                ('culinary', models.BooleanField(default=False)),
                ('day_trips', models.BooleanField(default=False)),
                ('community_owned', models.BooleanField(default=False)),
                ('off_grid', models.BooleanField(default=False)),
                ('solo_getaway', models.BooleanField(default=False)),
                ('wellness', models.BooleanField(default=False)),
                ('unconventional_safaris', models.BooleanField(default=False)),
                ('shopping', models.BooleanField(default=False)),
                ('art', models.BooleanField(default=False)),
                ('watersports', models.BooleanField(default=False)),
                ('sailing', models.BooleanField(default=False)),
                ('night_game_drives', models.BooleanField(default=False)),
                ('sustainable', models.BooleanField(default=False)),
                ('all_female', models.BooleanField(default=False, verbose_name='All-female')),
                ('groups', models.BooleanField(default=False)),
                ('luxury', models.BooleanField(default=False)),
                ('budget', models.BooleanField(default=False)),
                ('mid_range', models.BooleanField(default=False)),
                ('short_getaways', models.BooleanField(default=False)),
                ('cross_country', models.BooleanField(default=False, verbose_name='Cross-country')),
                ('park_conservancies', models.BooleanField(default=False, verbose_name='Park & Conservancies')),
                ('pricing_type', models.CharField(choices=[('REASONABLE', 'REASONABLE'), ('MID-RANGE', 'MID-RANGE'), ('HIGH-END', 'HIGH-END')], default='REASONABLE', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('old_price', models.FloatField(blank=True, help_text='add the previous price(old price)', null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('price_non_resident', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, help_text='Select the day of this itinerary', max_length=200, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('breakfast_included', models.BooleanField(default=False)),
                ('lunch_included', models.BooleanField(default=False)),
                ('dinner_included', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='curated_trip.curatedtrip')),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.CreateModel(
            name='SimilarTrips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curated_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_trips', to='curated_trip.curatedtrip')),
            ],
            options={
                'verbose_name': 'Similar Trip',
                'verbose_name_plural': 'Similar Trips',
            },
        ),
        migrations.CreateModel(
            name='OptionalItineraryActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(blank=True, help_text='Activity Name. price should be added if available. e.g. Hiking - 100 USD', max_length=500, null=True)),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optional_activities', to='curated_trip.itinerary')),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_location', models.CharField(blank=True, max_length=255, null=True)),
                ('ending_location', models.CharField(blank=True, max_length=255, null=True)),
                ('transport_type', models.CharField(choices=[('CAR', 'CAR'), ('BUS', 'BUS'), ('TRAIN', 'TRAIN'), ('FLIGHT', 'FLIGHT')], default='CAR', max_length=100)),
                ('driver_included_in_car', models.BooleanField(default=False, help_text='Is a driver included?')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_transports', to='curated_trip.itinerary')),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, help_text='Location Name', max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_locations', to='curated_trip.itinerary')),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryAccommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nights', models.IntegerField(default=1, help_text='Number of nights')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_stays', to='curated_trip.itinerary')),
                ('stay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lodging.stays')),
            ],
        ),
        migrations.CreateModel(
            name='IncludedItineraryActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activities')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_activities', to='curated_trip.itinerary')),
            ],
        ),
        migrations.CreateModel(
            name='FrequentlyAskedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='curated_trip.curatedtrip')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='CuratedTripLocations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('curated_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='curated_trip.curatedtrip')),
            ],
            options={
                'verbose_name': 'Curated Trip Location',
                'verbose_name_plural': 'Curated Trip Locations',
            },
        ),
        migrations.CreateModel(
            name='CuratedTripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.trip_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curated_trip_images', to='curated_trip.curatedtrip')),
            ],
        ),
    ]
