from django.db import models
from django.conf import settings
from activities.models import *
from core.utils import trip_image_thumbnail
from lodging.models import *
from transport.models import Flight, Transportation
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


PRICING_TYPE = (
    ("REASONABLE", "REASONABLE"),
    ("MID-RANGE", "MID-RANGE"),
    ("HIGH-END", "HIGH-END"),
)


class SingleTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transport = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True, blank=True
    )
    activity = models.ForeignKey(
        Activities, on_delete=models.SET_NULL, null=True, blank=True
    )
    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    area_covered = models.CharField(max_length=350, blank=True, null=True)
    total_number_of_days = models.IntegerField(blank=True, null=True)
    essential_information = models.TextField(blank=True, null=True)
    starting_location = models.CharField(max_length=255, blank=True, null=True)
    ending_location = models.CharField(max_length=255, blank=True, null=True)
    stop_at = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    countries_covered = ArrayField(
        models.CharField(max_length=255), blank=True, null=True
    )
    nights = models.IntegerField(default=3, verbose_name="Number of nights for stay")
    price = models.FloatField(blank=True, null=True)
    price_non_resident = models.FloatField(blank=True, null=True)
    # how_long_is_trip = models.IntegerField(default=3)

    honeymoon = models.BooleanField(default=False)
    cultural = models.BooleanField(default=False)
    weekend_getaway = models.BooleanField(default=False)
    road_trip = models.BooleanField(default=False)
    hiking = models.BooleanField(default=False)
    beach = models.BooleanField(default=False)
    game = models.BooleanField(default=False)
    romantic_getaway = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    cycling = models.BooleanField(default=False)
    lake = models.BooleanField(default=False)
    walking = models.BooleanField(default=False)

    family = models.BooleanField(default=False)
    couples = models.BooleanField(default=False)
    friends = models.BooleanField(default=False)
    caves = models.BooleanField(default=False)
    surfing = models.BooleanField(default=False)
    tropical = models.BooleanField(default=False)
    camping = models.BooleanField(default=False)
    mountain = models.BooleanField(default=False)
    cabin = models.BooleanField(default=False)
    desert = models.BooleanField(default=False)
    treehouse = models.BooleanField(default=False)
    boat = models.BooleanField(default=False)
    creative_space = models.BooleanField(default=False)

    day_game_drives = models.BooleanField(default=False)
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
    all_female = models.BooleanField(default=False)
    families = models.BooleanField(default=False)
    groups = models.BooleanField(default=False)
    luxury = models.BooleanField(default=False)
    budget = models.BooleanField(default=False)
    mid_range = models.BooleanField(default=False)
    beach = models.BooleanField(default=False)
    short_getaways = models.BooleanField(default=False)
    cross_country = models.BooleanField(default=False)
    park_conservancies = models.BooleanField(default=False)

    pricing_type = models.CharField(
        max_length=100, choices=PRICING_TYPE, default="REASONABLE"
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created { self.name } by {self.user}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Curated trip"
        verbose_name_plural = "Curated trips"


class TripHighlight(models.Model):
    trip = models.ForeignKey(
        SingleTrip, on_delete=models.CASCADE, related_name="trip_highlights"
    )
    highlight = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.highlight


class RecommendedMonths(models.Model):
    trip = models.ForeignKey(
        SingleTrip, on_delete=models.CASCADE, related_name="months"
    )
    month = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Format should be a number. It should be between 1 and 12",
    )

    def __str__(self):
        return f"{self.trip} - {self.month}"


class Itinerary(models.Model):
    trip = models.ForeignKey(
        SingleTrip, on_delete=models.CASCADE, related_name="itineraries"
    )
    day = models.CharField(
        max_length=255, blank=True, null=True, help_text="Day of the trip. eg 'Day 1'."
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.trip} - {self.day}"

    class Meta:
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"


class FrequentlyAskedQuestion(models.Model):
    trip = models.ForeignKey(SingleTrip, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.trip} - {self.question}"

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class SingleTripImage(models.Model):
    trip = models.ForeignKey(
        SingleTrip,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="single_trip_images",
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
            super(SingleTripImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(SingleTripImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created by ${self.trip.user}"
