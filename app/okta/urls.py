from django.urls import include, path

from . import views

app_name = 'okta'
urlpatterns = [
    path('', views.index, name='index'),
    path('groups/list', views.group_list, name='group-list'),
    path('groups/sync', views.group_sync, name='group-sync'),
    path('task/oktagroup', views.TaskSyncOktaGroups, name='task-okta-group-sync')
]