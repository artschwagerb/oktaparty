from django.urls import include, path

from . import views

app_name = 'okta'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/list', views.group_list, name='group-list'),
    path('group/yours', views.group_yours, name='group-yours'),
    path('group/<int:group_id>/join', views.group_join, name='group-join'),
    path('group/<int:group_id>/leave', views.group_leave, name='group-leave'),
    #path('groups/sync', views.group_sync, name='group-sync'),
    path('task/okta-group-sync', views.TaskSyncOktaGroups, name='task-okta-group-sync')
]