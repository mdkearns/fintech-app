from django.contrib import admin

from .models import UserMadeGroup, Report, ReportFile, Message, Comment, Rating

admin.site.register(UserMadeGroup)
admin.site.register(Report)
admin.site.register(ReportFile)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Rating)