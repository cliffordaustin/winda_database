# Generated by Django 3.2 on 2022-06-06 01:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0008_auto_20220605_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='from_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='from_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
