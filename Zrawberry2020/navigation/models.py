from json import dumps
from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User


class LinkBox(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LinkBox")
    boxname = models.CharField(max_length=20)
    urls = models.TextField(blank=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.boxname

    @staticmethod
    def dict_jsontr(urlds):
        if type(urlds) is dict:
            return dumps(urlds, sort_keys=True)
        elif type(urlds) is str:
            return eval(urlds)
        else:
            return None

    def str2dict(self):
        if self.urls:
            return eval(self.urls)
        else:
            return {}

    def urls_num(self):
        if self.urls:
            return len(self.str2dict())
        else:
            return 0