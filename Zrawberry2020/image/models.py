from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
# from django.contrib.auth.models import User


# from slugify import slugify
from datetime import date
from uuid import uuid4
import os


def path_and_rename(instance, filename):
    upload_to = 'picture'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Picture(models.Model):
    title = models.CharField("标题", max_length=100, blank=True, default='')
    image = models.ImageField("图片", upload_to=path_and_rename, blank=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:pic_detail', args=[str(self.id)])


@receiver(post_delete, sender=Picture)
def delete_upload_images(sender, instance, **kwargs):
    image = getattr(instance, 'image', '')
    if not image:
        return
    imagename = os.path.join(settings.MEDIA_ROOT, str(image))
    if os.path.isfile(imagename):
        os.remove(imagename)

