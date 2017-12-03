from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Report, ReportFile, UserMadeGroup, Message
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace

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

class ChooseGroupToAddUsersForm(forms.Form):
    request = None
    usermadegroup = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ChooseGroupToAddUsersForm, self).__init__(*args, **kwargs)
        self.fields['usermadegroup'].queryset=UserMadeGroup.objects.filter(members=self.request.user)
        self.fields['usermadegroup'].label = 'Which group would you like to add users to'

class AddUserToUserMadeGroupForm(forms.Form):
    request = None
    users = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddUserToUserMadeGroupForm, self).__init__(*args, **kwargs)
        group_name = self.request.session.get('group_name')
        group = UserMadeGroup.objects.filter(group_name = group_name).first()
        users = []
        for user in User.objects.all():
            if user not in group.members.all():
                users.append(user)

        self.fields['users'].queryset=User.objects.filter(username__in=users)
        self.fields['users'].label = 'Select the users you would like to add to this group'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message_subject', 'message_text', 'encrypted']

class DeleteMessageForm(forms.Form):
    request = None
    messages = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(DeleteMessageForm, self).__init__(*args, **kwargs)
        self.fields['messages'].queryset=Message.objects.filter(receiver=self.request.user)
        self.fields['messages'].label = 'Your Messages'
        self.fields['messages'].label_from_instance = lambda obj: "%s" % obj.message_subject


class addFileToReportForm(forms.Form):
    request = None
    newFiles = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        reportId = kwargs.pop("reportId")
        super(addFileToReportForm, self).__init__(*args, **kwargs)
        newFiles = []
        report = Report.objects.filter(id = reportId).first()
        allUsableFiles = ReportFile.objects.filter(companyUser = self.request.user )

        for reportFile in allUsableFiles:
            if reportFile not in report.files.all():
                newFiles.append(reportFile)

        self.fields['newFiles'].queryset = allUsableFiles.filter(name__in=newFiles)
        self.fields['newFiles'].label = ""
        # self.fields['newFiles'].label = 'Select which of your files to add to this report.'