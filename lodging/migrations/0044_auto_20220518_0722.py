# Generated by Django 3.2 on 2022-05-18 07:22

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0043_auto_20220429_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='from_date',
            field=models.DateField(default=datetime.date(2022, 5, 18)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateField(default=datetime.date(2022, 5, 19)),
        ),
    ]