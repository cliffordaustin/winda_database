from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from core.utils import profile_image_thumbnail

from imagekit.models import ProcessedImageField
from imagekit.processors import Resize, ResizeToFill


class UserManger(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            return TypeError("User should have an email")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if email is None:
            return TypeError("User should have an email")

        if password is None:
            return TypeError("Password should not be none")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    instagram_username = models.CharField(max_length=120, blank=True, null=True)
    tiktok_username = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(blank=True, null=True)
    profile_pic = ProcessedImageField(
        upload_to=profile_image_thumbnail,
        processors=[ResizeToFill(700, 450)],
        format="JPEG",
        options={"quality": 60},
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManger()

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.profile_pic
            self.profile_pic = None
            super(CustomUser, self).save(*args, **kwargs)

            self.profile_pic = saved_image
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")

        super(CustomUser, self).save(*args, **kwargs)
