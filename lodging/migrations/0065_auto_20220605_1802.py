# Generated by Django 3.2 on 2022-06-05 18:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0064_auto_20220604_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 18, 2, 10, 857957, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 18, 2, 10, 857957, tzinfo=utc)),
        ),
    ]
