# Generated by Django 3.2 on 2022-09-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0025_generaltransfers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generaltransfers',
            name='cancelled',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='email_sent',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='number_of_people',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='reviewing',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='transfer_types',
        ),
        migrations.RemoveField(
            model_name='generaltransfers',
            name='user_has_ordered',
        ),
        migrations.AddField(
            model_name='generaltransfers',
            name='is_train',
            field=models.BooleanField(default=False, verbose_name='Check the box if it is a train transfer'),
        ),
    ]
