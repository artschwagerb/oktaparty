# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import date, datetime
from dateutil import parser
import time

from .okta import OktaTools
from .models import OktaGroup, OktaUser

@shared_task
def okta_group_sync():
    okta = OktaTools()

    # query Okta groups
    okta_groups = okta.groups()

    # for each group from the Okta API
    for g in okta_groups:
        print("%s :: %s" % (g['id'],g['profile']['name']))

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
                'hidden': g['profile'].get('hidden', False),
                'lastUpdated': parser.parse(g['lastUpdated']),
                'lastMembershipUpdated': parser.parse(g['lastMembershipUpdated'])
            }
        )
        
        if group_created:
            # if the OktaGroup was created
            print("Group Created: %s" % (group_item))
        else:
            # if the Okta Group should be updated
            if parser.parse(g['lastUpdated']) != group_item.lastUpdated:
                print("lastUpdated... %s != %s" % (g['lastUpdated'],group_item.lastUpdated))
                group_item.name = g['profile']['name']
                group_item.description = g['profile'].get('description', None)
                group_item.profile = g['profile']
                group_item.source_type = g['type']
                group_item.source_system = g['objectClass'][0]
                group_item.allow_join = g['profile'].get('allowJoin', False)
                group_item.allow_leave = g['profile'].get('allowLeave', False)
                group_item.hidden = g['profile'].get('hidden', False)
                group_item.lastUpdated = parser.parse(g['lastUpdated'])
                group_item.lastMembershipUpdated = parser.parse(g['lastMembershipUpdated'])
                group_item.save()

            if parser.parse(g['lastMembershipUpdated']) != group_item.lastMembershipUpdated:
                print("lastUpdated... %s != %s" % (g['lastMembershipUpdated'],group_item.lastMembershipUpdated))
                group_item.members()
                time.sleep(1)

            #print("Group Updated: %s" % (group_item))
    
    # Delete 'Extra Groups' that don't exist in Okta anymore...
    # in some configurations, this may delete all groups.
    # make sure the okta call actually returns groups before deleting all the groups
    okta_group_ids = [g['id'] for g in okta_groups]
    if len(okta_group_ids) > 0:
        stale_okta_groups = OktaGroup.objects.exclude(okta_id__in=okta_group_ids)
        print("Stale Groups to Delete: %s" % (stale_okta_groups.count()))
        print(stale_okta_groups.delete())

@shared_task
def okta_user_sync():
    okta = OktaTools()

    # query Okta users
    okta_users = okta.users()

    # for each user from the Okta API
    for u in okta_users:

        # get or create the OktaGroup in the Django database
        user_item, user_created = OktaUser.objects.get_or_create(okta_id=u['id'],
            defaults={
                'firstName': u['profile'].get('firstName',None),
                'lastName': u['profile'].get('lastName',None),
                'profile': u['profile'],
                'email': u['profile'].get('email',None),
                'login': u['profile'].get('login',None),
                'title': u['profile'].get('title', None),
                'secondEmail': u['profile'].get('secondEmail', False),
            }
        )
        
        if user_created:
            # if the OktaUser was created
            print("User Created: %s" % (user_item))
        else:
            # if the Okta User should be updated
            user_item.firstName = u['profile'].get('firstName',None)
            user_item.lastName = u['profile'].get('lastName',None)
            user_item.profile = u['profile']
            user_item.email = u['profile'].get('email',None)
            user_item.login = u['profile'].get('login',None)
            user_item.title = u['profile'].get('title',None)
            user_item.secondEmail = u['profile'].get('secondEmail',None)
            
            user_item.save()

            print("User Updated: %s" % (user_item))