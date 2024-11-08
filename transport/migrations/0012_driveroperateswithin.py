# Generated by Django 3.2 on 2022-06-27 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0011_rename_refaundable_transportation_refundable'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverOperatesWithin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=350, null=True)),
                ('country', models.CharField(blank=True, max_length=350, null=True)),
                ('transportation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_operates_within', to='transport.transportation')),
            ],
        ),
    ]
