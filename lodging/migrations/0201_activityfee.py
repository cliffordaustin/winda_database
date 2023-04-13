# Generated by Django 3.2 on 2023-04-10 11:25

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0200_auto_20230410_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(default=0)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=core.utils.activity_fees_image_thumbnail)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_fees', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'Activity Fee',
                'verbose_name_plural': 'Activity Fees',
            },
        ),
    ]
