from django.db import models
from django.contrib.auth.models import AbstractUser
from AdminPanel.models import *
from django.contrib.auth.models import User, auth
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


class Creator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True, default="Hi there, I am new to Buzzy.")
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ForeignKey(ImageDetail, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    total_price = models.IntegerField(null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    payment_mode = models.CharField(max_length=50, null=True)
    plan = models.CharField(max_length=50, null=True)

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(ImageDetail, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=500, null=True)
    date_added = models.DateField(auto_now_add=True)

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    credits_available = models.IntegerField(null=True, default=0)
    

class Downloads(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ForeignKey(ImageDetail, on_delete=models.CASCADE, null=True, blank=True)
    date_downloaded = models.DateField(auto_now_add=True)


class Favourites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ForeignKey(ImageDetail, on_delete=models.CASCADE, null=True, blank=True)
    
