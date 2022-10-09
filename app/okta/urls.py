from django.urls import include, path

from . import views

app_name = 'okta'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/list', views.group_list, name='group-list'),
    path('group/owned', views.group_owned, name='group-owned'),
    path('group/roles', views.group_roles, name='group-roles'),
    path('group/yours', views.group_yours, name='group-yours'),
    path('group/<int:group_id>', views.group_view, name='group-view'),
    path('group/<int:group_id>/edit', views.group_edit, name='group-edit'),
    path('group/<int:group_id>/join', views.group_join, name='group-join'),
    path('group/<int:group_id>/leave', views.group_leave, name='group-leave'),
    path('user/list', views.user_list, name='user-list'),
    path('user/<int:user_id>', views.user_view, name='user-view'),
    path('task/okta-group-sync', views.TaskSyncOktaGroups, name='task-okta-group-sync'),
    path('task/okta-user-sync', views.TaskSyncOktaUsers, name='task-okta-user-sync')
]