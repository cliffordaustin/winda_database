# Generated by Django 3.2 on 2022-08-22 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0027_auto_20220822_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='nights',
            field=models.IntegerField(default=3, verbose_name='Number of nights for stay'),
        ),
    ]
