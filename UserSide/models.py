from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserDetail(AbstractUser):
    mobile_number = models.BigIntegerField(null=True)
    user_image = models.ImageField(null=True, blank=True, default="profileDefault.jpg")

    @property
    def ImageURL(self):
        try:
            url = self.user_image.url
        except ValueError:
            url = ''
        return url
