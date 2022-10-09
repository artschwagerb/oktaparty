from django.db import models
from users.models import User

from .okta import OktaTools

# Create your models here.
class OktaGroup(models.Model):
    """Okta Group"""

    # Fields
    name = models.CharField(max_length=255, help_text='Enter a name')
    description = models.TextField(help_text='Describe the group', null=True, blank=True)

    profile = models.JSONField()
    okta_id = models.CharField(max_length=100, null=True, blank=True)

    #email = models.CharField(max_length=255, help_text='name@stackoverflow.com', null=True, blank=True)
    #type = models.CharField(max_length=100, null=True, blank=True)

    source_system = models.CharField(max_length=255, null=True, blank=True)
    source_type = models.CharField(max_length=255, null=True, blank=True)

    member_count = models.IntegerField(default=0)
    
    allow_join = models.BooleanField(default=False)
    allow_leave = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    lastUpdated = models.DateTimeField(null=True, blank=True)
    lastMembershipUpdated = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Metadata
    class Meta: 
        ordering = ['name']
        permissions = (
            ("list_groups", "Can List Groups"),
        )
    
    def __str__(self):
        """String for representing the OktaGroup object (in Admin site etc.)."""
        return "%s (Okta ID: %s)" % (self.name, self.okta_id)
    
    def source_system_pretty(self):
        if self.source_system == 'okta:windows_security_principal':
            return "Active Directory"
        else:
            return "Okta"
    
    def join(self, user_item):
        okta = OktaTools()
        okta.group_users_add(self.okta_id, user_item.okta_id)
    
    def leave(self, user_item):
        okta = OktaTools()
        okta.group_users_remove(self.okta_id, user_item.okta_id)
    
    def members(self):
        okta = OktaTools()

        # Group Members
        okta_users = okta.group_users(self.okta_id)
        okta_user_ids = [user['id'] for user in okta_users]

        self.member_count = len(okta_users)
        self.save()

        user_list = OktaUser.objects.filter(okta_id__in=okta_user_ids)

        return user_list

class OktaUser(models.Model):
    """Okta User"""

    # Fields
    okta_id = models.CharField(max_length=100, null=True, blank=True)

    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    login = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    secondEmail = models.CharField(max_length=255, null=True, blank=True)

    profile = models.JSONField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Metadata
    class Meta: 
        ordering = ['email']
        permissions = (
            ("list_users", "Can List Users"),
        )
    
    def __str__(self):
        """String for representing the OktaUser object (in Admin site etc.)."""
        return "%s (Okta ID: %s)" % (self.email, self.okta_id)
    
    def groups(self):
        okta = OktaTools()
        user_groups = okta.user_groups(self.okta_id)
        user_group_ids = [g['id'] for g in user_groups]
        user_group_list = OktaGroup.objects.filter(okta_id__in=user_group_ids)

        return user_group_list