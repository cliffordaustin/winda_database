# Generated by Django 3.2 on 2023-03-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0193_auto_20230227_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherfeesnonresident',
            name='guest_type',
            field=models.CharField(blank=True, choices=[('ADULT', 'ADULT'), ('CHILD', 'CHILD')], max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='otherfeesresident',
            name='guest_type',
            field=models.CharField(blank=True, choices=[('ADULT', 'ADULT'), ('CHILD', 'CHILD')], max_length=120, null=True),
        ),
    ]