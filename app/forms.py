from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.forms import formset_factory

from .models import User, Project, Membership


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', )
        widgets = {
            'name': forms.TextInput()
        }

class MemberForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput()
    )

MembershipFormset = forms.formset_factory(MemberForm,extra=1)