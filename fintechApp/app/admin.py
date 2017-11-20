from django.contrib import admin

from .models import UserMadeGroup, Report, ReportFile

admin.site.register(UserMadeGroup)
admin.site.register(Report)
admin.site.register(ReportFile)