from django.urls import include, path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('reset-password', views.reset_password, name='reset-password'),
]