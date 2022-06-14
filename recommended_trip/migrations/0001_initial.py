# Generated by Django 3.2 on 2022-06-13 23:27

import core.utils
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transport', '0011_rename_refaundable_transportation_refundable'),
        ('activities', '0044_auto_20220613_2327'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lodging', '0086_auto_20220613_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each tags by using ' , '. Eg Honey moon, game, beach", null=True, size=None)),
                ('starting_point', models.CharField(blank=True, help_text='suggested starting point of the trip', max_length=250, null=True)),
                ('stay_num_of_adults', models.IntegerField(default=1)),
                ('stay_non_resident', models.BooleanField(default=False)),
                ('stay_num_of_children', models.IntegerField(default=0)),
                ('stay_plan', models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPPLE ROOM', 'TRIPPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM'), ('FAMILY ROOM', 'FAMILY ROOM')], default='STANDARD', max_length=100)),
                ('number_of_people', models.IntegerField(default=1)),
                ('user_need_a_driver', models.BooleanField(default=False)),
                ('nights', models.IntegerField(default=3)),
                ('activity_non_resident', models.BooleanField(default=False)),
                ('activity_pricing_type', models.CharField(choices=[('PER PERSON', 'PER PERSON'), ('PER ROOM', 'PER ROOM'), ('WHOLE PLACE', 'WHOLE PLACE')], default='PER PERSON', max_length=50)),
                ('activity_number_of_people', models.IntegerField(default=1, help_text='Set the default number of people coming for this experience. Make sure the experience supports a pricing plan of per person.')),
                ('activity_number_of_sessions', models.IntegerField(default=1, help_text='Set the default number of sessions for this experience. Make sure the experience supports a pricing plan of per session.')),
                ('activity_number_of_groups', models.IntegerField(default=1, help_text='Set the default number of group coming for this experience. Make sure the experience supports a pricing plan of per group.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activities')),
                ('stay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lodging.stays')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.transportation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SingleTripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.trip_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('trip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='single_trip_images', to='recommended_trip.singletrip')),
            ],
        ),
    ]
