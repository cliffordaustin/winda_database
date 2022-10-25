from unicodedata import name
from django.db import models
from tinymce.models import HTMLField


CATEGORIES = (
    ("Lifestyle", "Lifestyle"),
    ("Travel", "Travel"),
    ("Food", "Food"),
    ("Fashion", "Fashion"),
    ("Beauty", "Beauty"),
    ("Health", "Health"),
    ("Relationship", "Relationship"),
    ("Tech", "Tech"),
    ("Entertainment", "Entertainment"),
    ("Sports", "Sports"),
    ("Education", "Education"),
    ("Science", "Science"),
    ("Environment", "Environment"),
    ("History", "History"),
    ("Culture", "Culture"),
    ("Winda research", "Winda research"),
    ("Art", "Art"),
    ("Music", "Music"),
    ("Movies", "Movies"),
    ("Games", "Games"),
    ("Other", "Other"),
)


class Blog(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True, editable=False)
    name = models.CharField(max_length=250)
    content = HTMLField()
    category = models.CharField(
        max_length=250, blank=True, null=True, choices=CATEGORIES
    )
    header_image_src = models.URLField(blank=True, null=True)
    estimated_minute_read = models.IntegerField(
        default=5, help_text="Estimated time to read in minutes"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
