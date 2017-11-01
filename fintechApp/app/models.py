from django.db import models
from django.contrib.auth.models import User


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
