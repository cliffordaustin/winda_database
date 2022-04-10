# Generated by Django 3.2 on 2022-03-30 23:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0014_alter_stays_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stays',
            name='amenities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_boutique_hotel',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_campsite',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_house',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_lodge',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_unique_space',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, null=True, size=None),
        ),
    ]