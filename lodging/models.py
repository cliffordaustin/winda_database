from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from core.utils import lodge_image_thumbnail
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator, MaxValueValidator

ROOM_IS_ENSUITE = (("YES", "YES"), ("NO", "NO"))

PRICING_TYPE = (
    ("PER PERSON", "PER PERSON"),
    ("PER ROOM", "PER ROOM"),
    ("WHOLE PLACE", "WHOLE PLACE"),
)

TYPE_OF_STAY = (
    ("LODGE", "LODGE"),
    ("HOUSE", "HOUSE"),
    ("UNIQUE SPACE", "UNIQUE SPACE"),
    ("CAMPSITE", "CAMPSITE"),
    ("BOUTIQUE HOTEL", "BOUTIQUE HOTEL"),
)

tomorrow_time = date.today() + timedelta(days=1)


class Stays(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(
        max_length=100,
        help_text="If no name, enter a short description of the "
        + "accommodation. Eg A lovely place located at the lake side",
        verbose_name="Name or description",
    )
    type_of_stay = models.CharField(max_length=100, choices=TYPE_OF_STAY, blank=True)
    best_describes_lodge = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each description by using ' , '. Eg Tented camp, Permanent structures",
    )
    best_describes_house = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each description by using ' , '. Eg Residential home, Villa",
    )
    best_describes_unique_space = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each description by using ' , '. Eg Boathouse, Bus",
    )
    essential_information = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each essential information by using ' , '. Eg Covid-19 compliance",
    )
    best_describes_campsite = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each description by using ' , '. Eg On private property, In a conservancy",
    )
    best_describes_boutique_hotel = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each description by using ' , '. Eg Historical building, Resort",
    )
    location = models.CharField(
        max_length=350, blank=True, null=True, verbose_name="Address"
    )
    city = models.CharField(max_length=350, blank=True, null=True)
    country = models.CharField(max_length=350, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    room_is_ensuite = models.BooleanField(default=False)
    amenities = ArrayField(
        models.CharField(max_length=250, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each amenities by using ' , '. Eg Swimming Pool, Hot tub",
    )
    description = models.TextField(blank=True, null=True)
    unique_about_place = models.TextField(blank=True, null=True)
    pricing_type = models.CharField(max_length=100, choices=PRICING_TYPE, blank=True)
    price = models.FloatField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

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

    def __str__(self):
        return f"{self.stay.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="order")
    from_date = models.DateField(default=date.today())
    to_date = models.DateField(default=tomorrow_time)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order for { self.stay.name } by {self.user}"


class Review(models.Model):
    stay = models.ForeignKey(Stays, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.rate) + " - " + str(self.title)
