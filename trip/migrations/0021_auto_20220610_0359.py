# Generated by Django 3.2 on 2022-06-10 03:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0020_alter_trip_to_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='stay_non_resident',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 13, 3, 59, 28, 326841, tzinfo=utc)),
        ),
    ]