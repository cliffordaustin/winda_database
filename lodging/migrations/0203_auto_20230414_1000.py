# Generated by Django 3.2 on 2023-04-14 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0202_activityfee_price_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stays',
            name='children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='conservation_or_park_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='deluxe_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='double_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='emperor_suite_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='executive_suite_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='family_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='king_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='per_house',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='per_house_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='presidential_suite_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='quad_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='queen_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='standard',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='standard_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='studio_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='super_deluxe_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='tripple_room_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_capacity',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_children_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_children_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_child_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_child_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_single_teen_price_non_resident',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_teen_price',
        ),
        migrations.RemoveField(
            model_name='stays',
            name='twin_room_teen_price_non_resident',
        ),
        migrations.AddField(
            model_name='roomavailabilitynonresidentguest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='roomavailabilityresidentguest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roomavailabilitynonresidentguest',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='roomavailabilityresidentguest',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
