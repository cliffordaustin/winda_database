# Generated by Django 3.2 on 2022-06-09 13:28

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0072_auto_20220609_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='experiences_included',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Experiences included in this package ' , '. Eg Camping, Fishing, Hiking", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 13, 28, 41, 661370, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 13, 28, 41, 661370, tzinfo=utc)),
        ),
    ]
