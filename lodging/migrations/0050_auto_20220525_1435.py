# Generated by Django 3.2 on 2022-05-25 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0049_auto_20220524_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 25, 14, 35, 12, 833160)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 14, 35, 12, 830448)),
        ),
    ]
