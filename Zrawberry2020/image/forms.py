from django import forms
from django.core.files.base import ContentFile

from .models import Picture


class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('title', 'image',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        image = self.cleaned_data['image']
        ext = image.name.split('.')[-1].lower()
        if ext not in ['jpg', 'png']:
            raise forms.ValidationError("仅支持jpg和png")

        return image