# Generated by Django 3.2 on 2022-04-22 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0029_alter_review_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]