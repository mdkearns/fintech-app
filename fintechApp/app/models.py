from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .choiceArrays import *


class UserType(models.Model):
    title = models.CharField(max_length=50)
    # permissions

    def __str__(self):
        return self.title

class CustomUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_type = models.ForeignKey(UserType)

    def __str__(self):
        return self.first_name + self.last_name

    def getType(self):
        return self.user_type

class UserMadeGroup(models.Model):
    """
    Model representing a user group. Can be created by any user.
    """
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.group_name


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
        return self.reportName