# Generated by Django 3.2 on 2022-12-19 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0165_auto_20221219_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatesafari',
            name='stay',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='private_safari_options', to='lodging.stays'),
        ),
        migrations.AlterField(
            model_name='sharedsafari',
            name='stay',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shared_safari_options', to='lodging.stays'),
        ),
    ]
