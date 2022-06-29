from asyncio import transports
from dbm.ndbm import library
from os import access
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from activities.models import Activities
from core.utils import lodge_image_thumbnail
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator, MaxValueValidator

from transport.models import Transportation

ROOM_IS_ENSUITE = (("YES", "YES"), ("NO", "NO"))

PRICING_TYPE = (
    ("REASONABLE", "REASONABLE"),
    ("MID-RANGE", "MID-RANGE"),
    ("HIGH-END", "HIGH-END"),
)

TYPE_OF_STAY = (
    ("LODGE", "LODGE"),
    ("HOUSE", "HOUSE"),
    ("UNIQUE SPACE", "UNIQUE SPACE"),
    ("CAMPSITE", "CAMPSITE"),
    ("TENTED CAMP", "TENTED CAMP"),
    ("BOUTIQUE HOTEL", "BOUTIQUE HOTEL"),
    ("WEEKEND GETAWAY", "WEEKEND GETAWAY"),
    ("ROMANTIC GETAWAY", "ROMANTIC GETAWAY"),
    ("GROUP GETAWAY", "GROUP GETAWAY"),
    ("CONSERVANCY", "CONSERVANCY"),
    ("NATIONAL PARK/GAME RESERVES", "NATIONAL PARK/GAME RESERVES"),
    ("COZY PLACE", "COZY PLACE"),
    ("LAKEFRONT", "LAKEFRONT"),
    ("BEACHFRONT", "BEACHFRONT"),
    ("LUXURIOUS", "LUXURIOUS"),
    ("BEAUTIFUL VIEW", "BEAUTIFUL VIEW"),
    ("OFF-GRID", "OFF-GRID"),
    ("ECO-STAY", "ECO-STAY"),
    ("QUIRKY", "QUIRKY"),
    ("TRADITIONAL", "TRADITIONAL"),
    ("MANSIONS", "MANSIONS"),
    ("OVER-WATER", "OVER-WATER"),
    ("UNIQUE EXPERIENCES", "UNIQUE EXPERIENCES"),
    ("STUNNING ARCHITECTURE", "STUNNING ARCHITECTURE"),
    ("HONEYMOON SPOT", "HONEYMOON SPOT"),
    ("RIVERFRONT", "RIVERFRONT"),
    ("PRIVATE HOUSE", "PRIVATE HOUSE"),
    ("RESORT", "RESORT"),
)

PLAN_TYPE = (
    ("STANDARD", "STANDARD"),
    ("DELUXE", "DELUXE"),
    ("SUPER DELUXE", "SUPER DELUXE"),
    ("STUDIO", "STUDIO"),
    ("DOUBLE ROOM", "DOUBLE ROOM"),
    ("TRIPPLE ROOM", "TRIPPLE ROOM"),
    ("QUAD ROOM", "QUAD ROOM"),
    ("KING ROOM", "KING ROOM"),
    ("QUEEN ROOM", "QUEEN ROOM"),
    ("TWIN ROOM", "TWIN ROOM"),
    ("FAMILY ROOM", "FAMILY ROOM"),
    ("PRESIDENTIAL SUITE", "PRESIDENTIAL SUITE"),
    ("EMPEROR SUITE", "EMPEROR SUITE"),
)


