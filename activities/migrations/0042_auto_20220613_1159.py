# Generated by Django 3.2 on 2022-06-13 11:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0041_auto_20220612_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='refaundable',
            new_name='refundable',
        ),
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 11, 59, 21, 76536, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 11, 59, 21, 76536, tzinfo=utc)),
        ),
    ]
