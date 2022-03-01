from django import forms

from .models import Image, Users

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'image', 'public',)

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'password']