# Generated by Django 3.2 on 2022-05-27 19:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0056_auto_20220527_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 30, 19, 46, 31, 580797, tzinfo=utc)),
        ),
    ]
