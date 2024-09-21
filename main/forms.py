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
class TrainerChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=50, required=True)


# Reports: Send reports from trainer to user and vice versa
class ReportForTrainerForm(forms.ModelForm):
    class Meta:
        model = models.TrainerSubscriberReport
        fields = ('report_for_trainer', 'report_msg')

class ReportForUserForm(forms.ModelForm):
    class Meta:
        model = models.TrainerSubscriberReport
        fields = ('report_for_user', 'report_msg', 'report_from_trainer')
        widgets = {'report_from_trainer': forms.HiddenInput()}


class ReportForTrainerForm(forms.ModelForm):
    class Meta:
        model = models.TrainerSubscriberReport
        fields = ('report_for_trainer', 'report_msg', 'report_from_user')
        widgets = {'report_from_user': forms.HiddenInput()}