# Generated by Django 3.2 on 2022-05-18 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20220518_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='city',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='activities',
            name='country',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='activities',
            name='location',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Address'),
        ),
    ]
