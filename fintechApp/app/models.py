from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .choiceArrays import *
from django.forms import ModelForm
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

class UserMadeGroup(models.Model):
    """
    Model representing a user group. Can be created by any user.
    """
    group_name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('group_detail', args=[str(self.id)])


class Report(models.Model):
    reportName = models.CharField(max_length=50, default="NO_NAME")
    companyUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timeStamp = models.DateField(null=True, blank=True)
    companyName = models.CharField(max_length=50)
    companyPhone = models.CharField(max_length=12)
    companyLocation = models.CharField(max_length=50)
    companyCountry = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default="US")
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    # currentProjects =
    accessType = models.CharField(max_length=7, choices=(("private", "private"), ("public", "public")), default="public")
    # files

    def __str__(self):
        return self.reportName + self.sector

    def get_absolute_url(self):
        return reverse('report_detail', args=[str(self.id)])

class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = ['reportName', 'companyUser', 'timeStamp', 'companyName','companyPhone','companyLocation','companyCountry','sector', 'industry','accessType']
        fields = '__all__'
        exclude = ["companyUser"]

class SuspendUserForm(forms.Form):
    kam = forms.ModelChoiceField(queryset=User.objects.all())

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
