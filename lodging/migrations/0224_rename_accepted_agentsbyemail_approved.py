# Generated by Django 3.2 on 2023-08-21 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0223_auto_20230821_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agentsbyemail',
            old_name='accepted',
            new_name='approved',
        ),
    ]
