# Generated by Django 3.2 on 2022-09-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0146_auto_20220920_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='distance_from_venue',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
