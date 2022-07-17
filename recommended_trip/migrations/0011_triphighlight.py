# Generated by Django 3.2 on 2022-07-17 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0010_alter_singletrip_price_budget'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripHighlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlight', models.CharField(blank=True, max_length=255, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommended_trip.singletrip')),
            ],
        ),
    ]
