# Generated by Django 3.2 on 2022-06-15 10:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0048_auto_20220615_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 18, 10, 47, 28, 937679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 18, 10, 47, 28, 937679, tzinfo=utc)),
        ),
    ]
