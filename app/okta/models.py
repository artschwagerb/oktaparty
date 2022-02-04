from django.db import models

# Create your models here.
class OktaGroup(models.Model):
    """A typical class defining a model, derived from the Model class."""

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

    active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Metadata
    class Meta: 
        ordering = ['name']
        permissions = (
        )
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s (Okta ID: %s)" % (self.name, self.okta_id)