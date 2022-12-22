# Generated by Django 3.2 on 2022-12-20 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0166_auto_20221219_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatesafariimages',
            name='main',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sharedsafariimages',
            name='main',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='privatesafari',
            name='stay',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='private_safari', to='lodging.stays'),
        ),
        migrations.AlterField(
            model_name='sharedsafari',
            name='stay',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shared_safari', to='lodging.stays'),
        ),
    ]
