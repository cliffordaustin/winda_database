# Generated by Django 3.2 on 2022-09-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0153_typeofrooms_not_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='has_min_date',
            field=models.BooleanField(default=False),
        ),
    ]
