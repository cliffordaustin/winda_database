from django.db import models
from django.conf import settings
from activities.models import Activities
from core.utils import group_trip_image_thumbnail, trip_image_thumbnail

from lodging.models import Stays
from transport.models import Transportation
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone

next_time = timezone.now() + timezone.timedelta(days=3)


class Trip(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    transport = models.ForeignKey(Transportation, on_delete=models.SET_NULL, null=True)

    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True)
    stay_from_date = models.DateTimeField(default=timezone.now)
    stay_to_date = models.DateTimeField(default=next_time)

    activity = models.ForeignKey(Activities, on_delete=models.SET_NULL, null=True)
    activity_from_date = models.DateTimeField(default=timezone.now)
    activity_to_date = models.DateTimeField(default=next_time)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"Created by ${self.user}"

    class Meta:
        ordering = ["-created_at"]


class TripImage(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="trip_images",
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
            super(TripImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(TripImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created by ${self.trip.user}"


class GroupTrip(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    trip = models.ManyToManyField(Trip, related_name="group_trip")
    transport_back = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Created by ${self.user}"


class GroupTripImage(models.Model):
    group_trip = models.ForeignKey(
        GroupTrip, on_delete=models.CASCADE, related_name="group_trip_images"
    )
    image = ProcessedImageField(
        upload_to=group_trip_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(GroupTripImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(GroupTripImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created by ${self.group_trip.user}"
