# Generated by Django 3.2 on 2022-09-08 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0134_stays_beachfront'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
