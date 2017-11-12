from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user/', views.adduser, name='create_user'),
    url(r'^reports/$', views.reports.as_view(), name='reports'),
	url(r'^fda_authenticate', views.fda_authenticate, name='fda_authenticate'),
	url(r'^get_reports', views.get_reports, name='get_reports'),
    url(r'^create_report/', views.add_report, name='create_report'),
    url(r'^report/(?P<pk>\d+)$', views.reportDetail.as_view(), name='report_detail'),
    url(r'^groups/$', views.groups.as_view(), name='groups'),
    url(r'^group/(?P<pk>\d+)$', views.group_detail.as_view(), name='group_detail'),
]
