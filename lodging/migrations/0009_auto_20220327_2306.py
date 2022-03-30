# Generated by Django 3.2 on 2022-03-27 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0008_auto_20220327_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='images',
        ),
        migrations.AddField(
            model_name='stays',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='StayImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stay_images', to='lodging.stays')),
            ],
        ),
    ]