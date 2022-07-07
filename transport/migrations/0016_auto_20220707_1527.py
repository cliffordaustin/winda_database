# Generated by Django 3.2 on 2022-07-07 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0015_auto_20220707_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportation',
            name='audio_input',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='bluetooth',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='cd_player',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='children_allowed',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='covid_19_compliance',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='covid_19_compliance_details',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='cruise_control',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='damage_policy',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='dropoff_city',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='dropoff_country',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='fm_radio',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='included_in_price',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='open_roof',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='overhead_passenger_airbag',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='pets_allowed',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='power_locks',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='power_mirrors',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='power_windows',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='refund_policy',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='refundable',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='safety_tools',
        ),
        migrations.RemoveField(
            model_name='transportation',
            name='side_airbag',
        ),
        migrations.CreateModel(
            name='IncludedInPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('included_in_price', models.CharField(blank=True, max_length=500, null=True)),
                ('transportation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='included_in_price', to='transport.transportation')),
            ],
        ),
    ]
