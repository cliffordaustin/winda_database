# Generated by Django 3.2 on 2022-07-20 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0016_singletrip_area_covered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triphighlight',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_highlights', to='recommended_trip.singletrip'),
        ),
    ]
