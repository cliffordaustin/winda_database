# Generated by Django 3.2 on 2022-05-26 09:57

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0012_alter_order_to_date'),
        ('lodging', '0054_alter_order_to_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transport', '0006_auto_20220524_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=False)),
                ('transport_back', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.transportation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activities')),
                ('stay', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lodging.stays')),
                ('transport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.transportation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.trip_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_images', to='trip.trip')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.group_trip_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('group_trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_trip_images', to='trip.grouptrip')),
            ],
        ),
        migrations.AddField(
            model_name='grouptrip',
            name='trip',
            field=models.ManyToManyField(related_name='group_trip', to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='grouptrip',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
