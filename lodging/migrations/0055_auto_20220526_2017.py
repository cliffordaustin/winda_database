# Generated by Django 3.2 on 2022-05-26 20:17

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0006_auto_20220524_1820'),
        ('lodging', '0054_alter_order_to_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transport_back',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transport_back', to='transport.transportation'),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 20, 17, 12, 465129, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='transport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transport', to='transport.transportation'),
        ),
    ]
