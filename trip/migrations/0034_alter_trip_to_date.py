# Generated by Django 3.2 on 2022-06-14 00:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0033_alter_trip_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 0, 10, 12, 955335, tzinfo=utc)),
        ),
    ]