# Generated by Django 3.2 on 2022-03-31 10:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0017_stays_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stays',
            name='amenities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250, null=True), blank=True, default=list, help_text="Separate each amenities by using ','. Eg Swimming Pool, Hot tub", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_boutique_hotel',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each description by using ','. Eg Historical building, Resort", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_campsite',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each description by using ','. Eg On private property, In a conservancy", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_house',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each description by using ','. Eg Residential home, Villa", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_lodge',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each description by using ','. Eg Tented camp, Permanent structures", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='best_describes_unique_space',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate each description by using ','. Eg Boathouse, Bus", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='name',
            field=models.CharField(help_text="If no name, enter a short description of the accommodation. Eg 'A lovely place located at the lake side'", max_length=250),
        ),
    ]