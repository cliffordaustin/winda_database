# Generated by Django 3.2 on 2022-08-09 08:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0121_remove_stays_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='other_amenities',
        ),
        migrations.AlterField(
            model_name='review',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='stays',
            name='city',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='county'),
        ),
    ]
