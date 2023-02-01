# Generated by Django 3.2 on 2022-12-19 21:42

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0164_auto_20221219_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateSafari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(blank=True, max_length=500, null=True)),
                ('available', models.BooleanField(default=True)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_safari_options', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'Private Safari',
                'verbose_name_plural': 'Private Safaris',
            },
        ),
        migrations.CreateModel(
            name='PrivateSafariImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.lodge_image_thumbnail)),
                ('private_safari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_safari_images', to='lodging.privatesafari')),
            ],
            options={
                'verbose_name': 'Private Safari Image',
                'verbose_name_plural': 'Private Safari Images',
            },
        ),
        migrations.CreateModel(
            name='SharedSafari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(blank=True, max_length=500, null=True)),
                ('available', models.BooleanField(default=True)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_safari_options', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'Shared Safari',
                'verbose_name_plural': 'Shared Safaris',
            },
        ),
        migrations.CreateModel(
            name='SharedSafariImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.lodge_image_thumbnail)),
                ('shared_safari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_safari_images', to='lodging.sharedsafari')),
            ],
            options={
                'verbose_name': 'Shared Safari Image',
                'verbose_name_plural': 'Shared Safari Images',
            },
        ),
        migrations.RemoveField(
            model_name='typeofoptionsimages',
            name='type_of_option',
        ),
        migrations.DeleteModel(
            name='TypeOfOptions',
        ),
        migrations.DeleteModel(
            name='TypeOfOptionsImages',
        ),
    ]