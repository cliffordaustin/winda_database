# Generated by Django 3.2 on 2023-01-11 02:21

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0168_auto_20221221_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllInclusive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('stay', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='all_inclusive', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'All Inclusive',
                'verbose_name_plural': 'All Inclusive',
            },
        ),
        migrations.AlterModelOptions(
            name='privatesafari',
            options={'verbose_name': 'Full Board', 'verbose_name_plural': 'Full Boards'},
        ),
        migrations.AlterModelOptions(
            name='privatesafariimages',
            options={'verbose_name': 'Full Board Image', 'verbose_name_plural': 'Full Board Images'},
        ),
        migrations.AlterModelOptions(
            name='sharedsafari',
            options={'verbose_name': 'Game Package', 'verbose_name_plural': 'Game Packages'},
        ),
        migrations.AlterModelOptions(
            name='sharedsafariimages',
            options={'verbose_name': 'Game Package Image', 'verbose_name_plural': 'Game Package Images'},
        ),
        migrations.CreateModel(
            name='AllInclusiveImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.lodge_image_thumbnail)),
                ('main', models.BooleanField(default=False)),
                ('all_inclusive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_inclusive_images', to='lodging.allinclusive')),
            ],
            options={
                'verbose_name': 'All Inclusive Image',
                'verbose_name_plural': 'All Inclusive Images',
            },
        ),
    ]
