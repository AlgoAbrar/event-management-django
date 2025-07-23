from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_image_path(instance, filename):
    return f'profile_pictures/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_image_path,
        default='profile_pictures/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
