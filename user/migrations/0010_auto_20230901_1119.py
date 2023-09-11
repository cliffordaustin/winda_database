# Generated by Django 3.2 on 2023-09-01 11:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20230901_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
