from asyncio import transports
from dbm.ndbm import library
from email import message
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

TRANSPORT_OPTIONS = ((0, "No Transport"), (1, "Car"), (2, "Bus"))

ROOM_IS_ENSUITE = (("YES", "YES"), ("NO", "NO"))

PRICING_TYPE = (
    ("REASONABLE", "REASONABLE"),
    ("MID-RANGE", "MID-RANGE"),
    ("HIGH-END", "HIGH-END"),
)

TYPE_OF_STAY = (
    ("TENTED CAMP", "TENTED CAMP"),
    ("LODGE", "LODGE"),
    ("HOUSE", "HOUSE"),  #
    ("CAMPSITE", "CAMPSITE"),
    ("WEEKEND GETAWAY", "WEEKEND GETAWAY"),
    ("ROMANTIC GETAWAY", "ROMANTIC GETAWAY"),
    ("GROUP GETAWAY", "GROUP GETAWAY"),
    ("CONSERVANCY", "CONSERVANCY"),
    ("FARMSTAY", "FARMSTAY"),
    ("NATIONAL PARK/GAME RESERVES", "NATIONAL PARK/GAME RESERVES"),
    ("LAKEFRONT", "LAKEFRONT"),
    ("BEACHFRONT", "BEACHFRONT"),
    ("LUXURIOUS", "LUXURIOUS"),
    ("BEAUTIFUL VIEW", "BEAUTIFUL VIEW"),
    ("OFF-GRID", "OFF-GRID"),
    ("ECO-STAY", "ECO-STAY"),
    ("QUIRKY", "QUIRKY"),
    ("HONEYMOON SPOT", "HONEYMOON SPOT"),
    ("UNIQUE EXPERIENCES", "UNIQUE EXPERIENCES"),
    ("TRADITIONAL", "TRADITIONAL"),
    ("MANSION", "MANSION"),
    ("OVER-WATER", "OVER-WATER"),
    ("STUNNING ARCHITECTURE", "STUNNING ARCHITECTURE"),
    ("RIVERFRONT", "RIVERFRONT"),
    ("PRIVATE HOUSE", "PRIVATE HOUSE"),
    ("RESORT", "RESORT"),
    ("BOUTIQUE HOTEL", "BOUTIQUE HOTEL"),
    ("UNIQUE SPACE", "UNIQUE SPACE"),  #
    ("UNIQUE LOCATION", "UNIQUE LOCATION"),
    ("HOTEL", "HOTEL"),
    ("COTTAGE", "COTTAGE"),
    ("COWORKING SPOT", "COWORKING SPOT"),
    ("SWIMMING POOL", "SWIMMING POOL"),
    ("LOCALLY OWNED", "LOCALLY OWNED"),
    ("COMMUNITY OWNED", "COMMUNITY OWNED"),
    ("CARBON NEUTRAL", "CARBON NEUTRAL"),
    ("OWNER OPERATED", "OWNER OPERATED"),
    ("POPULAR", "POPULAR"),
    ("WELLNESS RETREAT", "WELLNESS RETREAT"),
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
    ("EXECUTIVE SUITE ROOM", "EXECUTIVE SUITE ROOM"),
    ("FAMILY ROOM", "FAMILY ROOM"),
    ("PRESIDENTIAL SUITE ROOM", "PRESIDENTIAL SUITE ROOM"),
    ("EMPEROR SUITE ROOM", "EMPEROR SUITE ROOM"),
)


