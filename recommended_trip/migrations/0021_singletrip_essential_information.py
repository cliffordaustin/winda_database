# Generated by Django 3.2 on 2022-08-17 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0020_singletrip_total_number_of_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='essential_information',
            field=models.TextField(blank=True, null=True),
        ),
    ]
