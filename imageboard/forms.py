from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, UserInfo


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'public',)


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('name', 'second_name', 'avatar', 'info')