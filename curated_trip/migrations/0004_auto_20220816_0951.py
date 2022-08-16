# Generated by Django 3.2 on 2022-08-16 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curated_trip', '0003_auto_20220816_0943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertrips',
            options={'ordering': ['-created_at'], 'verbose_name': 'Group User Trip', 'verbose_name_plural': 'Group User Trips'},
        ),
        migrations.AlterField(
            model_name='usertrip',
            name='trips',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='curated_trip.usertrips'),
            preserve_default=False,
        ),
    ]
