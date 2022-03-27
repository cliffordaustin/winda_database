from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from core.utils import lodge_image_thumbnail


ROOM_IS_ENSUITE = (("YES", "YES"), ("NO", "NO"))
PRICING_TYPE = (
    ("PER PERSON", "PER PERSON"),
    ("PER ROOM", "PER ROOM"),
    ("WHOLE PLACE", "WHOLE PLACE"),
)


class Stays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=250)
    type_of_lodge = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), default=list
    )
    type_of_house = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), default=list
    )
    type_of_unique_space = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), default=list
    )
    type_of_campsite = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), default=list
    )
    type_of_boutique_hotel = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), default=list
    )
    location = models.CharField(max_length=350, blank=True, null=True)
    num_of_capacity = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    room_is_ensuite = models.CharField(
        max_length=100, choices=ROOM_IS_ENSUITE, blank=True
    )
    amenities = ArrayField(
        models.CharField(max_length=250, blank=True, null=True), default=list
    )
    description = models.TextField(blank=True, null=True)
    unique_about_place = models.TextField(blank=True, null=True)
    pricing_type = models.CharField(max_length=100, choices=PRICING_TYPE, blank=True)
    pricing_per_person = models.IntegerField(blank=True, null=True)
    pricing_per_room = models.IntegerField(blank=True, null=True)
    pricing_per_whole_place = models.IntegerField(blank=True, null=True)

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

    def __str__(self):
        return f"{self.stay.user} - {self.stay.name}"
