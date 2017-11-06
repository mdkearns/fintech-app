from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user/', views.adduser, name='create_user'),
    url(r'^reports/$', views.reports.as_view(), name='reports'),
	url(r'^fda_authenticate', views.fda_authenticate, name='fda_authenticate'),
	url(r'^get_reports', views.get_reports, name='get_reports'),
    url(r'^create_report/', views.add_report, name='create_report'),
]
