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
from django.contrib.sessions.models import Session
from activities.models import Activities
from core.utils import (
    lodge_image_thumbnail,
    activity_fees_image_thumbnail,
    lodge_price_data_file,
)
from django.utils import timezone
from django.core.validators import FileExtensionValidator
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

FEE_GUEST_OPTIONS = (
    ("ADULT", "ADULT"),
    ("CHILD", "CHILD"),
    ("INFANT", "INFANT"),
)

GUEST_OPTIONS = (
    ("ADULT SINGLE", "ADULT SINGLE"),
    ("ADULT DOUBLE", "ADULT DOUBLE"),
    ("ADULT TRIPLE", "ADULT TRIPLE"),
    ("CHILD SINGLE", "CHILD SINGLE"),
    ("CHILD DOUBLE", "CHILD DOUBLE"),
    ("CHILD TRIPLE", "CHILD TRIPLE"),
    ("INFANT", "INFANT"),
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


FEE_OPTIONS = (
    ("PER PERSON", "PER PERSON"),
    ("PER PERSON PER NIGHT", "PER PERSON PER NIGHT"),
    ("WHOLE GROUP", "WHOLE GROUP"),
)


PACKAGE = (
    ("ALL INCLUSIVE", "ALL INCLUSIVE"),
    ("GAME PACKAGE", "GAME PACKAGE"),
    ("FULL BOARD", "FULL BOARD"),
    ("HALF BOARD", "HALF BOARD"),
    ("BED AND BREAKFAST", "BED AND BREAKFAST"),
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
        blank=True,
        null=True,
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
    sheety_url = models.URLField(max_length=500, blank=True, null=True)

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

    pricing_type = models.CharField(
        max_length=100,
        choices=PRICING_TYPE,
        default="REASONABLE",
        blank=True,
        null=True,
    )

    contact_name = models.CharField(max_length=250, blank=True, null=True)
    contact_email = models.EmailField(max_length=250, blank=True, null=True)
    contact_emails = ArrayField(
        models.EmailField(max_length=250, blank=True, null=True),
        default=list,
        help_text="Add multiple emails separated by comma",
    )
    contact_phone = PhoneNumberField(blank=True)
    company = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=False)

    is_an_event = models.BooleanField(default=False)
    is_kaleidoscope_event = models.BooleanField(default=False)
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
    lodge_price_data_pdf = models.FileField(
        upload_to=lodge_price_data_file,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    # review
    user_added_to_calculate = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="user_added_to_calculate"
    )
    annonymous_added_to_calculate = models.ManyToManyField(
        Session, blank=True, related_name="annonymous_added_to_calculate"
    )
    in_homepage = models.BooleanField(default=False)
    has_options = models.BooleanField(default=False)
    is_partner_property = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.property_name} - {self.name}"

    class Meta:
        verbose_name = "Stay"
        verbose_name_plural = "Stays"


class PrivateSafari(models.Model):
    stay = models.OneToOneField(
        Stays, on_delete=models.CASCADE, related_name="private_safari"
    )
    price = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "Full Board"
        verbose_name_plural = "Full Boards"


class SharedSafari(models.Model):
    stay = models.OneToOneField(
        Stays, on_delete=models.CASCADE, related_name="shared_safari"
    )
    price = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "Game Package"
        verbose_name_plural = "Game Packages"


class AllInclusive(models.Model):
    stay = models.OneToOneField(
        Stays, on_delete=models.CASCADE, related_name="all_inclusive"
    )
    price = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "All Inclusive"
        verbose_name_plural = "All Inclusive"


class OtherOption(models.Model):
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="other_options"
    )
    price = models.FloatField(blank=True, null=True)
    available = models.BooleanField(default=False)
    title = models.CharField(max_length=120, blank=True, null=True)
    about = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.stay.name} - {self.id}"

    class Meta:
        verbose_name = "Other Option"
        verbose_name_plural = "Other Options"


