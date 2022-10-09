# users/admin.py
from django.contrib import admin

from .models import OktaGroup, OktaUser

@admin.register(OktaGroup)
class OktaGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'okta_id', 'profile', 'source_type', 'source_system', 'member_count', 'created_date', 'updated_date')

@admin.register(OktaUser)
class OktaUserAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'login', 'title', 'secondEmail', 'profile', 'created_date', 'updated_date')
