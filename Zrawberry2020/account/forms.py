import datetime
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for v in self.fields.values():
            v.widget.attrs.update({'class': 'form-control'})


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for v in self.fields.values():
            v.widget.attrs.update({'class': 'form-control'})


    def clean_password2(self):
        """在调用is_valid()时会执行 clean_+属性名称()"""
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("密码不匹配")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    birth = forms.DateField(required=False, initial=datetime.date.today)
    wechat = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ("wechat", "birth")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for v in self.fields.values():
            v.widget.attrs.update({'class': 'form-control'})


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for v in self.fields.values():
            v.widget.attrs.update({'class': 'form-control'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)