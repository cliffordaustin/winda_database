# Generated by Django 3.2 on 2022-06-05 23:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0066_auto_20220605_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 23, 37, 23, 603025, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 23, 37, 23, 603025, tzinfo=utc)),
        ),
    ]