class ExtrasIncluded(models.Model):
    stay = models.ForeignKey(
        "Stays", on_delete=models.CASCADE, related_name="extras_included"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Extra"
        verbose_name_plural = "Extras"


class Facts(models.Model):
    stay = models.ForeignKey("Stays", on_delete=models.CASCADE, related_name="facts")
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Amenties(Quick Fact)"
        verbose_name_plural = "Amenties(Quick Facts)"


class Inclusions(models.Model):
    stay = models.ForeignKey(
        "Stays", on_delete=models.CASCADE, related_name="inclusions"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.stay.name)

    class Meta:
        verbose_name = "Included Activity"
        verbose_name_plural = "Included Activities"


class Stays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(
        max_length=500,
        help_text="If no name, enter a short description of the "
        + "accommodation. Eg A lovely place located at the lake side",
        verbose_name="Name or description",
    )
    property_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    room_type = models.CharField(max_length=100, blank=True)
    type_of_stay = models.CharField(max_length=100, choices=TYPE_OF_STAY, blank=True)
    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Separate each tag by using ' , '",
    )

    # Best describe the stay
    tented_camp = models.BooleanField(default=False)
    lodge = models.BooleanField(default=False)
    house = models.BooleanField(default=False)
    campsite = models.BooleanField(default=False)
    weekend_getaway = models.BooleanField(default=False)
    romantic_getaway = models.BooleanField(default=False)
    group_getaway = models.BooleanField(default=False)
    conservancy = models.BooleanField(default=False)
    farmstay = models.BooleanField(default=False)
    national_park_game_reserves = models.BooleanField(default=False)
    lakefront = models.BooleanField(default=False)
    beachfront = models.BooleanField(default=False)
    luxurious = models.BooleanField(default=False)
    beautiful_view = models.BooleanField(default=False)
    off_grid = models.BooleanField(default=False)
    eco_stay = models.BooleanField(default=False)
    quirky = models.BooleanField(default=False)
    honeymoon_spot = models.BooleanField(default=False)
    unique_experiences = models.BooleanField(default=False)
    traditional = models.BooleanField(default=False)
    mansion = models.BooleanField(default=False)
    over_water = models.BooleanField(default=False)
    stunning_architecture = models.BooleanField(default=False)
    riverfront = models.BooleanField(default=False)
    private_house = models.BooleanField(default=False)
    resort = models.BooleanField(default=False)
    boutique_hotel = models.BooleanField(default=False)
    unique_space = models.BooleanField(default=False)
    unique_location = models.BooleanField(default=False)
    hotel = models.BooleanField(default=False)
    cottage = models.BooleanField(default=False)
    coworking_spot = models.BooleanField(default=False)
    fast_wifi = models.BooleanField(default=False)
    locally_owned = models.BooleanField(default=False)
    community_owned = models.BooleanField(default=False)
    carbon_neutral = models.BooleanField(default=False)
    owner_operated = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    wellness_retreat = models.BooleanField(default=False)

    # Amenities
    swimming_pool = models.BooleanField(default=False)
    hot_tub = models.BooleanField(default=False)
    sauna = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    patio = models.BooleanField(default=False)
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
    city = models.CharField(
        max_length=350, blank=True, null=True, verbose_name="county"
    )
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

    per_house = models.BooleanField(default=False)
    per_house_price = models.FloatField(blank=True, null=True)

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

    conservation_or_park = models.BooleanField(default=False)
    conservation_or_park_capacity = models.IntegerField(blank=True, null=True)
    conservation_or_park_price = models.FloatField(blank=True, null=True)
    conservation_or_park_price_non_resident = models.FloatField(blank=True, null=True)
    conservation_or_park_children_price = models.FloatField(blank=True, null=True)
    conservation_or_park_children_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    conservation_or_park_teen_price = models.FloatField(blank=True, null=True)
    conservation_or_park_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    conservation_or_park_single_price = models.FloatField(blank=True, null=True)
    conservation_or_park_single_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    conservation_or_park_single_child_price = models.FloatField(blank=True, null=True)
    conservation_or_park_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    conservation_or_park_single_teen_price = models.FloatField(blank=True, null=True)
    conservation_or_park_single_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )

    executive_suite_room = models.BooleanField(default=False)
    executive_suite_room_capacity = models.IntegerField(blank=True, null=True)
    executive_suite_room_price = models.FloatField(blank=True, null=True)
    executive_suite_room_price_non_resident = models.FloatField(blank=True, null=True)
    executive_suite_room_children_price = models.FloatField(blank=True, null=True)
    executive_suite_room_children_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    executive_suite_room_teen_price = models.FloatField(blank=True, null=True)
    executive_suite_room_teen_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    executive_suite_room_single_price = models.FloatField(blank=True, null=True)
    executive_suite_room_single_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    executive_suite_room_single_child_price = models.FloatField(blank=True, null=True)
    executive_suite_room_single_child_price_non_resident = models.FloatField(
        blank=True, null=True
    )
    executive_suite_room_single_teen_price = models.FloatField(blank=True, null=True)
    executive_suite_room_single_teen_price_non_resident = models.FloatField(
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

    is_an_event = models.BooleanField(default=False)
    has_holiday_package = models.BooleanField(default=False)
    has_min_date = models.BooleanField(default=False)
    date_starts_from_ninth = models.BooleanField(default=False)

    car_transfer_price = models.FloatField(
        blank=True,
        null=True,
        help_text="Add if car service is available",
        verbose_name="Van Transfer Price",
    )
    car_transfer_text_location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="Add if car service is available",
        verbose_name="Van Transfer Text Location",
    )
    bus_transfer_price = models.FloatField(
        blank=True, null=True, help_text="Add if bus service is available"
    )
    bus_transfer_text_location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="Add if bus service is available",
        verbose_name="Bus Transfer Text Location",
    )
    distance_from_venue = models.FloatField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    unique_about_place = models.TextField(blank=True, null=True)
    unavailable_dates = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Select the dates you won't be available ' , '",
    )
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.property_name} - {self.name}"

    class Meta:
        verbose_name = "Stay"
        verbose_name_plural = "Stays"


