# Generated by Django 3.2 on 2022-06-14 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_trip', '0002_auto_20220614_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]