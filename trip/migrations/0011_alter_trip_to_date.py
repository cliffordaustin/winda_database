# Generated by Django 3.2 on 2022-06-04 00:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0010_alter_trip_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 7, 0, 38, 43, 417787, tzinfo=utc)),
        ),
    ]
