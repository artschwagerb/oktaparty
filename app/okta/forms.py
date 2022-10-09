from django import forms
from django import forms

from .models import OktaGroup

class GroupEditForm(forms.ModelForm):
    name = forms.CharField(label="Name"),
    description = forms.CharField(label="Description"),
    okta_id = forms.CharField(label="Okta Group ID"),
    allow_join = forms.BooleanField(label='Users can Join', help_text="Allow users to add themselves to the group.", required=False)
    allow_leave = forms.BooleanField(label='Users can Leave', help_text="Allow users to remove themselves from the group.", required=False)
    hidden = forms.BooleanField(label='Hide from Users', help_text="Keep this group a secret?", required=False)
    active = forms.BooleanField(label='Active', required=False)

    class Meta:
        model = OktaGroup
        fields = ['name', 'description', 'okta_id', 'allow_join', 'allow_leave', 'hidden', 'active']