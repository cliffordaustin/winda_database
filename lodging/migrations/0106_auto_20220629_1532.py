# Generated by Django 3.2 on 2022-06-29 15:32

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0105_stays_pricing_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='experiences_included',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='facts',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='included',
        ),
        migrations.AlterField(
            model_name='stays',
            name='other_amenities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), blank=True, default=list, help_text="Separate all included items by using ' , '. If the text includes a comma, then place it in a single quote ' , '.", null=True, size=None),
        ),
        migrations.AlterField(
            model_name='stays',
            name='type_of_stay',
            field=models.CharField(blank=True, choices=[('LODGE', 'LODGE'), ('HOUSE', 'HOUSE'), ('UNIQUE SPACE', 'UNIQUE SPACE'), ('CAMPSITE', 'CAMPSITE'), ('BOUTIQUE HOTEL', 'BOUTIQUE HOTEL'), ('WEEKEND GETAWAY', 'WEEKEND GETAWAY'), ('ROMANTIC GETAWAY', 'ROMANTIC GETAWAY'), ('GROUP GETAWAY', 'GROUP GETAWAY'), ('CONSERVANCY', 'CONSERVANCY'), ('NATIONAL PARK/GAME RESERVES', 'NATIONAL PARK/GAME RESERVES'), ('COZY PLACE', 'COZY PLACE'), ('LAKEFRONT', 'LAKEFRONT'), ('BEACHFRONT', 'BEACHFRONT'), ('LUXURIOUS', 'LUXURIOUS'), ('BEAUTIFUL VIEW', 'BEAUTIFUL VIEW'), ('OFF-GRID', 'OFF-GRID'), ('ECO-STAY', 'ECO-STAY'), ('QUIRKY', 'QUIRKY'), ('TRADITIONAL', 'TRADITIONAL'), ('MANSIONS', 'MANSIONS'), ('OVER-WATER', 'OVER-WATER'), ('UNIQUE EXPERIENCES', 'UNIQUE EXPERIENCES'), ('STUNNING ARCHITECTURE', 'STUNNING ARCHITECTURE'), ('HONEYMOON SPOT', 'HONEYMOON SPOT'), ('RIVERFRONT', 'RIVERFRONT'), ('PRIVATE HOUSE', 'PRIVATE HOUSE'), ('RESORT', 'RESORT')], max_length=100),
        ),
        migrations.CreateModel(
            name='Inclusions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inclusions', to='lodging.stays')),
            ],
        ),
        migrations.CreateModel(
            name='Facts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='lodging.stays')),
            ],
        ),
        migrations.CreateModel(
            name='ExperiencesIncluded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences_included', to='lodging.stays')),
            ],
        ),
    ]