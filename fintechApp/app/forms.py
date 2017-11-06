from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Report

GROUPS = [('Investor User','Investor User'),
    ('Company User','Company User')]

class UserForm(UserCreationForm):

    user_type = forms.ChoiceField(choices=GROUPS, widget = forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2','user_type')


    