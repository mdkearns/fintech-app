from django.contrib import admin

from .models import CustomUser, UserType

admin.site.register(CustomUser)
admin.site.register(UserType)
