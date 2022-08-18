from tabnanny import verbose
from django.db import models
from lodging.models import Stays
from transport.models import Transportation
from activities.models import Activities

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

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


class StayTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(
        "CuratedTrip", on_delete=models.CASCADE, related_name="stay_trip"
    )

    def __str__(self):
        return f"{self.stay.property_name}"


class TransportationTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    transport = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True, blank=True
    )
    trip = models.ForeignKey(
        "CuratedTrip", on_delete=models.CASCADE, related_name="transport_trip"
    )

    def __str__(self):
        return f"{self.transport.vehicle_make} - {self.transport.type_of_car}"


class ActivityTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    activity = models.ForeignKey(
        Activities, on_delete=models.SET_NULL, null=True, blank=True
    )
    trip = models.ForeignKey(
        "CuratedTrip", on_delete=models.CASCADE, related_name="activity_trip"
    )

    def __str__(self):
        return f"{self.activity.name}"


class CuratedTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    area_covered = models.CharField(max_length=350, blank=True, null=True)
    total_number_of_days = models.IntegerField(blank=True, null=True)
    essential_information = models.TextField(blank=True, null=True)
    starting_location = models.CharField(max_length=255, blank=True, null=True)
    ending_location = models.CharField(max_length=255, blank=True, null=True)

    honeymoon = models.BooleanField(default=False)
    cultural = models.BooleanField(default=False)
    weekend_getaway = models.BooleanField(default=False)
    road_trip = models.BooleanField(default=False)
    hiking = models.BooleanField(default=False)
    beach = models.BooleanField(default=False)
    beachfront = models.BooleanField(default=False)
    all_female_owned = models.BooleanField(default=False)
    culinary = models.BooleanField(default=False)
    solo_experience = models.BooleanField(default=False)
    shopping = models.BooleanField(default=False)
    community_owned = models.BooleanField(default=False)
    natural_and_wildlife = models.BooleanField(default=False)
    group_getaway = models.BooleanField(default=False)
    riverside = models.BooleanField(default=False)
    day_trip = models.BooleanField(default=False)
    off_grid = models.BooleanField(default=False)
    beautiful_views = models.BooleanField(default=False)
    quirky = models.BooleanField(default=False)
    conservancies = models.BooleanField(default=False)
    wellness = models.BooleanField(default=False)
    active_adventure = models.BooleanField(default=False)
    game = models.BooleanField(default=False)
    romantic_getaway = models.BooleanField(default=False)
    farmstay = models.BooleanField(default=False)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["-created_at"]


class Itinerary(models.Model):
    trip = models.ForeignKey(
        CuratedTrip, on_delete=models.CASCADE, related_name="itineraries"
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


class UserStayTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(
        "UserTrip", on_delete=models.CASCADE, related_name="user_stay_trip"
    )
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    plan = models.CharField(max_length=100, choices=PLAN_TYPE, default="STANDARD")
    num_of_adults = models.IntegerField(default=1)
    num_of_children = models.IntegerField(default=0)
    num_of_adults_non_resident = models.IntegerField(default=0)
    num_of_children_non_resident = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stay}"


class UserActivityTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    activity = models.ForeignKey(
        Activities, on_delete=models.SET_NULL, null=True, blank=True
    )
    trip = models.ForeignKey(
        "UserTrip", on_delete=models.CASCADE, related_name="user_activity_trip"
    )
    from_date = models.DateTimeField(default=timezone.now)

    pricing_type = models.CharField(
        max_length=50, choices=PRICING_TYPE, default="PER PERSON"
    )
    number_of_people = models.IntegerField(default=0)
    number_of_people_non_resident = models.IntegerField(default=0)
    number_of_sessions = models.IntegerField(default=0)
    number_of_sessions_non_resident = models.IntegerField(default=0)
    number_of_groups = models.IntegerField(default=0)
    number_of_groups_non_resident = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.activity}"


class UserTransportTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    transport = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True, blank=True
    )
    trip = models.ForeignKey(
        "UserTrip", on_delete=models.CASCADE, related_name="user_transport_trip"
    )
    starting_point = models.CharField(max_length=250, blank=True, null=True)
    from_date = models.DateTimeField(default=timezone.now)
    number_of_days = models.IntegerField(null=True, blank=True)
    user_need_a_driver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transport}"


class UserTrip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_trip"
    )
    name = models.CharField(max_length=250, default="Untitled Trip")
    trips = models.ForeignKey(
        "UserTrips",
        on_delete=models.CASCADE,
        null=True,
        related_name="trip",
        verbose_name="Group Trip",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created by {self.user}"

    class Meta:
        ordering = ["-created_at"]


class UserTrips(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_trips"
    )
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    starting_point = models.CharField(max_length=250, blank=True, null=True)  # remove
    name = models.CharField(max_length=250, default="Untitled Trip")
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Group User Trip"
        verbose_name_plural = "Group User Trips"
