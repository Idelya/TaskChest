from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.forms import formset_factory, ModelChoiceField
from bootstrap_datepicker_plus import DatePickerInput

from .models import User, Project, Membership, Table, Task, LogWork

class DateInput(forms.DateInput):
    input_type='date'

class CustomTableField(forms.CharField):    
    def label_from_instance(self, table):
        return "%s" % table.name

class NewTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name', )
        widgets = {
            'name': forms.TextInput()
        }

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

class TaskCreateForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
            queryset=None,
            widget=forms.CheckboxSelectMultiple,
            required=False)
    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id', None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        members = Membership.objects.filter(project_id=self.project_id).values('user_id')
        self.fields['table'].queryset = Table.objects.filter(project_id=self.project_id).all()
        self.fields['assigned_users'].queryset = User.objects.filter(pk__in = members)


    class Meta:
        model = Task
        fields = ('name', 'estimate', 'priority', 'describe', 'task_type', 'table', 'assigned_users')


class LogTimeForm(forms.ModelForm):
    class Meta:
        model = LogWork
        fields = ('date','logedTime')
        widgets = {
            'date': DateInput()
        }
