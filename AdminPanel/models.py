from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
from imagekit.processors import ResizeToFit
# Create your models here.

class ImageDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    price = models.BooleanField(null=True, default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_thumbnail = ImageSpecField(source='image', format='JPEG', options={'quality': 8})
    approval = models.CharField(max_length=50, null=True)
    rate = models.IntegerField(default=1)
    description = models.CharField(max_length=200, null=True)

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except ValueError:
            url = ''
        return url


class Tags(models.Model):
    tag = models.CharField(max_length=50, null=True, blank=True)
    image = models.ForeignKey(ImageDetail, on_delete=models.CASCADE, related_name="tag_image", null=True, blank=True)
