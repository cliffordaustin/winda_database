# Generated by Django 3.2 on 2022-10-20 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0034_requestinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='has_holiday_package',
            field=models.BooleanField(default=False),
        ),
    ]
