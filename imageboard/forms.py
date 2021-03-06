from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, UserInfo, ModerationRequest, Transfer, Comments, Complaints


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'public',)


class NewUserForm(UserCreationForm):
    captcha = CaptchaField()

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
        fields = ('name', 'second_name', 'info')


class RecoveryForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('secret',)


class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('public',)


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = ModerationRequest
        fields = ('accept',)


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('token',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ('to_user', 'image_token',)


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('body',)


class ComplaintApprovalForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ('resolve',)
