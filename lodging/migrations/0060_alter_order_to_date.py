# Generated by Django 3.2 on 2022-05-28 01:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0059_alter_order_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 1, 53, 34, 628337, tzinfo=utc)),
        ),
    ]
