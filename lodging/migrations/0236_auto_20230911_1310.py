# Generated by Django 3.2 on 2023-09-11 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0235_agentsbyemail_contract_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyaccess',
            name='accepted_invite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='propertyaccess',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
