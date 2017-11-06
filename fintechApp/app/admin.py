from django.contrib import admin

from .models import CustomUser, UserType, UserMadeGroup, Report

admin.site.register(CustomUser)
admin.site.register(UserType)
admin.site.register(UserMadeGroup)
admin.site.register(Report)
