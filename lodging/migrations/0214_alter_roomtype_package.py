# Generated by Django 3.2 on 2023-07-02 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0213_roomtype_package_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='package',
            field=models.CharField(default='ALL INCLUSIVE', max_length=120),
        ),
    ]
