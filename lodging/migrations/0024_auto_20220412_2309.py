# Generated by Django 3.2 on 2022-04-12 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0023_sum_prices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='pricing_per_person',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='pricing_per_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='pricing_per_whole_place',
        ),
    ]
