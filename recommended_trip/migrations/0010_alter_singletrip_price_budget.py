# Generated by Django 3.2 on 2022-06-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0009_singletrip_price_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singletrip',
            name='price_budget',
            field=models.CharField(choices=[('BUDGET', 'BUDGET'), ('MID RANGE', 'MID RANGE'), ('LUXURY', 'LUXURY')], default='MID RANGE', max_length=100),
        ),
    ]