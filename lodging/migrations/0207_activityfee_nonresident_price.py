# Generated by Django 3.2 on 2023-06-07 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0206_auto_20230606_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityfee',
            name='nonresident_price',
            field=models.FloatField(default=0),
        ),
    ]