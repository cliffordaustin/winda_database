from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Trip, GroupTrip
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=Trip)
def create_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=GroupTrip)
def create_group_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string
