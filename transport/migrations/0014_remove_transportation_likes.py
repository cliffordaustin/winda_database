# Generated by Django 3.2 on 2022-06-28 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0013_auto_20220628_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportation',
            name='likes',
        ),
    ]