# users/admin.py
from django.contrib import admin

from .models import OktaGroup

@admin.register(OktaGroup)
class OktaGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'okta_id', 'profile', 'source_type', 'source_system', 'member_count')
