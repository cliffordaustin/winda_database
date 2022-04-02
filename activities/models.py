from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from core.utils import activities_image_thumbnail
from django.utils import timezone

PRICING_TYPE = (
    ("PER PERSON", "PER PERSON"),
    ("PER GROUP", "PER GROUP"),
    ("PER SESSION", "PER SESSION"))


class Activities(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(max_length=250,
                            help_text="If no name, enter a short description of the " +
                                      "activities. Eg Have fun hiking in Nairobi"
                            )
    type_of_activities = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), blank=True, null=True, default=list,
        help_text="Separate each activities by using ' , '. Eg Active Adventures, Wellness experiences"
    )
    location = models.CharField(max_length=350, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    gear_or_equipments = ArrayField(
        models.CharField(max_length=500, blank=True, null=True), blank=True, null=True, default=list,
        help_text="What gear or equipment is needed? Separate each gear or equipments by using ' , '"
    )
    will_you_provide_gear_or_equipments = models.BooleanField(default=False)
    time_taken_for_activities = models.CharField(max_length=350, blank=True, null=True,
                                                 help_text="Input should be in format, eg '4 hours', '12 hours'," +
                                                           " '2 days'")
    description = models.TextField(blank=True, null=True, help_text="what makes this activity special, describe how" +
                                                                    " it will take place")
    pricing_type = models.CharField(max_length=100, choices=PRICING_TYPE, blank=True)
    max_number_of_groups = models.PositiveIntegerField(blank=True, null=True,
                                                       help_text="Enter this field if the pricing plan is per group")
    pricing_per_person = models.IntegerField(blank=True, null=True)
    pricing_per_group = models.IntegerField(blank=True, null=True)
    pricing_per_session = models.IntegerField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user} - {self.name}"

    class Meta:
        verbose_name = "Activities"


class ActivitiesImage(models.Model):
    activity = models.ForeignKey(
        Activities, on_delete=models.CASCADE, related_name="stay_images"
    )
    image = ProcessedImageField(
        upload_to=activities_image_thumbnail(),
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
