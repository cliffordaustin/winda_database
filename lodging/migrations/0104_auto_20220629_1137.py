# Generated by Django 3.2 on 2022-06-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0103_remove_stays_salon'),
    ]

    operations = [
        migrations.AddField(
            model_name='stays',
            name='children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='deluxe_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='deluxe_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='double_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='double_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='emperor_suite_room_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='family_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='family_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='king_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='king_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='presidential_suite_room_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='quad_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='quad_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='queen_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='queen_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='studio_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='studio_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='super_deluxe_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='super_deluxe_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='tripple_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='tripple_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='twin_room_children_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stays',
            name='twin_room_children_price_non_resident',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='plan',
            field=models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPPLE ROOM', 'TRIPPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM'), ('FAMILY ROOM', 'FAMILY ROOM'), ('PRESIDENTIAL SUITE', 'PRESIDENTIAL SUITE'), ('EMPEROR SUITE', 'EMPEROR SUITE')], default='STANDARD', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='plan',
            field=models.CharField(choices=[('STANDARD', 'STANDARD'), ('DELUXE', 'DELUXE'), ('SUPER DELUXE', 'SUPER DELUXE'), ('STUDIO', 'STUDIO'), ('DOUBLE ROOM', 'DOUBLE ROOM'), ('TRIPPLE ROOM', 'TRIPPLE ROOM'), ('QUAD ROOM', 'QUAD ROOM'), ('KING ROOM', 'KING ROOM'), ('QUEEN ROOM', 'QUEEN ROOM'), ('TWIN ROOM', 'TWIN ROOM'), ('FAMILY ROOM', 'FAMILY ROOM'), ('PRESIDENTIAL SUITE', 'PRESIDENTIAL SUITE'), ('EMPEROR SUITE', 'EMPEROR SUITE')], default='STANDARD', max_length=100),
        ),
    ]