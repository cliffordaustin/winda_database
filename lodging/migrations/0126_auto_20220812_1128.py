# Generated by Django 3.2 on 2022-08-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0125_auto_20220812_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='stay_is_a_home',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stay_is_a_home',
        ),
        migrations.AddField(
            model_name='cart',
            name='stay_home_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='stay_home_capacity',
            field=models.IntegerField(default=0),
        ),
    ]
