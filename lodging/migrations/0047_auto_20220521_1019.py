# Generated by Django 3.2 on 2022-05-21 10:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0046_auto_20220520_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='from_date',
            field=models.DateTimeField(default=datetime.date(2022, 5, 21)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.date(2022, 5, 24)),
        ),
    ]
