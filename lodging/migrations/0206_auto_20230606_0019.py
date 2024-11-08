# Generated by Django 3.2 on 2023-06-06 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0205_auto_20230503_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherfeesnonresident',
            name='guest_type',
        ),
        migrations.RemoveField(
            model_name='otherfeesnonresident',
            name='is_park_fee',
        ),
        migrations.RemoveField(
            model_name='otherfeesnonresident',
            name='nonresident_fee_type',
        ),
        migrations.RemoveField(
            model_name='otherfeesresident',
            name='guest_type',
        ),
        migrations.RemoveField(
            model_name='otherfeesresident',
            name='is_park_fee',
        ),
        migrations.RemoveField(
            model_name='otherfeesresident',
            name='resident_fee_type',
        ),
        migrations.AddField(
            model_name='otherfeesnonresident',
            name='adult_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='otherfeesnonresident',
            name='child_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='otherfeesnonresident',
            name='teen_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='otherfeesresident',
            name='adult_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='otherfeesresident',
            name='child_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='otherfeesresident',
            name='teen_price',
            field=models.FloatField(default=0),
        ),
    ]