class TypeOfRooms(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="type_of_rooms"
    )
    short_description = models.CharField(max_length=500, blank=True, null=True)
    is_tented_camp = models.BooleanField(default=False)
    price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(blank=True, null=True)
    sleeps = models.IntegerField(blank=True, null=True)
    available_rooms = models.IntegerField(blank=True, null=True)
    is_standard = models.BooleanField(default=False)
    not_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type of Room"
        verbose_name_plural = "Types of Rooms"


class TypeOfRoomsImages(models.Model):
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)
    room = models.ForeignKey(
        TypeOfRooms, on_delete=models.CASCADE, related_name="type_of_room_images"
    )

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "Type of Room Image"
        verbose_name_plural = "Types of Room Images"


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
    # non_resident = models.BooleanField(default=False)
    num_of_adults = models.IntegerField(default=1)
    num_of_children = models.IntegerField(default=0)
    num_of_adults_non_resident = models.IntegerField(default=0)
    num_of_children_non_resident = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stay.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    stay = models.ForeignKey(
        Stays, on_delete=models.SET_NULL, blank=True, null=True, related_name="order"
    )

    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(blank=True, null=True)
    num_of_adults = models.IntegerField(default=1)
    num_of_children = models.IntegerField(default=0)
    num_of_adults_non_resident = models.IntegerField(default=0)
    num_of_children_non_resident = models.IntegerField(default=0)
    reviewing = models.BooleanField(default=True)
    email_sent = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    plan = models.CharField(max_length=100, choices=PLAN_TYPE, default="STANDARD")
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.user}"


class Event(models.Model):
    stay = models.ForeignKey(
        Stays,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="event_order",
    )
    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(blank=True, null=True)
    rooms = models.IntegerField(default=1)
    adults = models.IntegerField(default=2)
    children = models.IntegerField(default=0)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    type_of_room = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    confirmation_code = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    passengers = models.IntegerField(default=0)
    transport = models.CharField(max_length=100, choices=TRANSPORT_OPTIONS, blank=True)
    paid = models.BooleanField(default=False, verbose_name="payment confirmed")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Event booking"
        verbose_name_plural = "Event bookings"


class EventTransport(models.Model):
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    type_of_transport = models.CharField(max_length=300, blank=True, null=True)
    confirmation_code = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    passengers = models.IntegerField(default=0)
    paid = models.BooleanField(default=False, verbose_name="payment confirmed")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Event Transport booking"
        verbose_name_plural = "Event Transport bookings"


class Review(models.Model):
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_posted = models.DateField(default=timezone.now, editable=False)

    def __str__(self):
        return "Rated as " + str(self.rate) + " star - " + str(self.title)


class SaveStays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="saved_stays"
    )

    def __str__(self):
        return str(self.stay)
