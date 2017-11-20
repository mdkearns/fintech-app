from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_user/', views.adduser, name='create_user'),
    url(r'^reports/$', views.reports.as_view(), name='reports'),
    url(r'^reports_search/$', views.reportSearchListView.as_view(), name='reports_search'),
	url(r'^fda_authenticate', views.fda_authenticate, name='fda_authenticate'),
	url(r'^get_reports', views.get_reports, name='get_reports'),
	url(r'^make_reports', views.make_reports, name='make_reports'),
	url(r'^display_report', views.display_report, name='display_report'),
    url(r'^create_report/', views.add_report, name='create_report'),
    url(r'^add_reportFile/', views.add_reportFile, name='add_reportFile'),
    url(r'^report/(?P<pk>\d+)$', views.reportDetail.as_view(), name='report_detail'),
    url(r'^groups/$', views.groups.as_view(), name='groups'),
    url(r'^suspend_user/', views.suspend_user, name='suspend_user'),
    url(r'^group/(?P<pk>\d+)$', views.group_detail.as_view(), name='group_detail'),
    url(r'^group/(?P<pk>\d+)/add_users_to_group', views.add_users_to_group, name='add_users_to_group'),
    url(r'^groups/remove_from_groups', views.remove_from_groups, name='remove_from_groups'),
    url(r'^groups/create_group', views.add_group, name='create_group'),
<<<<<<< HEAD
    url(r'^sm/add_sm/', views.add_sm, name='add_sm'),
    url(r'^sm/groups', views.sm_add_to_group, name='sm_add_to_group'),
=======
    url(r'^groups/choose_group_to_add_users', views.choose_group_to_add_users, name='choose_group_to_add_users'),
    url(r'^add_sm/', views.add_sm, name='add_sm'),
    url(r'^messages/$', views.messages.as_view(), name='messages'),
    url(r'^messages/(?P<pk>\d+)$', views.message_detail.as_view(), name='message_detail'),
>>>>>>> bf7ef3dd3199cb48dda48e084ae7ad75dd13fc26
]