class PrivateSafariImages(models.Model):
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    private_safari = models.ForeignKey(
        PrivateSafari, on_delete=models.CASCADE, related_name="private_safari_images"
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.private_safari.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "Full Board Image"
        verbose_name_plural = "Full Board Images"


class SharedSafariImages(models.Model):
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    shared_safari = models.ForeignKey(
        SharedSafari, on_delete=models.CASCADE, related_name="shared_safari_images"
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.shared_safari.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "Game Package Image"
        verbose_name_plural = "Game Package Images"


class AllInclusiveImages(models.Model):
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    all_inclusive = models.ForeignKey(
        AllInclusive, on_delete=models.CASCADE, related_name="all_inclusive_images"
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.all_inclusive.stay.name} - {self.id}"

    # rather than changing the name of the model, we can change the name of the model in the admin
    class Meta:
        verbose_name = "All Inclusive Image"
        verbose_name_plural = "All Inclusive Images"


class OtherOptionImages(models.Model):
    image = ProcessedImageField(
        upload_to=lodge_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    other_option = models.ForeignKey(
        OtherOption, on_delete=models.CASCADE, related_name="other_option_images"
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.other_option.stay.name} - {self.id}"

    class Meta:
        verbose_name = "Other Option Image"
        verbose_name_plural = "Other Option Images"


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


class LodgePackageBooking(models.Model):
    stay = models.ForeignKey(
        Stays,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lodge_package_order",
    )
    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    type_of_package = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False, verbose_name="payment confirmed")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Lodge package booking"
        verbose_name_plural = "Lodge package bookings"


class LodgePackageBookingInstallment(models.Model):
    stay = models.ForeignKey(
        Stays,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lodge_package_order_installment",
    )
    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    type_of_package = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    paid_installment_1 = models.BooleanField(
        default=False, verbose_name="payment confirmed for installment 1"
    )
    paid_installment_2 = models.BooleanField(
        default=False, verbose_name="payment confirmed for installment 2"
    )
    paid_installment_3 = models.BooleanField(
        default=False, verbose_name="payment confirmed for installment 3"
    )
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order by {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Lodge package booking Installment"
        verbose_name_plural = "Lodge package bookings Installment"


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


class RoomType(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="room_types")
    name = models.CharField(max_length=120, blank=True, null=True)
    capacity = models.IntegerField(default=0)
    child_capacity = models.IntegerField(default=0)
    infant_capacity = models.IntegerField(default=0)
    package = models.CharField(max_length=120, default="ALL INCLUSIVE")
    package_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Room type"
        verbose_name_plural = "Room types"


class Bookings(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="bookings"
    )
    num_of_rooms = models.IntegerField(default=0)
    num_of_guests = models.IntegerField(default=0)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    check_in_date = models.DateField(default=timezone.now)
    check_out_date = models.DateField(default=timezone.now)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.full_name)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class RoomAvailability(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room_availabilities"
    )
    num_of_available_rooms = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Room availability"
        verbose_name_plural = "Room availabilities"


class RoomAvailabilityResident(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room_resident_availabilities"
    )
    num_of_available_rooms = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Room availability Resident"
        verbose_name_plural = "Room availabilities Resident"


class ResidentOtherFees(models.Model):
    room_availability_resident = models.ForeignKey(
        RoomAvailabilityResident,
        on_delete=models.CASCADE,
        related_name="resident_other_fees",
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Resident Other Fees"
        verbose_name_plural = "Resident Other Fees"


class RoomAvailabilityResidentGuest(models.Model):
    room_availability_resident = models.ForeignKey(
        RoomAvailabilityResident,
        on_delete=models.CASCADE,
        related_name="room_resident_guest_availabilities",
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    season = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    age_group = models.CharField(max_length=120, blank=True, null=True)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Room availability Resident Guest"
        verbose_name_plural = "Room availabilities Resident Guest"


class RoomAvailabilityNonResident(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name="room_non_resident_availabilities",
    )
    num_of_available_rooms = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Room availability Non-Resident"
        verbose_name_plural = "Room availabilities Non-Resident"


class ParkFees(models.Model):
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="park_fees")
    name = models.CharField(max_length=120, blank=True, null=True)
    resident_adult_price = models.FloatField(default=0)
    resident_child_price = models.FloatField(default=0)
    resident_teen_price = models.FloatField(default=0)
    non_resident_adult_price = models.FloatField(default=0)
    non_resident_child_price = models.FloatField(default=0)
    non_resident_teen_price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Park Fees"
        verbose_name_plural = "Park Fees"


class OtherFeesResident(models.Model):
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="other_fees_resident"
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    adult_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    teen_price = models.FloatField(default=0)

    price = models.FloatField(default=0)
    # resident_fee_type = models.CharField(
    #     max_length=120, choices=FEE_OPTIONS, blank=True, null=True, default="PER PERSON"
    # )
    # guest_type = models.CharField(
    #     max_length=120,
    #     choices=FEE_GUEST_OPTIONS,
    #     blank=True,
    #     null=True,
    #     default="ADULT",
    # )

    class Meta:
        verbose_name = "Resident Other Fees"
        verbose_name_plural = "Resident Other Fees"


class ActivityFee(models.Model):
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="activity_fees"
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0, help_text="for non-resident")
    resident_price = models.FloatField(default=0, help_text="for resident")
    image = ProcessedImageField(
        upload_to=activity_fees_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        blank=True,
        options={"quality": 60},
    )
    price_type = models.CharField(
        max_length=120, choices=FEE_OPTIONS, blank=True, null=True, default="PER PERSON"
    )

    def __str__(self):
        return str(self.name) + " - " + str(self.stay.property_name)

    class Meta:
        verbose_name = "Activity Fee"
        verbose_name_plural = "Activity Fees"


class OtherFeesNonResident(models.Model):
    stay = models.ForeignKey(
        Stays, on_delete=models.CASCADE, related_name="other_fees_non_resident"
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    adult_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    teen_price = models.FloatField(default=0)

    price = models.FloatField(default=0)
    # nonresident_fee_type = models.CharField(
    #     max_length=120, choices=FEE_OPTIONS, blank=True, null=True, default="PER PERSON"
    # )
    # guest_type = models.CharField(
    #     max_length=120,
    #     choices=FEE_GUEST_OPTIONS,
    #     blank=True,
    #     null=True,
    #     default="ADULT",
    # )

    class Meta:
        verbose_name = "Non-Resident Other Fees"
        verbose_name_plural = "Non-Resident Other Fees"


class NonResidentOtherFees(models.Model):
    room_availability_non_resident = models.ForeignKey(
        RoomAvailabilityNonResident,
        on_delete=models.CASCADE,
        related_name="non_resident_other_fees",
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Non-Resident Other Fees"
        verbose_name_plural = "Non-Resident Other Fees"


class RoomAvailabilityNonResidentGuest(models.Model):
    room_availability_non_resident = models.ForeignKey(
        RoomAvailabilityNonResident,
        on_delete=models.CASCADE,
        related_name="room_non_resident_guest_availabilities",
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    season = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    age_group = models.CharField(max_length=120, blank=True, null=True)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Room availability Non-Resident Guest"
        verbose_name_plural = "Room availabilities Non-Resident Guest"
