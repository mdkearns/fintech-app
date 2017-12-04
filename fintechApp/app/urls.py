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
	url(r'^get_report_files', views.get_report_files, name='get_report_files'),
    url(r'^create_report/', views.add_report, name='create_report'),
    url(r'^add_reportFile/', views.add_reportFile, name='add_reportFile'),
    url(r'^star_report/(?P<reportId>[\w ]+)/(?P<view>[\w ]+)$', views.starReport, name='star_report'),
    url(r'^add_file_to_report/(?P<reportId>\d+)$', views.addFileToReport, name='add_file_to_report'),
    url(r'^add_new_file_to_report/(?P<reportId>\d+)$', views.addNewFileToReport, name='add_new_file_to_report'),
    url(r'^report/(?P<pk>\d+)$', views.reportDetail.as_view(), name='report_detail'),
    url(r'^report/(?P<pk>\d+)/edit_report$', views.sm_edit_report, name='edit_report'),
    url(r'^groups/$', views.groups.as_view(), name='groups'),
    url(r'^suspend_user/', views.suspend_user, name='suspend_user'),
    url(r'^group/(?P<pk>\d+)$', views.group_detail.as_view(), name='group_detail'),
    url(r'^group/add_users_to_group/(?P<groupId>[\w ]+)$', views.add_users_to_group, name='add_users_to_group'),
    url(r'^groups/delete_message/(?P<groupId>[\w ]+)$', views.remove_from_group, name='remove_from_group'),
    url(r'^groups/create_group', views.add_group, name='create_group'),
    url(r'^groups/add_report_to_group', views.add_report_to_group, name='add_report_to_group'),
    url(r'^sm/add_sm/', views.add_sm, name='add_sm'),
    url(r'^sm/groups', views.sm_add_to_group, name='sm_add_to_group'),
    url(r'^sm/delete_report/', views.delete_report, name='sm_delete_report'),
    url(r'^sm/access_report/', views.access_report, name='sm_access_report'),
    url(r'^sm/edit_report/', views.edit_report, name='sm_edit_report'),
    url(r'^messages/$', views.messages.as_view(), name='messages'),
    url(r'^messages/(?P<pk>\d+)$', views.message_detail.as_view(), name='message_detail'),
    url(r'^messages/send_message$', views.send_message, name='send_message'),
    url(r'^messages/delete_message/(?P<messageId>[\w ]+)$', views.delete_message, name='delete_message'),
    url(r'^messages/decrypt_message/(?P<messageId>[\w ]+)$', views.decrypt_message, name='decrypt_message')
]
