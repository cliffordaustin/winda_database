# Generated by Django 3.2 on 2022-08-12 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0127_auto_20220812_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='stay_home_is_non_resident',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stay_home_is_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='per_house_price_non_resident',
        ),
    ]
