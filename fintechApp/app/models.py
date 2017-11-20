from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .choiceArrays import *
from django.forms import ModelForm, Select
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.core.files.storage import FileSystemStorage
import json

class UserMadeGroup(models.Model):
    """
    Model representing a group of users. Can be created by any user.
    """
    group_name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('group_detail', args=[str(self.id)])

    def remove_user(group, user):
        UserMadeGroup.objects.get(group_name=group).members.remove(User.objects.get(username=user))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class ReportFile(models.Model):
    companyUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, default="NO_NAME")
    file = models.FileField(upload_to='files/')
    encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    reportName = models.CharField(max_length=50, default="NO_NAME")
    companyUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timeStamp = models.DateTimeField(null=True, blank=True)
    companyName = models.CharField(max_length=50)
    companyPhone = models.CharField(max_length=12)
    companyLocation = models.CharField(max_length=50)
    companyCountry = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default="US")
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    # currentProjects =
    accessType = models.CharField(max_length=7, choices=(("private", "private"), ("public", "public")), default="public")
    files = models.ManyToManyField(ReportFile, null=True)

    def __str__(self):
        return self.reportName + self.sector

    def display_for_fda(self):
        text = "Report: " + str(self.reportName) + "\n"
        text += "Company User: " + str(self.companyUser) + "\n"
        text += "Time Stamp: " + str(self.timeStamp) + "\n"
        text += "Company Name: " + str(self.companyName) + "\n"
        text += "Company Phone: " + str(self.companyPhone) + "\n"
        text += "Company Location: " + str(self.companyLocation) + "\n"
        text += "Company Country: " + str(self.companyCountry) + "\n"
        text += "Sector: " + str(self.sector) + "\n"
        text += "Industry: " + str(self.industry) + "\n"
        return text

    def get_absolute_url(self):
        return reverse('report_detail', args=[str(self.id)])

    class Meta:
        permissions = (
            ('can_view_reports', "Can view reports"),
            ('can_change_reports', "Can change reports")
        )

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = ['reportName', 'companyUser', 'timeStamp', 'companyName','companyPhone','companyLocation','companyCountry','sector', 'industry','accessType']
        fields = '__all__'
        exclude = ["companyUser", "timeStamp"]
        request = None
        files = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['files'].queryset = ReportFile.objects.filter(companyUser = user)

class ReportFileForm(ModelForm):
    class Meta:
        model = ReportFile
        fields = '__all__'
        exclude = ["companyUser"]


class SuspendUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    action = forms.ChoiceField(choices=( ('S', 'Suspend'), ('U', 'Unsuspend') ), required=True)

class AddSMForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suspended = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
