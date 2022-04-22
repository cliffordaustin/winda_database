# Generated by Django 3.2 on 2022-04-21 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0025_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.TextField(default=None)),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='lodging.stays')),
            ],
            options={
                'verbose_name': 'Stay Views',
            },
        ),
    ]