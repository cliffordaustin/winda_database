# Generated by Django 3.2 on 2022-06-11 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0077_auto_20220610_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 6, 55, 49, 938149, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 14, 6, 55, 49, 938149, tzinfo=utc)),
        ),
    ]
