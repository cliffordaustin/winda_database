# Generated by Django 3.2 on 2023-01-25 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0176_alter_otheroption_stay'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='is_kaleidoscope_event',
            field=models.BooleanField(default=False),
        ),
    ]