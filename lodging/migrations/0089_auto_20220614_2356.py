# Generated by Django 3.2 on 2022-06-14 23:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0088_auto_20220614_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 23, 56, 1, 266024, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 23, 56, 1, 266024, tzinfo=utc)),
        ),
    ]