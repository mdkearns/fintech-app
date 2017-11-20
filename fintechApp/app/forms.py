from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Report, UserMadeGroup

GROUPS = [('Investor User','Investor User'),
    ('Company User','Company User')]

class UserForm(UserCreationForm):

    user_type = forms.ChoiceField(choices=GROUPS, widget = forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2','user_type')

class UserMadeGroupForm(ModelForm):
    class Meta:
        model = UserMadeGroup
        fields = ['group_name', 'members']

class RemoveUserMadeGroupForm(forms.Form):
    request = None
    usermadegroups = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RemoveUserMadeGroupForm, self).__init__(*args, **kwargs)
        self.fields['usermadegroups'].queryset=UserMadeGroup.objects.filter(members=self.request.user)
        self.fields['usermadegroups'].label = 'Groups you belong to'

class AddUserToUserMadeGroupForm(forms.Form):
    request = None
    users = forms.ModelMultipleChoiceField(queryset=None)
    this_group = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.this_group = kwargs.pop('this_group')

        super(RemoveUserMadeGroupForm, self).__init__(*args, **kwargs)
        users_not_in_group = []
        for user in User.objects.all():
            if user not in self.this_group.members:
                user_not_in_group.append(user)
        self.fields['users'].queryset=User.objects.filter(members=users_not_in_group)
        self.fields['users'].label = 'Users not in this group'
