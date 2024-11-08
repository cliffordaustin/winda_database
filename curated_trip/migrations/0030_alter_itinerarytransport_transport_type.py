# Generated by Django 3.2 on 2022-11-16 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0029_remove_tripwizard_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerarytransport',
            name='transport_type',
            field=models.CharField(choices=[('CAR HIRE', 'CAR HIRE'), ('CAR TRANSFER', 'CAR TRANSFER'), ('BUS TRANSFER', 'BUS TRANSFER'), ('TRAIN TRANSFER', 'TRAIN TRANSFER'), ('FLIGHT TRANSFER', 'FLIGHT TRANSFER')], default='CAR TRANSFER', max_length=100),
        ),
    ]
