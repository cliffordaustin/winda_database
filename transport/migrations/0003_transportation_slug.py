# Generated by Django 3.2 on 2022-05-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_auto_20220521_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportation',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
