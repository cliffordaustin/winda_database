from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *
from django.utils.text import slugify
from core.utils import generate_random_string

# curated trips signals
@receiver(pre_save, sender=CuratedTrip)
def create_trip_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        random_string = generate_random_string(length=24)
        instance.slug = random_string
