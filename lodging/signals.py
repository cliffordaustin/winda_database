from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import (
    Stays,
    RoomAvailability,
    RoomType,
    Bookings,
    RoomAvailabilityResident,
    RoomAvailabilityNonResident,
)
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=Stays)
def create_stay_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.name)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string


@receiver(pre_save, sender=RoomAvailability)
def create_room_availability_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=12)
        instance.slug = random_string


@receiver(pre_save, sender=RoomAvailabilityResident)
def create_resident_room_availability_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=12)
        instance.slug = random_string


@receiver(pre_save, sender=RoomAvailabilityNonResident)
def create_non_resident_room_availability_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=12)
        instance.slug = random_string


@receiver(pre_save, sender=RoomType)
def create_room_type_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=12)
        instance.slug = random_string


@receiver(pre_save, sender=Bookings)
def create_booking_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=12)
        instance.slug = random_string
