# Generated by Django 3.2 on 2022-08-11 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0018_alter_singletrip_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='ending_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='singletrip',
            name='starting_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, help_text="Day of the trip. eg 'Day 1'.", max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='recommended_trip.singletrip')),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.CreateModel(
            name='FrequentlyAskedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='recommended_trip.singletrip')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
    ]
