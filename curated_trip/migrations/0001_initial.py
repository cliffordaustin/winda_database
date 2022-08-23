# Generated by Django 3.2 on 2022-08-13 15:00

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0066_auto_20220809_0852'),
        ('transport', '0018_alter_transportation_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lodging', '0128_auto_20220812_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuratedTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('area_covered', models.CharField(blank=True, max_length=350, null=True)),
                ('total_number_of_days', models.IntegerField(blank=True, null=True)),
                ('starting_location', models.CharField(blank=True, max_length=255, null=True)),
                ('ending_location', models.CharField(blank=True, max_length=255, null=True)),
                ('honeymoon', models.BooleanField(default=False)),
                ('cultural', models.BooleanField(default=False)),
                ('weekend_getaway', models.BooleanField(default=False)),
                ('road_trip', models.BooleanField(default=False)),
                ('hiking', models.BooleanField(default=False)),
                ('beach', models.BooleanField(default=False)),
                ('beachfront', models.BooleanField(default=False)),
                ('all_female_owned', models.BooleanField(default=False)),
                ('culinary', models.BooleanField(default=False)),
                ('solo_experience', models.BooleanField(default=False)),
                ('shopping', models.BooleanField(default=False)),
                ('community_owned', models.BooleanField(default=False)),
                ('natural_and_wildlife', models.BooleanField(default=False)),
                ('group_getaway', models.BooleanField(default=False)),
                ('riverside', models.BooleanField(default=False)),
                ('day_trip', models.BooleanField(default=False)),
                ('off_grid', models.BooleanField(default=False)),
                ('beautiful_views', models.BooleanField(default=False)),
                ('quirky', models.BooleanField(default=False)),
                ('conservancies', models.BooleanField(default=False)),
                ('wellness', models.BooleanField(default=False)),
                ('active_adventure', models.BooleanField(default=False)),
                ('game', models.BooleanField(default=False)),
                ('romantic_getaway', models.BooleanField(default=False)),
                ('farmstay', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('cycling', models.BooleanField(default=False)),
                ('lake', models.BooleanField(default=False)),
                ('walking', models.BooleanField(default=False)),
                ('family', models.BooleanField(default=False)),
                ('couples', models.BooleanField(default=False)),
                ('friends', models.BooleanField(default=False)),
                ('caves', models.BooleanField(default=False)),
                ('surfing', models.BooleanField(default=False)),
                ('tropical', models.BooleanField(default=False)),
                ('camping', models.BooleanField(default=False)),
                ('mountain', models.BooleanField(default=False)),
                ('cabin', models.BooleanField(default=False)),
                ('desert', models.BooleanField(default=False)),
                ('treehouse', models.BooleanField(default=False)),
                ('boat', models.BooleanField(default=False)),
                ('creative_space', models.BooleanField(default=False)),
                ('pricing_type', models.CharField(choices=[('REASONABLE', 'REASONABLE'), ('MID-RANGE', 'MID-RANGE'), ('HIGH-END', 'HIGH-END')], default='REASONABLE', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TransportationTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.transportation')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_trip', to='curated_trip.curatedtrip')),
            ],
        ),
        migrations.CreateModel(
            name='StayTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('stay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lodging.stays')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stay_trip', to='curated_trip.curatedtrip')),
            ],
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, help_text="Day of the trip. eg 'Day 1'.", max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='curated_trip.curatedtrip')),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
            },
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
            name='CuratedTripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.trip_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curated_trip_images', to='curated_trip.curatedtrip')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activities')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_trip', to='curated_trip.curatedtrip')),
            ],
        ),
    ]