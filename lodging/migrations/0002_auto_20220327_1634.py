# Generated by Django 3.2 on 2022-03-27 16:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='type_of_lodge',
        ),
        migrations.AddField(
            model_name='stays',
            name='type_of_lodge',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), null=True, size=None),
        ),
    ]
