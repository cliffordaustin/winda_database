from django.db.models.signals import pre_save
from django.dispatch import receiver

from transport.admin import GeneralTransferAdmin
from .models import Flight, Transportation
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=Transportation)
def create_transport_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=Flight)
def create_flight_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string


@receiver(pre_save, sender=GeneralTransferAdmin)
def create_general_transfer_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string
