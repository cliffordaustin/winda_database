# Generated by Django 3.2 on 2022-06-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0006_auto_20220524_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_per_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='user_need_a_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_per_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='user_need_a_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transportation',
            name='additional_price_with_a_driver',
            field=models.FloatField(blank=True, help_text='Price when a user needs a driver', null=True),
        ),
        migrations.AddField(
            model_name='transportation',
            name='price_per_day',
            field=models.FloatField(blank=True, help_text='Price per day, if available', null=True),
        ),
    ]
