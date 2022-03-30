from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Stays
from django.utils.text import slugify
from core.utils import generate_random_string


@receiver(pre_save, sender=Stays)
def create_stay_slug(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.name)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string