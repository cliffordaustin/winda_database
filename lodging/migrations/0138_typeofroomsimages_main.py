# Generated by Django 3.2 on 2022-09-17 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0137_event_typeofrooms_typeofroomsimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeofroomsimages',
            name='main',
            field=models.BooleanField(default=False),
        ),
    ]