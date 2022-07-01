# Generated by Django 3.2 on 2022-07-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0111_auto_20220630_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='plan',
            field=models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPPLE ROOM', 'TRIPPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM'), ('EXECUTIVE SUITE ROOM', 'EXECUTIVE SUITE ROOM'), ('FAMILY ROOM', 'FAMILY ROOM'), ('PRESIDENTIAL SUITE ROOM', 'PRESIDENTIAL SUITE ROOM'), ('EMPEROR SUITE ROOM', 'EMPEROR SUITE ROOM')], default='STANDARD', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='plan',
            field=models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPPLE ROOM', 'TRIPPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM'), ('EXECUTIVE SUITE ROOM', 'EXECUTIVE SUITE ROOM'), ('FAMILY ROOM', 'FAMILY ROOM'), ('PRESIDENTIAL SUITE ROOM', 'PRESIDENTIAL SUITE ROOM'), ('EMPEROR SUITE ROOM', 'EMPEROR SUITE ROOM')], default='STANDARD', max_length=100),
        ),
    ]
