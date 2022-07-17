# Generated by Django 3.2 on 2022-07-17 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0011_triphighlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='cultural',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='cycling',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='road_trip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='romantic_getaway',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='walking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='weekend_getaway',
            field=models.BooleanField(default=False),
        ),
    ]
