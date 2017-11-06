from django.contrib import admin

from .models import CustomUser, UserType, Report

admin.site.register(CustomUser)
admin.site.register(UserType)
admin.site.register(Report)
