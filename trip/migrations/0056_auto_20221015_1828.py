# Generated by Django 3.2 on 2022-10-15 18:28

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0055_bookedtrip_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedtrip',
            name='email',
            field=models.EmailField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bookedtrip',
            name='first_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bookedtrip',
            name='last_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bookedtrip',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
