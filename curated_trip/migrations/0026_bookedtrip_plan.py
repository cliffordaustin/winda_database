# Generated by Django 3.2 on 2022-11-10 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0025_bookedtrip'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedtrip',
            name='plan',
            field=models.CharField(choices=[('PLAN A', 'PLAN A'), ('PLAN B', 'PLAN B'), ('PLAN C', 'PLAN C')], default='PLAN A', max_length=100),
        ),
    ]
