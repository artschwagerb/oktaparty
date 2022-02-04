from django.urls import include, path

from . import views

app_name = 'core'
urlpatterns = [
    path('reset-password', views.reset_password, name='reset-password'),
]