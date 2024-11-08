from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from core.utils import activities_image_thumbnail
from datetime import datetime, timedelta, date, tzinfo
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


PRICING_TYPE = (
    ("PER PERSON", "PER PERSON"),
    ("PER GROUP", "PER GROUP"),
    ("PER SESSION", "PER SESSION"),
)


PRICING_STATUS = (
    ("REASONABLE", "REASONABLE"),
    ("MID-RANGE", "MID-RANGE"),
    ("HIGH-END", "HIGH-END"),
)


class EnquipmentProvided(models.Model):
    activity = models.ForeignKey(
        "Activities", on_delete=models.CASCADE, related_name="enquipment_provided"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.activity.name)

    class Meta:
        verbose_name = "Inclusions"
        verbose_name_plural = "Inclusions"


class EnquipmentRequiredByUser(models.Model):
    activity = models.ForeignKey(
        "Activities",
        on_delete=models.CASCADE,
        related_name="enquipment_required_by_user",
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.activity.name)

    class Meta:
        verbose_name = "What to bring"
        verbose_name_plural = "What to bring"


class Facts(models.Model):
    activity = models.ForeignKey(
        "Activities",
        on_delete=models.CASCADE,
        related_name="facts",
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.activity.name)

    class Meta:
        verbose_name = "Quick Fact"
        verbose_name_plural = "Quick Facts"


class Activities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(
        max_length=250,
        help_text="If no name, enter a short description of the "
        + "activities. Eg Have fun hiking in Nairobi",
    )
    type_of_activities = ArrayField(
        models.CharField(max_length=500, blank=True, null=True),
        blank=True,
        null=True,
        default=list,
        help_text="Separate each activities by using ' , '. Eg Active Adventures, Wellness experiences",
    )
    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Separate each tag by using ' , '",
    )
    location = models.CharField(
        max_length=350, blank=True, null=True, verbose_name="Address"
    )
    city = models.CharField(
        max_length=350, blank=True, null=True, verbose_name="county"
    )
    country = models.CharField(max_length=350, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    min_capacity = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    duration_of_activity = models.DurationField(blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="what makes this activity special, describe how"
        + " it will take place",
    )

    pricing_type = models.CharField(
        max_length=100, choices=PRICING_STATUS, default="REASONABLE"
    )

    price_per_person = models.BooleanField(default=True)
    price = models.FloatField(default=0)
    price_non_resident = models.FloatField(default=0)
    price_is_flexible = models.BooleanField(
        default=False,
        help_text="This means they will be a 'from' price next to the price in the frontend. Eg from $100 per person",
    )

    price_per_session = models.BooleanField(default=False)
    session_price = models.FloatField(blank=True, null=True)
    session_price_non_resident = models.FloatField(blank=True, null=True)

    price_per_group = models.BooleanField(default=False)
    group_price = models.FloatField(blank=True, null=True)
    group_price_non_resident = models.FloatField(blank=True, null=True)
    max_number_of_people_in_a_group = models.PositiveIntegerField(default=4)
    max_number_of_groups = models.PositiveIntegerField(default=1)

    date_posted = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    contact_name = models.CharField(max_length=250, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = PhoneNumberField(blank=True)
    company = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    refundable = models.BooleanField(default=False)
    refund_policy = models.CharField(max_length=500, blank=True, null=True)
    damage_policy = models.CharField(max_length=500, blank=True, null=True)
    children_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    covid_19_compliance = models.BooleanField(default=False)
    covid_19_compliance_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.name}"

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"


class ActivitiesImage(models.Model):
    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="activity_images"
    )
    image = ProcessedImageField(
        upload_to=activities_image_thumbnail,
        processors=[ResizeToFill(1000, 750)],
        format="JPEG",
        options={"quality": 60},
    )
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(ActivitiesImage, self).save(*args, **kwargs)

            self.image = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(ActivitiesImage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity.user} - {self.activity.name}"

    class Meta:
        verbose_name = "Experience Image"
        verbose_name_plural = "Experience Images"


class Views(models.Model):
    user_ip = models.TextField(default=None)
    activity = models.ForeignKey(
        Activities, related_name="activity_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{ self.activity.user }"

    class Meta:
        verbose_name = "Activity Views"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_user"
    )
    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="activity_cart"
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
        return f"{self.activity.name}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user"
    )

    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="activity_order"
    )
    from_date = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    pricing_type = models.CharField(
        max_length=50, choices=PRICING_TYPE, default="PER PERSON"
    )
    number_of_people = models.IntegerField(default=0)
    number_of_people_non_resident = models.IntegerField(default=0)
    number_of_sessions = models.IntegerField(default=0)
    number_of_sessions_non_resident = models.IntegerField(default=0)
    number_of_groups = models.IntegerField(default=0)
    number_of_groups_non_resident = models.IntegerField(default=0)
    reviewing = models.BooleanField(default=True)
    email_sent = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for { self.activity.name } by {self.user}"


class Review(models.Model):
    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="activity_reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_user"
    )
    rate = models.IntegerField(
        blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(5))
    )
    title = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return "Rated as " + str(self.rate) + " star - " + str(self.title)


class SaveActivities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="saved_activities"
    )

    def __str__(self):
        return str(self.activity)
