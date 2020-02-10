from django.db import models
from datetime import date
from django.urls import reverse
# from django.contrib.auth.models import User

# from slugify import slugify
from uuid import uuid4
import os


def path_and_rename(instance, filename):
    upload_to = 'mypictures'
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