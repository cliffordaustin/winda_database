from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=SingleTrip)
def create_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=RequestCustomTrip)
def create_request_custom_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=RequestInfo)
def create_request_info_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string
