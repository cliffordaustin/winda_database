# Generated by Django 3.2 on 2022-09-06 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0026_auto_20220906_1537'),
        ('recommended_trip', '0032_singletrip_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletrip',
            name='general_transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.generaltransfers'),
        ),
    ]
