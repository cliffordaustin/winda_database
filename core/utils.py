import random
import string

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits

STRING_LENGTH = 12


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))


def profile_image_thumbnail(instance, filename):
    return f"profile_images/{instance.id}/{filename}"


def lodge_image_thumbnail(instance, filename):
    return f"lodge_images/{instance.id}/{filename}"


def activities_image_thumbnail(instance, filename):
    return f"activities_images/{instance.id}/{filename}"
