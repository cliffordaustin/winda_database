# Generated by Django 3.2 on 2022-10-31 21:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0159_stays_has_holiday_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='unavailable_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, help_text="Select the dates you won't be available ' , '", null=True, size=None),
        ),
    ]
