# Generated by Django 3.2 on 2022-06-14 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0003_singletrip_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='singletrip',
            old_name='familiy',
            new_name='family',
        ),
    ]
