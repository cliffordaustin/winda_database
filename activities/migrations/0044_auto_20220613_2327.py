# Generated by Django 3.2 on 2022-06-13 23:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0043_auto_20220613_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 23, 27, 15, 159051, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 23, 27, 15, 159051, tzinfo=utc)),
        ),
    ]
