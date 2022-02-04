# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date, datetime
import time

from .okta import OktaTools
from .models import OktaGroup

@shared_task
def okta_group_sync():
    okta = OktaTools()

    # query Okta groups
    okta_groups = okta.groups()

    # for each group from the Okta API
    for g in okta_groups:

        # get or create the OktaGroup in the Django database
        group_item, group_created = OktaGroup.objects.get_or_create(okta_id=g['id'],
            defaults={
                'name': g['profile']['name'],
                'description': g['profile'].get('description',None),
                'profile': g['profile'],
                'source_type': g['type'],
                'source_system': g['objectClass'][0],
                'allow_join': g['profile'].get('allowJoin', False),
                'allow_leave': g['profile'].get('allowLeave', False),
                'hidden': g['profile'].get('hidden', False)
            }
        )
        
        if group_created:
            # if the OktaGroup was created
            print("Group Created: %s" % (group_item))
        else:
            # if the Okta Group should be updated
            group_item.name = g['profile']['name']
            group_item.description = g['profile'].get('description', None)
            group_item.profile = g['profile']
            group_item.source_type = g['type']
            group_item.source_system = g['objectClass'][0]
            group_item.allow_join = g['profile'].get('allowJoin', False)
            group_item.allow_leave = g['profile'].get('allowLeave', False)
            group_item.hidden = g['profile'].get('hidden', False)
            
            group_item.save()

            print("Group Updated: %s" % (group_item))