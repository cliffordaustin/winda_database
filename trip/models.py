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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transport = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True, blank=True
    )
    stay = models.ForeignKey(Stays, on_delete=models.SET_NULL, null=True, blank=True)
    from_date = models.DateTimeField(default=timezone.now)
    activity_from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(default=next_time)
    number_of_days = models.IntegerField(null=True, blank=True)
    user_need_a_driver = models.BooleanField(default=False)
    number_of_people = models.IntegerField(default=1)
    nights = models.IntegerField(default=3)
    activity = models.ForeignKey(
        Activities, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     self.activity_from_date = self.from_date + timezone.timedelta(days=3)

    #     super(Trip, self).save(*args, **kwargs)

    def __str__(self):
        return f"Created by {self.user}"

    class Meta:
        ordering = ["-created_at"]


class GroupTrip(models.Model):
    starting_point = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    trip = models.ManyToManyField(Trip, blank=True)
    transport_back = models.ForeignKey(
        Transportation, on_delete=models.SET_NULL, null=True, blank=True
    )
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Created by {self.user}"


# class TripImage(models.Model):
#     trip = models.ForeignKey(
#         Trip,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#         related_name="trip_images",
#     )
#     image = ProcessedImageField(
#         upload_to=trip_image_thumbnail,
#         processors=[ResizeToFill(1000, 750)],
#         format="JPEG",
#         options={"quality": 60},
#     )
#     main = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             saved_image = self.image
#             self.image = None
#             super(TripImage, self).save(*args, **kwargs)

#             self.image = saved_image
#             if "force_insert" in kwargs:
#                 kwargs.pop("force_insert")

#         super(TripImage, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"Created by ${self.trip.user}"


# class GroupTripImage(models.Model):
#     group_trip = models.ForeignKey(
#         GroupTrip, on_delete=models.CASCADE, related_name="group_trip_images"
#     )
#     image = ProcessedImageField(
#         upload_to=group_trip_image_thumbnail,
#         processors=[ResizeToFill(1000, 750)],
#         format="JPEG",
#         options={"quality": 60},
#     )
#     main = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             saved_image = self.image
#             self.image = None
#             super(GroupTripImage, self).save(*args, **kwargs)

#             self.image = saved_image
#             if "force_insert" in kwargs:
#                 kwargs.pop("force_insert")

#         super(GroupTripImage, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"Created by ${self.group_trip.user}"
