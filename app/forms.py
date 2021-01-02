from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields