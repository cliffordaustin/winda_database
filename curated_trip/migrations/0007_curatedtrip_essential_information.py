# Generated by Django 3.2 on 2022-08-17 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0006_auto_20220816_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='curatedtrip',
            name='essential_information',
            field=models.TextField(blank=True, null=True),
        ),
    ]
