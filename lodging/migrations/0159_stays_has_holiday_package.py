# Generated by Django 3.2 on 2022-10-28 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0158_auto_20221016_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='has_holiday_package',
            field=models.BooleanField(default=False),
        ),
    ]