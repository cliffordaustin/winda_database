# Generated by Django 3.2 on 2023-02-10 02:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0182_bookings_num_of_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='contact_emails',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=250, null=True), default=list, help_text='Add multiple emails separated by comma', size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=250, null=True),
        ),
    ]
