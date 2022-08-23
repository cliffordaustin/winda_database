# Generated by Django 3.2 on 2022-08-23 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0020_flight_number_of_people'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='reviewing',
            field=models.BooleanField(default=True),
        ),
    ]