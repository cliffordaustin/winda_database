# Generated by Django 3.2 on 2022-08-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0052_bookedtrip'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedtrip',
            name='non_residents',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookedtrip',
            name='guests',
            field=models.IntegerField(blank=True, null=True, verbose_name='residents'),
        ),
    ]
