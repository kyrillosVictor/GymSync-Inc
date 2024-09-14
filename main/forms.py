from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import models

# Enquiry form
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = models.Enquiry
        fields = ("full_name", "email", "detail",)


# User registration form with the below fields
class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


# Edit user's profile
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


# Django session for trainers login
class TrainerLoginForm(forms.ModelForm):
    class Meta:
        model = models.Trainer
        fields = ('username', 'password')


# Trainer Profile Form
class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = models.Trainer
        fields = ('full_name', 'mobile', 'address', 'img', 'details', 'facebook', 'instagram', 'twitter', 'youtube', 'blog')


# Trainer - Change Password
class TrainerChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(max_length=50, required=True)