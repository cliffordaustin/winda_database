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
    ("SEDAN", "SEDAN"),
    ("SMALL CAR", "SMALL CAR"),
)


class Transportation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    type_of_car = models.CharField(max_length=100, choices=TYPE_OF_CAR, blank=True)
    vehicle_plate = models.CharField(max_length=100, blank=True, null=True)
    vehicle_make = models.CharField(max_length=100, blank=True, null=True)
    vehicle_color = models.CharField(
        max_length=100, blank=True, null=True, help_text="eg. Red or #FF0000"
    )
    price = models.FloatField(blank=True, null=True, help_text="Price per 10km")
    price_per_day = models.FloatField(
        blank=True, null=True, help_text="Price per day, if available"
    )
    additional_price_with_a_driver = models.FloatField(
        blank=True, null=True, help_text="Price when a user needs a driver"
    )
    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    has_air_condition = models.BooleanField(default=False)
    fm_radio = models.BooleanField(default=False)
    cd_player = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    audio_input = models.BooleanField(default=False)
    cruise_control = models.BooleanField(default=False)
    overhead_passenger_airbag = models.BooleanField(default=False)
    side_airbag = models.BooleanField(default=False)
    power_locks = models.BooleanField(default=False)
    power_mirrors = models.BooleanField(default=False)
    power_windows = models.BooleanField(default=False)
    safety_tools = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each tools by using ' , '. Eg Spare wheel, Carjack",
    )
    open_roof = models.BooleanField(default=False)
    dropoff_city = models.CharField(max_length=350, blank=True, null=True)
    dropoff_country = models.CharField(max_length=350, blank=True, null=True)

    # policies
    refaundable = models.BooleanField(default=False)
    refund_policy = models.CharField(max_length=500, blank=True, null=True)
    damage_policy = models.CharField(max_length=500, blank=True, null=True)
    children_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    covid_19_compliance = models.BooleanField(default=False)
    covid_19_compliance_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.type_of_car}"


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
