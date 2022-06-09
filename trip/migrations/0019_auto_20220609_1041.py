# Generated by Django 3.2 on 2022-06-09 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0018_alter_trip_to_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='stay_num_of_adults',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='trip',
            name='stay_num_of_children',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trip',
            name='stay_plan',
            field=models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPLE ROOM', 'TRIPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM')], default='STANDARD', max_length=100),
        ),
        migrations.AlterField(
            model_name='trip',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 12, 10, 40, 46, 57948, tzinfo=utc)),
        ),
    ]
