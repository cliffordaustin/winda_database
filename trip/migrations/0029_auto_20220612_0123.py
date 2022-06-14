# Generated by Django 3.2 on 2022-06-12 01:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0028_alter_trip_to_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='activity_number_of_poeple',
            new_name='activity_number_of_people',
        ),
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 1, 23, 9, 92708, tzinfo=utc)),
        ),
    ]