from django import forms
from django.contrib.auth.models import User
from .models import LinkBox


class LinkForm(forms.Form):
    sitename = forms.CharField(label="站点名")
    url = forms.URLField(label="网址")