class ExperiencesIncluded(models.Model):
    stay = models.ForeignKey(
        "Stays", on_delete=models.CASCADE, related_name="experiences_included"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Experience Included"
        verbose_name_plural = "Experiences Included"


class Facts(models.Model):
    stay = models.ForeignKey("Stays", on_delete=models.CASCADE, related_name="facts")
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Fact"
        verbose_name_plural = "Facts"


class Inclusions(models.Model):
    stay = models.ForeignKey(
        "Stays", on_delete=models.CASCADE, related_name="inclusions"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Inclusion"
        verbose_name_plural = "Inclusions"


class Stays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(
        max_length=100,
        help_text="If no name, enter a short description of the "
        + "accommodation. Eg A lovely place located at the lake side",
        verbose_name="Name or description",
    )
    type_of_stay = models.CharField(max_length=100, choices=TYPE_OF_STAY, blank=True)

    # experiences_included = ArrayField(
    #     models.CharField(max_length=500, blank=True, null=True),
    #     blank=True,
    #     null=True,
    #     default=list,
    #     help_text="Separate all experiences included in this package by using ' , '. If the text includes a comma, then place it in a single quote Eg Camping, Fishing, Hiking",
    # )
    # # work on this in the frontend
    # facts = ArrayField(
    #     models.CharField(max_length=500, blank=True, null=True),
    #     blank=True,
    #     null=True,
    #     default=list,
    #     help_text="Separate all experiences included in this package by using ' , '. If the text includes a comma, then place it in a single quote",
    # )
    # # work on this in the frontend
    # included = ArrayField(
    #     models.CharField(max_length=500, blank=True, null=True),
    #     blank=True,
    #     null=True,
    #     default=list,
    #     help_text="Separate each by using ' , '. If the text includes a comma, then place it in a single quote. Eg Pool",
    # )

    # Lodge
    tented_camp = models.BooleanField(default=False)
    permanent_structures = models.BooleanField(default=False)
    part_permanent_structures = models.BooleanField(default=False)
    mobile_camp = models.BooleanField(default=False)

    # House
    residential_home = models.BooleanField(default=False)
    villa = models.BooleanField(default=False)
    boathouse = models.BooleanField(default=False)
    historical_building = models.BooleanField(default=False)
    on_private_property = models.BooleanField(default=False)
    cabin = models.BooleanField(default=False)
    cottage = models.BooleanField(default=False)
    chalets = models.BooleanField(default=False)
    bungalow = models.BooleanField(default=False)
    tiny_house = models.BooleanField(default=False)
    duplex = models.BooleanField(default=False)
    earth_house = models.BooleanField(default=False)
    container_house = models.BooleanField(default=False)
    terrace_house = models.BooleanField(default=False)

    # Unique Space
    bus = models.BooleanField(default=False)
    lighthouse = models.BooleanField(default=False)
    glasshouse = models.BooleanField(default=False)
    treehouse = models.BooleanField(default=False)
    barn = models.BooleanField(default=False)
    grasshouse = models.BooleanField(default=False)

    # Campsite
    in_conservancy = models.BooleanField(default=False)
    in_national_park = models.BooleanField(default=False)
    in_nature_reserve = models.BooleanField(default=False)
    in_public_area = models.BooleanField(default=False)

    # Boutique Hotel
    a_hotel_out_in_nature = models.BooleanField(default=False)
    resort = models.BooleanField(default=False)
    unique_achitectural_design = models.BooleanField(default=False)

    # Amenities
    swimming_pool = models.BooleanField(default=False)
    hot_tub = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    patio = models.BooleanField(default=False)
    beachfront = models.BooleanField(default=False)
    terrace = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    firepit = models.BooleanField(default=False)
    barbecue_grill = models.BooleanField(default=False)
    outdoor_dining_area = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    fridge = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    washing_machine = models.BooleanField(default=False)
    dedicated_working_area = models.BooleanField(default=False)
    smoke_alarm = models.BooleanField(default=False)
    first_aid_kit = models.BooleanField(default=False)
    medical_service_on_site = models.BooleanField(default=False)
    carbon_monoxide_detector = models.BooleanField(default=False)
    lockable_room = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    giftshop = models.BooleanField(default=False)
    photography_room = models.BooleanField(default=False)
    themed_room = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    # work on this in the frontend
    barber_shop = models.BooleanField(default=False)
    beauty_salon = models.BooleanField(default=False)
    ensuite_room = models.BooleanField(default=False)
    purified_drinking_water = models.BooleanField(default=False)
    firewood = models.BooleanField(default=False)
    conference_center = models.BooleanField(default=False)
    library = models.BooleanField(default=False)

    # work on this in the frontend
    other_amenities = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each amenities by using ' , '",
    )

    # Policies
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    refundable = models.BooleanField(default=False)
    refund_policy = models.TextField(blank=True, null=True)
    damage_policy = models.TextField(blank=True, null=True)
    children_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    events_allowed = models.BooleanField(default=False)
    covid_19_compliance = models.BooleanField(default=False)
    covid_19_compliance_details = models.TextField(blank=True, null=True)

    cancellation_policy = models.TextField(blank=True, null=True)
    cancellation_policy_by_provider = models.TextField(blank=True, null=True)
    health_and_safety_policy = models.TextField(blank=True, null=True)
    damage_policy_by_provider = models.TextField(blank=True, null=True)

    location = models.CharField(
        max_length=350, blank=True, null=True, verbose_name="Address"
    )
    city = models.CharField(max_length=350, blank=True, null=True)
    country = models.CharField(max_length=350, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)

    super_deluxe = models.BooleanField(default=False)
    super_deluxe_capacity = models.IntegerField(blank=True, null=True)
    super_deluxe_price = models.FloatField(blank=True, null=True)
    super_deluxe_price_non_resident = models.FloatField(blank=True, null=True)
    super_deluxe_children_price = models.FloatField(blank=True, null=True)
    super_deluxe_children_price_non_resident = models.FloatField(blank=True, null=True)
    super_deluxe_teen_price = models.FloatField(blank=True, null=True)
    super_deluxe_teen_price_non_resident = models.FloatField(blank=True, null=True)
    super_deluxe_single_price = models.FloatField(blank=True, null=True)
    super_deluxe_single_price_non_resident = models.FloatField(blank=True, null=True)
    super_deluxe_single_child_price = models.FloatField(blank=True, null=True)
    super_deluxe_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    super_deluxe_single_teen_price = models.FloatField(blank=True, null=True)
    super_deluxe_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    deluxe = models.BooleanField(default=False)
    deluxe_capacity = models.IntegerField(blank=True, null=True)
    deluxe_price = models.FloatField(blank=True, null=True)
    deluxe_price_non_resident = models.FloatField(blank=True, null=True)
    deluxe_children_price = models.FloatField(blank=True, null=True)
    deluxe_children_price_non_resident = models.FloatField(blank=True, null=True)
    deluxe_teen_price = models.FloatField(blank=True, null=True)
    deluxe_teen_price_non_resident = models.FloatField(blank=True, null=True)
    deluxe_single_price = models.FloatField(blank=True, null=True)
    deluxe_single_price_non_resident = models.FloatField(blank=True, null=True)
    deluxe_single_child_price = models.FloatField(blank=True, null=True)
    deluxe_single_child_price_non_resident = models.FloatField(blank=True, null=True)
    deluxe_single_teen_price = models.FloatField(blank=True, null=True)
    deluxe_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    standard = models.BooleanField(default=True)
    standard_capacity = models.IntegerField(default=2)
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)
    children_price = models.FloatField(blank=True, null=True)
    children_price_non_resident = models.FloatField(blank=True, null=True)
    teen_price = models.FloatField(blank=True, null=True)
    teen_price_non_resident = models.FloatField(blank=True, null=True)
    single_price = models.FloatField(blank=True, null=True)
    single_price_non_resident = models.FloatField(blank=True, null=True)
    single_child_price = models.FloatField(blank=True, null=True)
    single_child_price_non_resident = models.FloatField(blank=True, null=True)
    single_teen_price = models.FloatField(blank=True, null=True)
    single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    studio = models.BooleanField(default=False)
    studio_capacity = models.IntegerField(blank=True, null=True)
    studio_price = models.FloatField(blank=True, null=True)
    studio_price_non_resident = models.FloatField(blank=True, null=True)
    studio_children_price = models.FloatField(blank=True, null=True)
    studio_children_price_non_resident = models.FloatField(blank=True, null=True)
    studio_teen_price = models.FloatField(blank=True, null=True)
    studio_teen_price_non_resident = models.FloatField(blank=True, null=True)
    studio_single_price = models.FloatField(blank=True, null=True)
    studio_single_price_non_resident = models.FloatField(blank=True, null=True)
    studio_single_child_price = models.FloatField(blank=True, null=True)
    studio_single_child_price_non_resident = models.FloatField(blank=True, null=True)
    studio_single_teen_price = models.FloatField(blank=True, null=True)
    studio_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    double_room = models.BooleanField(default=False)
    double_room_capacity = models.IntegerField(blank=True, null=True)
    double_room_price = models.FloatField(blank=True, null=True)
    double_room_price_non_resident = models.FloatField(blank=True, null=True)
    double_room_children_price = models.FloatField(blank=True, null=True)
    double_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    double_room_teen_price = models.FloatField(blank=True, null=True)
    double_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    double_room_single_price = models.FloatField(blank=True, null=True)
    double_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    double_room_single_child_price = models.FloatField(blank=True, null=True)
    double_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    double_room_single_teen_price = models.FloatField(blank=True, null=True)
    double_room_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    tripple_room = models.BooleanField(default=False)
    tripple_room_capacity = models.IntegerField(blank=True, null=True)
    tripple_room_price = models.FloatField(blank=True, null=True)
    tripple_room_price_non_resident = models.FloatField(blank=True, null=True)
    tripple_room_children_price = models.FloatField(blank=True, null=True)
    tripple_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    tripple_room_teen_price = models.FloatField(blank=True, null=True)
    tripple_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    tripple_room_single_price = models.FloatField(blank=True, null=True)
    tripple_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    tripple_room_single_child_price = models.FloatField(blank=True, null=True)
    tripple_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    tripple_room_single_teen_price = models.FloatField(blank=True, null=True)
    tripple_room_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    quad_room = models.BooleanField(default=False)
    quad_room_capacity = models.IntegerField(blank=True, null=True)
    quad_room_price = models.FloatField(blank=True, null=True)
    quad_room_price_non_resident = models.FloatField(blank=True, null=True)
    quad_room_children_price = models.FloatField(blank=True, null=True)
    quad_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    quad_room_teen_price = models.FloatField(blank=True, null=True)
    quad_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    quad_room_single_price = models.FloatField(blank=True, null=True)
    quad_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    quad_room_single_child_price = models.FloatField(blank=True, null=True)
    quad_room_single_child_price_non_resident = models.FloatField(blank=True, null=True)
    quad_room_single_teen_price = models.FloatField(blank=True, null=True)
    quad_room_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    queen_room = models.BooleanField(default=False)
    queen_room_capacity = models.IntegerField(blank=True, null=True)
    queen_room_price = models.FloatField(blank=True, null=True)
    queen_room_price_non_resident = models.FloatField(blank=True, null=True)
    queen_room_children_price = models.FloatField(blank=True, null=True)
    queen_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    queen_room_teen_price = models.FloatField(blank=True, null=True)
    queen_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    queen_room_single_price = models.FloatField(blank=True, null=True)
    queen_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    queen_room_single_child_price = models.FloatField(blank=True, null=True)
    queen_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    queen_room_single_teen_price = models.FloatField(blank=True, null=True)
    queen_room_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    king_room = models.BooleanField(default=False)
    king_room_capacity = models.IntegerField(blank=True, null=True)
    king_room_price = models.FloatField(blank=True, null=True)
    king_room_price_non_resident = models.FloatField(blank=True, null=True)
    king_room_children_price = models.FloatField(blank=True, null=True)
    king_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    king_room_teen_price = models.FloatField(blank=True, null=True)
    king_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    king_room_single_price = models.FloatField(blank=True, null=True)
    king_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    king_room_single_child_price = models.FloatField(blank=True, null=True)
    king_room_single_child_price_non_resident = models.FloatField(blank=True, null=True)
    king_room_single_teen_price = models.FloatField(blank=True, null=True)
    king_room_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    twin_room = models.BooleanField(default=False)
    twin_room_capacity = models.IntegerField(blank=True, null=True)
    twin_room_price = models.FloatField(blank=True, null=True)
    twin_room_price_non_resident = models.FloatField(blank=True, null=True)
    twin_room_children_price = models.FloatField(blank=True, null=True)
    twin_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    twin_room_teen_price = models.FloatField(blank=True, null=True)
    twin_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    twin_room_single_price = models.FloatField(blank=True, null=True)
    twin_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    twin_room_single_child_price = models.FloatField(blank=True, null=True)
    twin_room_single_child_price_non_resident = models.FloatField(blank=True, null=True)
    twin_room_single_teen_price = models.FloatField(blank=True, null=True)
    twin_room_single_teen_price_non_resident = models.FloatField(blank=True, null=True)

    family_room = models.BooleanField(default=False)
    family_room_capacity = models.IntegerField(blank=True, null=True)
    family_room_price = models.FloatField(blank=True, null=True)
    family_room_price_non_resident = models.FloatField(blank=True, null=True)
    family_room_children_price = models.FloatField(blank=True, null=True)
    family_room_children_price_non_resident = models.FloatField(blank=True, null=True)
    family_room_teen_price = models.FloatField(blank=True, null=True)
    family_room_teen_price_non_resident = models.FloatField(blank=True, null=True)
    family_room_single_price = models.FloatField(blank=True, null=True)
    family_room_single_price_non_resident = models.FloatField(blank=True, null=True)
    family_room_single_child_price = models.FloatField(blank=True, null=True)
    family_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    family_room_single_teen_price = models.FloatField(blank=True, null=True)
    family_room_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    presidential_suite_room = models.BooleanField(default=False)
    presidential_suite_room_capacity = models.IntegerField(blank=True, null=True)
    presidential_suite_room_price = models.FloatField(blank=True, null=True)
    presidential_suite_room_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_children_price = models.FloatField(blank=True, null=True)
    presidential_suite_room_children_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_teen_price = models.FloatField(blank=True, null=True)
    presidential_suite_room_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_single_price = models.FloatField(blank=True, null=True)
    presidential_suite_room_single_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_single_child_price = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    presidential_suite_room_single_teen_price = models.FloatField(blank=True, null=True)
    presidential_suite_room_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    emperor_suite_room = models.BooleanField(default=False)
    emperor_suite_room_capacity = models.IntegerField(blank=True, null=True)
    emperor_suite_room_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_price_non_resident = models.FloatField(blank=True, null=True)
    emperor_suite_room_children_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_children_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    emperor_suite_room_teen_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    emperor_suite_room_single_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_single_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    emperor_suite_room_single_child_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    emperor_suite_room_single_teen_price = models.FloatField(blank=True, null=True)
    emperor_suite_room_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    pricing_type = models.CharField(
        max_length=100, choices=PRICING_TYPE, default="REASONABLE"
    )

    contact_name = models.CharField(max_length=250, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = PhoneNumberField(blank=True)
    company = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    description = models.TextField(blank=True, null=True)
    unique_about_place = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user} - {self.name}"

    class Meta:
        verbose_name = "Stay"


