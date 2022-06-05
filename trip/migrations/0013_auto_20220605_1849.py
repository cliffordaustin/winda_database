# Generated by Django 3.2 on 2022-06-05 18:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0012_auto_20220605_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='is_transport_per_day',
        ),
        migrations.AddField(
            model_name='trip',
            name='number_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 18, 49, 55, 794490, tzinfo=utc)),
        ),
    ]
