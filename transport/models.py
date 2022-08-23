from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from core.utils import transportation_image_thumbnail
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


TYPE_OF_CAR = (
    ("LARGE 4x4", "LARGE 4x4"),
    ("SMALL 4x4", "SMALL 4x4"),
    ("VAN", "VAN"),
    ("MEDIUM", "MEDIUM"),
    ("MOTORBIKE", "MOTORBIKE"),
    ("PICKUP TRUCK", "PICKUP TRUCK"),
    ("SEDAN", "SEDAN"),
)

TYPE_OF_TRANSMISSION = (
    ("AUTOMATIC", "AUTOMATIC"),
    ("MANUAL", "MANUAL"),
)


class Transportation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    type_of_car = models.CharField(max_length=100, choices=TYPE_OF_CAR, blank=True)
    vehicle_make = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    bags = models.IntegerField(blank=True, null=True)
    price_per_day = models.FloatField(
        blank=True, null=True, help_text="Price per day, if available"
    )
    additional_price_with_a_driver = models.FloatField(
        blank=True, null=True, help_text="Price when a user needs a driver"
    )
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    transmission = models.CharField(
        max_length=100, blank=True, null=True, choices=TYPE_OF_TRANSMISSION
    )
    has_air_condition = models.BooleanField(default=False)
    four_wheel_drive = models.BooleanField(default=False)
    open_roof = models.BooleanField(default=False)

    # policies
    policy = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - { self.vehicle_make } - {self.type_of_car}"

    class Meta:
        verbose_name = "Transportation"
        verbose_name_plural = "Transportations"


class Flight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    starting_point = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)
    number_of_people = models.IntegerField(default=1)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"


class IncludedInPrice(models.Model):
    transportation = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="included_in_price"
    )
    included_in_price = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.transportation} - {self.included_in_price}"


class DriverOperatesWithin(models.Model):
    transportation = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="driver_operates_within"
    )
    city = models.CharField(max_length=350, blank=True, null=True)
    country = models.CharField(max_length=350, blank=True, null=True)

    def __str__(self):
        return f"{self.transportation} - {self.city}"


class TransportationImage(models.Model):
    transportation = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="transportation_images"
    )
    image = ProcessedImageField(
        upload_to=transportation_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(TransportationImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(TransportationImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.transportation.user} - {self.transportation.type_of_car}"


class Views(models.Model):
    user_ip = models.TextField(default=None)
    transport = models.ForeignKey(
        Transportation,
        related_name="transport_views",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{ self.transport.user }"

    class Meta:
        verbose_name = "Transport Views"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_cart"
    )
    transport = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="transport_cart"
    )
    starting_point = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    from_date = models.DateTimeField(default=timezone.now)
    number_of_days = models.IntegerField(null=True, blank=True)
    user_need_a_driver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transport.user} - {self.transport.type_of_car}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_orders"
    )
    transport = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="transport_order"
    )
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    starting_point = models.CharField(max_length=250, blank=True, null=True)
    destination = models.CharField(max_length=250, blank=True, null=True)
    number_of_days = models.IntegerField(null=True, blank=True)
    from_date = models.DateTimeField(default=timezone.now)
    user_need_a_driver = models.BooleanField(default=False)
    distance = models.FloatField(blank=True, null=True)
    reviewing = models.BooleanField(default=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for a { self.transport.type_of_car } by {self.user}"


class Review(models.Model):
    transport = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="transport_review"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_review"
    )
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.rate) + " - " + str(self.title)


class SaveTransportation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transport = models.ForeignKey(
        Transportation, on_delete=models.CASCADE, related_name="saved_transport"
    )

    def __str__(self):
        return str(self.transport)
