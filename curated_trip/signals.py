from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import *
from django.utils.text import slugify
from core.utils import generate_random_string

# curated trips signals
@receiver(pre_save, sender=CuratedTrip)
def create_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=CuratedTrip)
def create_date_pricing_slug(sender, instance, *args, **kwargs):
    for date_pricing in instance.date_and_pricing.all():
        random_string = generate_random_string(length=24)
        if not date_pricing.slug:
            date_pricing.slug = random_string
            date_pricing.save()
