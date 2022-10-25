from email.policy import default
from tabnanny import verbose
from django.db import models
from lodging.models import Stays
from transport.models import Transportation
from activities.models import Activities

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.postgres.fields import ArrayField

from django.conf import settings
from django.utils import timezone

from core.utils import trip_image_thumbnail


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
    ("CAR", "CAR"),
    ("BUS", "BUS"),
    ("TRAIN", "TRAIN"),
    ("FLIGHT", "FLIGHT"),
)


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

    pricing_type = models.CharField(
        max_length=100, choices=PRICING_TYPE, default="REASONABLE"
    )
    is_active = models.BooleanField(default=True)
    old_price = models.FloatField(
        blank=True, null=True, help_text="add the previous price(old price)"
    )
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created { self.name } by {self.user}"

    class Meta:
        ordering = ["-created_at"]


# class SimilarTrips(models.Model):
#     curated_trip = models.ManyToManyField(CuratedTrip, related_name="similar_trips")

#     def __str__(self):
#         return f"{self.curated_trip}"

#     class Meta:
#         verbose_name = "Similar Trip"
#         verbose_name_plural = "Similar Trips"


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


class Itinerary(models.Model):
    trip = models.ForeignKey(
        CuratedTrip, on_delete=models.CASCADE, related_name="itineraries"
    )
    day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Select the day of this itinerary",
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.trip} - itinerary {self.day}"

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
        max_length=100, choices=TRANSPORT_TYPE, default="CAR"
    )
    driver_included_in_car = models.BooleanField(
        default=False, help_text="Is a driver included?"
    )
    all_round_trip = models.BooleanField(
        default=False, help_text="Is this an all round trip?"
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