class StayImage(models.Model):
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="stay_images"
    )
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(StayImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(StayImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.stay.user} - {self.stay.name}"


class Views(models.Model):
    user_ip = models.TextField(default=None)
    stay = models.ForeignKey(Stays, related_name="views", on_delete=models.CASCADE)

    def __str__(self):
        return f"{ self.stay.user }"

    class Meta:
        verbose_name = "Stay Views"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="cart")
    from_date = models.DateTimeField(default=timezone.now)
    plan = models.CharField(max_length=100, choices=PLAN_TYPE, default="STANDARD")
    to_date = models.DateTimeField(blank=True, null=True)
    non_resident = models.BooleanField(default=False)
    num_of_adults = models.IntegerField(default=1)
    num_of_children = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stay.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    stay = models.ForeignKey(
        Stays, on_delete=models.SET_NULL, blank=True, null=True, related_name="order"
    )

    from_date = models.DateTimeField(default=timezone.now)
    non_resident = models.BooleanField(default=False)
    to_date = models.DateTimeField(blank=True, null=True)
    num_of_adults = models.IntegerField(default=1)
    num_of_children = models.IntegerField(default=0)
    plan = models.CharField(max_length=100, choices=PLAN_TYPE, default="STANDARD")
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.user}"


class Review(models.Model):
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.rate) + " - " + str(self.title)


class SaveStays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="saved_stays"
    )

    def __str__(self):
        return str(self.stay)
