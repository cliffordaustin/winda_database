# Generated by Django 3.2 on 2022-09-19 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0141_event_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rooms',
            field=models.IntegerField(default=1),
        ),
    ]
