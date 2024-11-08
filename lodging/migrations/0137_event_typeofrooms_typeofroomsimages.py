# Generated by Django 3.2 on 2022-09-16 22:59

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lodging', '0136_auto_20220913_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeOfRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_images', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'Type of Room',
                'verbose_name_plural': 'Types of Rooms',
            },
        ),
        migrations.CreateModel(
            name='TypeOfRoomsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.lodge_image_thumbnail)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_room_images', to='lodging.typeofrooms')),
            ],
            options={
                'verbose_name': 'Type of Room Image',
                'verbose_name_plural': 'Types of Room Images',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
                ('num_of_guests', models.IntegerField(default=1)),
                ('first_name', models.CharField(blank=True, max_length=120, null=True)),
                ('last_name', models.CharField(blank=True, max_length=120, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('stay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_order', to='lodging.stays')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
