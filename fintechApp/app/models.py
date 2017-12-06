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
from uuid import uuid4
import nacl.utils
from nacl.public import PrivateKey, SealedBox
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class ReportFile(models.Model):
    companyUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, default="NO_NAME")
    file = models.FileField(upload_to='files/')
    encrypted = models.BooleanField(default=False)
	
    def get_file(self):
        return self.file

    def __str__(self):
        return self.name

class Comment(models.Model):
    userName = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=100)
    timeStamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text

class Rating(models.Model):
    userName = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return str(self.rating)

class Report(models.Model):
    reportName = models.CharField(max_length=50, default="NO_NAME")
    companyUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="companyUser")
    timeStamp = models.DateTimeField(null=True, blank=True)
    companyName = models.CharField(max_length=50)
    companyCEO = models.CharField(max_length=50)
    companyPhone = models.CharField(max_length=12)
    companyEmail = models.CharField(max_length=50)
    companyLocation = models.CharField(max_length=50)
    companyCountry = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default="US")
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    currentProjects = models.CharField(max_length=200)
    accessType = models.CharField(max_length=7, choices=(("private", "private"), ("public", "public")), default="public")
    files = models.ManyToManyField(ReportFile, blank=True)
    stars = models.ManyToManyField(User, blank=True, related_name="starred")
    comments = models.ManyToManyField(Comment, blank=True)
    ratings = models.ManyToManyField(Rating, blank=True)

    def __str__(self):
        return self.reportName

    def get_files(self):
			
        return self.files.all()
		
    def add_files(self, file_to_add):
	    self.files.add(file_to_add)

    def display_for_fda(self):
        text = "Report: " + str(self.reportName) + "\n"
        text += "Company User: " + str(self.companyUser) + "\n"
        text += "Time Stamp: " + str(self.timeStamp) + "\n"
        text += "Company Name: " + str(self.companyName) + "\n"
        text += "Company CEO: " + str(self.companyCEO) + "\n"
        text += "Company Phone: " + str(self.companyPhone) + "\n"
        text += "Company Email: " + str(self.companyEmail) + "\n"
        text += "Company Location: " + str(self.companyLocation) + "\n"
        text += "Company Country: " + str(self.companyCountry) + "\n"
        text += "Sector: " + str(self.sector) + "\n"
        text += "Industry: " + str(self.industry) + "\n"
        text += "Current Projects: " + str(self.currentProjects) + "\n"
        text += "Access Type: " + str(self.accessType) + "\n" 
		
        return text

    def get_absolute_url(self):
        return reverse('report_detail', args=[str(self.id)])

    class Meta:
        permissions = (
            ('can_view_reports', "Can view reports"),
            ('can_change_reports', "Can change reports")
        )

class UserMadeGroup(models.Model):
    """
    Model representing a group of users. Can be created by any user.
    """
    group_name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User)
    reports = models.ManyToManyField(Report)

    def __str__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('group_detail', args=[str(self.id)])

    def add_user(group, user):
        UserMadeGroup.objects.get(group_name=group).members.add(User.objects.get(username=user))

    def remove_user(group, user):
        UserMadeGroup.objects.get(group_name=group).members.remove(User.objects.get(username=user))

class Message(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    message_subject = models.CharField(max_length = 200, blank = False)
    message_text = models.TextField(blank = False)
    encrypted = models.BooleanField(default = False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'receiver')
    encrypted_message_text = models.BinaryField()
    should_display_unencrypted_message_text = models.BooleanField(default = False)

    class Meta:
       ordering = ['-time_stamp']

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])

    def decrypt(self):
        self.should_display_unencrypted_message_text = True
        self.save()
        return self.receiver.key.decrypt(self.encrypted_message_text)


class ReportForm(ModelForm):
    class Meta:
        model = Report
        # fields = ['reportName', 'companyUser', 'timeStamp', 'companyName','companyPhone','companyLocation','companyCountry','sector', 'industry','accessType']
        fields = '__all__'
        exclude = ["companyUser", "timeStamp","stars"]
        request = None
        files = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['files'].queryset = ReportFile.objects.filter(companyUser = user)

class ReportForm2(ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        request = None

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ["userName","timeStamp"]
        request = None

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

class AddToGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    group = forms.ModelChoiceField(queryset = UserMadeGroup.objects.all(), empty_label=None)
    action = forms.ChoiceField(choices=( ('A', 'Add'), ('R', 'Remove') ), required=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suspended = models.BooleanField(default=False)

class DeleteReportForm(forms.Form):
    report = forms.ModelChoiceField(queryset=Report.objects.all(), empty_label=None)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class CustomKey(object):
    def __init__(self, private_key):
        self.priv_key=private_key

class Key(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = CustomKey(PrivateKey.generate())

    def gen_key(self):
        print("NEW KEY GENERATED................................................")
        self.key = PrivateKey.generate()
        self.user.key.save()
        print(self.key)

    def get_pub_key(self):
        return self.key.priv_key.public_key

    def get_priv_key(self):
        return self.key.priv_key

    def encrypt(self, message):
        sealed_box = SealedBox(self.get_pub_key())
        return sealed_box.encrypt(message)

    def decrypt(self, encrypted_message):
        unseal_box = SealedBox(self.get_priv_key())
        return unseal_box.decrypt(encrypted_message)




@receiver(post_save, sender=User)
def create_user_key(sender, instance, created, **kwargs):
    if created:
        Key.objects.create(user=instance)
        Key.objects.filter(user=instance).first().gen_key()


@receiver(post_save, sender=User)
def save_user_key(sender, instance, **kwargs):
    instance.key.save()
