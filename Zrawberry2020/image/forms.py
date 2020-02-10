from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
# from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description')

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageForm, self).save(commit=False)   # 建立实例 不保存数据
        image_name = slugify(image.title)

        if commit:
            image.save()
        return image


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()