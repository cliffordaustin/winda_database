# Generated by Django 3.2 on 2023-05-03 00:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sessions', '0001_initial'),
        ('lodging', '0204_stays_lodge_price_data_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='annonymous_added_to_calculate',
            field=models.ManyToManyField(blank=True, related_name='annonymous_added_to_calculate', to='sessions.Session'),
        ),
        migrations.AddField(
            model_name='stays',
            name='user_added_to_calculate',
            field=models.ManyToManyField(blank=True, related_name='user_added_to_calculate', to=settings.AUTH_USER_MODEL),
        ),
    ]
