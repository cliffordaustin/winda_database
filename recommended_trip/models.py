from django.db import models
from django.conf import settings
from activities.models import *
from core.utils import trip_image_thumbnail
from lodging.models import *
from transport.models import Transportation
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
    description = models.TextField(blank=True, null=True)
    area_covered = models.CharField(max_length=350, blank=True, null=True)
    total_number_of_days = models.IntegerField(blank=True, null=True)
    starting_location = models.CharField(max_length=255, blank=True, null=True)
    ending_location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
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

    pricing_type = models.CharField(
        max_length=100, choices=PRICING_TYPE, default="REASONABLE"
    )
    is_active = models.BooleanField(default=True)

    # stay_num_of_adults = models.IntegerField(default=1)
    # stay_non_resident = models.BooleanField(default=False)
    # stay_num_of_children = models.IntegerField(default=0)
    # stay_plan = models.CharField(max_length=100, choices=PLAN_TYPE, default="STANDARD")
    # number_of_people = models.IntegerField(default=1)
    # user_need_a_driver = models.BooleanField(default=False)
    # nights = models.IntegerField(default=3)

    # activity_non_resident = models.BooleanField(default=False)
    # activity_pricing_type = models.CharField(
    #     max_length=50, choices=PRICING_TYPE, default="PER PERSON"
    # )
    # activity_number_of_people = models.IntegerField(
    #     default=1,
    #     help_text="Set the default number of people coming for this experience. Make sure the experience supports a pricing plan of per person.",
    # )
    # activity_number_of_sessions = models.IntegerField(
    #     default=0,
    #     help_text="Set the default number of sessions for this experience. Make sure the experience supports a pricing plan of per session.",
    # )
    # activity_number_of_groups = models.IntegerField(
    #     default=0,
    #     help_text="Set the default number of group coming for this experience. Make sure the experience supports a pricing plan of per group.",
    # )

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
