# Generated by Django 3.2 on 2022-03-30 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0013_auto_20220330_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stays',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=255, null=True),
        ),
    ]
