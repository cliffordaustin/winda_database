from email.policy import default
from tabnanny import verbose
from django.db import models
from lodging.models import Stays
from transport.models import Transportation
from activities.models import Activities

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings
from django.utils import timezone

from core.utils import trip_image_thumbnail
from core.utils import generate_random_string
from copy import deepcopy


PRICING_TYPE = (
    ("REASONABLE", "REASONABLE"),
    ("MID-RANGE", "MID-RANGE"),
    ("HIGH-END", "HIGH-END"),
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

TRANSPORT_TYPE = (
    ("CAR HIRE", "CAR HIRE"),
    ("CAR TRANSFER", "CAR TRANSFER"),
    ("BUS TRANSFER", "BUS TRANSFER"),
    ("TRAIN TRANSFER", "TRAIN TRANSFER"),
    ("FLIGHT TRANSFER", "FLIGHT TRANSFER"),
)

PLANS = (("PLAN A", "PLAN A"), ("PLAN B", "PLAN B"), ("PLAN C", "PLAN C"))


class CuratedTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    number_of_countries = models.IntegerField(default=1)
    total_number_of_days = models.IntegerField(blank=True, null=True)
    essential_information = models.TextField(blank=True, null=True)
    local_guide_available = models.BooleanField(default=False)
    max_number_of_people = models.IntegerField(blank=True, null=True)
    trip_is_carbon_neutral = models.BooleanField(default=False)

    # trip categories
    weekend_getaway = models.BooleanField(default=False)
    road_trip = models.BooleanField(default=False)
    cultural = models.BooleanField(default=False)
    lake = models.BooleanField(default=False)
    day_game_drives = models.BooleanField(default=False)
    walking_hiking = models.BooleanField(default=False, verbose_name="Walking/hinking")
    beach = models.BooleanField(default=False)
    family = models.BooleanField(default=False, verbose_name="Families")
    romantic = models.BooleanField(default=False)
    culinary = models.BooleanField(default=False)
    day_trips = models.BooleanField(default=False)
    community_owned = models.BooleanField(default=False)
    off_grid = models.BooleanField(default=False)
    solo_getaway = models.BooleanField(default=False)
    wellness = models.BooleanField(default=False)
    unconventional_safaris = models.BooleanField(default=False)
    shopping = models.BooleanField(default=False)
    art = models.BooleanField(default=False)
    watersports = models.BooleanField(default=False)
    sailing = models.BooleanField(default=False)
    night_game_drives = models.BooleanField(default=False)
    sustainable = models.BooleanField(default=False)
    all_female = models.BooleanField(default=False, verbose_name="All-female")
    groups = models.BooleanField(default=False)
    luxury = models.BooleanField(default=False)
    budget = models.BooleanField(default=False)
    mid_range = models.BooleanField(default=False)
    short_getaways = models.BooleanField(default=False)
    cross_country = models.BooleanField(default=False, verbose_name="Cross-country")
    park_conservancies = models.BooleanField(
        default=False, verbose_name="Park & Conservancies"
    )
    valentine_offer = models.BooleanField(default=False)
    pricing_type = models.CharField(
        max_length=100, choices=PRICING_TYPE, default="REASONABLE"
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duplicate(self):
        obj_copy = deepcopy(self)
        obj_copy.pk = None
        obj_copy.slug = generate_random_string(length=24)
        obj_copy.is_active = False
        obj_copy.save()

        for location in self.locations.all():
            location.pk = None
            location.curated_trip = obj_copy
            location.save()

        for itinerary in self.itineraries.all():
            itinerary_copy = deepcopy(itinerary)
            itinerary_copy.pk = None
            itinerary_copy.trip = obj_copy
            itinerary_copy.save()

            for itinerary_location in itinerary.itinerary_locations.all():
                itinerary_location.pk = None
                itinerary_location.itinerary = itinerary_copy
                itinerary_location.save()

            for itinerary_transport in itinerary.itinerary_transports.all():
                itinerary_transport.pk = None
                itinerary_transport.itinerary = itinerary_copy
                itinerary_transport.save()

            for itinerary_activity in itinerary.itinerary_activities.all():
                itinerary_activity.pk = None
                itinerary_activity.itinerary = itinerary_copy
                itinerary_activity.save()

            for optional_activity in itinerary.optional_activities.all():
                optional_activity.pk = None
                optional_activity.itinerary = itinerary_copy
                optional_activity.save()

            for itinerary_accommodation in itinerary.itinerary_accommodations.all():
                itinerary_accommodation.pk = None
                itinerary_accommodation.itinerary = itinerary_copy
                itinerary_accommodation.save()

        for faq in self.faqs.all():
            faq.pk = None
            faq.trip = obj_copy
            faq.save()

        for curated_trip_image in self.curated_trip_images.all():
            curated_trip_image.pk = None
            curated_trip_image.trip = obj_copy
            curated_trip_image.save()

        self.plan_a_price.pk = None
        self.plan_a_price.trip = obj_copy
        self.plan_a_price.save()

        self.plan_b_price.pk = None
        self.plan_b_price.trip = obj_copy
        self.plan_b_price.save()

        self.plan_c_price.pk = None
        self.plan_c_price.trip = obj_copy
        self.plan_c_price.save()

        obj_copy.save()

    def __str__(self):
        return f"Created { self.name } by {self.user}"

    class Meta:
        ordering = ["-created_at"]


class BookedTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    trip = models.ForeignKey(
        CuratedTrip, on_delete=models.SET_NULL, null=True, blank=True
    )
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    starting_date = models.DateField(default=timezone.now)
    plan = models.CharField(max_length=100, choices=PLANS, default="PLAN A")
    adults = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    booking_request = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booked Trip"
        verbose_name_plural = "Booked Trips"

    def __str__(self):
        return "{}".format(self.trip)


# class SimilarTrips(models.Model):
#     curated_trip = models.ManyToManyField(CuratedTrip, related_name="similar_trips")

#     def __str__(self):
#         return f"{self.curated_trip}"

#     class Meta:
#         verbose_name = "Similar Trip"
#         verbose_name_plural = "Similar Trips"


class RequestInfoOnCustomTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    custom_trip = models.ForeignKey(
        CuratedTrip, on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created { self.first_name } {self.last_name}"

    class Meta:
        verbose_name = "Request Info On Curated Trip"
        verbose_name_plural = "Request Info On Curated Trips"


class CuratedTripLocations(models.Model):
    curated_trip = models.ForeignKey(
        CuratedTrip, on_delete=models.CASCADE, related_name="locations"
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    nights = models.IntegerField(
        blank=True, null=True, help_text="How long will the trip be in this location?"
    )

    def __str__(self):
        return f"{self.curated_trip} - {self.location}"

    class Meta:
        verbose_name = "Curated Trip Location"
        verbose_name_plural = "Curated Trip Locations"


# class DateAndPricing(models.Model):
#     slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
#     trip = models.ForeignKey(
#         CuratedTrip, on_delete=models.CASCADE, related_name="date_and_pricing"
#     )
#     starting_date = models.DateField(
#         blank=True,
#         null=True,
#     )
#     is_not_available = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.trip} - {self.starting_date}"


class PricePlanA(models.Model):
    trip = models.OneToOneField(
        CuratedTrip,
        on_delete=models.CASCADE,
        related_name="plan_a_price",
        null=True,
        blank=True,
    )
    old_price = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name = "Price Plan A"
        verbose_name_plural = "Price Plan A"


class PricePlanB(models.Model):
    trip = models.OneToOneField(
        CuratedTrip,
        on_delete=models.CASCADE,
        related_name="plan_b_price",
        null=True,
        blank=True,
    )
    old_price = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name = "Price Plan B"
        verbose_name_plural = "Price Plan B"


class PricePlanC(models.Model):
    trip = models.OneToOneField(
        CuratedTrip,
        on_delete=models.CASCADE,
        related_name="plan_c_price",
        null=True,
        blank=True,
    )
    old_price = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name = "Price Plan C"
        verbose_name_plural = "Price Plan C"


class Itinerary(models.Model):
    trip = models.ForeignKey(
        CuratedTrip, on_delete=models.CASCADE, related_name="itineraries"
    )
    start_day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Select the start day of this itinerary",
    )
    end_day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Select the end day of this itinerary",
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.trip} - itinerary {self.start_day}"

    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"


class ItineraryLocation(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="itinerary_locations"
    )
    location = models.CharField(
        max_length=200, blank=True, null=True, help_text="Location Name"
    )
    description = models.TextField(blank=True, null=True)


class ItineraryTransport(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="itinerary_transports"
    )
    starting_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="No need to add this if the transport is an all round trip",
    )
    ending_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="No need to add this if the transport is an all round trip",
    )
    transport_type = models.CharField(
        max_length=100, choices=TRANSPORT_TYPE, default="CAR TRANSFER"
    )


class IncludedItineraryActivity(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="itinerary_activities"
    )
    activity = models.ForeignKey(
        Activities, on_delete=models.SET_NULL, null=True, blank=True
    )


class OptionalItineraryActivity(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="optional_activities"
    )
    activity = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Activity Name. price should be added if available. e.g. Hiking - 100 USD",
    )


class ItineraryAccommodation(models.Model):
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="itinerary_accommodations"
    )
    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True, blank=True)
    nights = models.IntegerField(default=1, help_text="Number of nights")


class FrequentlyAskedQuestion(models.Model):
    trip = models.ForeignKey(CuratedTrip, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.trip} - {self.question}"

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class CuratedTripImage(models.Model):
    trip = models.ForeignKey(
        CuratedTrip,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="curated_trip_images",
    )
    image = ProcessedImageField(
        upload_to=trip_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(CuratedTripImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(CuratedTripImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created by ${self.trip.user}"


class TripWizard(models.Model):
    locations = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    month = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    number_of_people = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EbookEmail(models.Model):
    email = models.EmailField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Ebook Email"
        verbose_name_plural = "Ebook Emails"
