import logging
import requests
import json
from django.conf import settings

logging.basicConfig()
log = logging.getLogger(__name__)

OKTA_URL = settings.OKTA_URL
OKTA_TOKEN = settings.OKTA_TOKEN

class OktaTools(object):
    """Okta API Toolset"""
    def __init__(self):
        super(OktaTools, self).__init__()
        self.okta_url = "https://%s" % OKTA_URL
    
    def api_get(self, api_path, payload=None):
        """Wrapper for GET request"""
        log.debug("OKTA API: %s", api_path)

        headers = {
            'accept': 'application/json',
            'authorization': 'SSWS %s' % OKTA_TOKEN,
            'content-type': 'application/json'
        }

        if payload is None:
            payload = {}

        r = requests.get(url=self.okta_url + api_path,
                            params=payload,
                            headers=headers)
        log.debug(r.text)

        if r.links.get('next'):
            results = []
            results.extend(r.json())

            while r.links.get('next'):

                r = requests.get(url=r.links.get('next')['url'],
                                params=payload,
                                headers=headers)
                log.debug(r.text)
                results.extend(r.json())

            return results
            
        else:
            return r.json()
    
    def api_put(self, api_path, payload=None):
        """Wrapper for PUT request"""
        log.debug("OKTA API: %s", api_path)

        headers = {
            'accept': 'application/json',
            'authorization': 'SSWS %s' % OKTA_TOKEN,
            'content-type': 'application/json'
        }

        if payload is None:
            payload = {}
        if isinstance(payload, dict):
            payload = json.dumps(payload)

        r = requests.put(url=self.okta_url + api_path,
                            data=payload,
                            headers=headers)
        log.debug(r.text)

        return r.text
    
    def api_post(self, api_path, payload=None):
        """Wrapper for POST request"""
        log.debug("OKTA API: %s", api_path)

        headers = {
            'accept': 'application/json',
            'authorization': 'SSWS %s' % OKTA_TOKEN,
            'content-type': 'application/json'
        }

        if payload is None:
            payload = {}
        if isinstance(payload, dict):
            payload = json.dumps(payload)

        r = requests.post(url=self.okta_url + api_path,
                            data=payload,
                            headers=headers)
        log.debug(r.text)

        return r.json()
    
    def api_delete(self, api_path, payload=None):
        """Wrapper for DELETE request"""
        log.debug("OKTA API: %s", api_path)

        headers = {
            'accept': 'application/json',
            'authorization': 'SSWS %s' % OKTA_TOKEN,
            'content-type': 'application/json'
        }

        if payload is None:
            payload = {}

        r = requests.delete(url=self.okta_url + api_path,
                            params=payload,
                            headers=headers)
        log.debug(r.text)

        return r.text

    def users(self, payload=None):
        """List Users
        https://developer.okta.com/docs/reference/api/users/#list-users"""

        api_path = "/api/v1/users"
        data = self.api_get(api_path, payload)
        return data
    
    def user(self, user_id):
        """Get User by id, email, username
        https://developer.okta.com/docs/reference/api/users/#get-user-s-groups"""

        api_path = "/api/v1/users/%s" % user_id
        data = self.api_get(api_path)
        return data
    
    def user_applinks(self, user_id):
        """Get User AppLinks
        https://developer.okta.com/docs/reference/api/users/#get-assigned-app-links"""

        api_path = "/api/v1/users/%s/appLinks" % user_id
        data = self.api_get(api_path)
        return data
    
    def user_groups(self, user_id):
        """Get User Groups
        https://developer.okta.com/docs/reference/api/users/#get-user-s-groups"""

        api_path = "/api/v1/users/%s/groups" % user_id
        data = self.api_get(api_path)
        return data
    
    def user_update(self, user_id, payload):
        """Update User Profile
        https://developer.okta.com/docs/reference/api/users/#update-profile-with-id"""

        api_path = "/api/v1/users/%s" % user_id
        data = self.api_post(api_path, payload)
        return data
    
    def groups(self, payload=None):
        """List Groups
        https://developer.okta.com/docs/reference/api/groups/#list-groups"""

        api_path = "/api/v1/groups"
        data = self.api_get(api_path, payload)
        return data
    
    def group(self, group_id):
        """Get Group
        https://developer.okta.com/docs/reference/api/groups/#get-group"""

        api_path = "/api/v1/groups/%s" % group_id
        data = self.api_get(api_path)
        return data
    
    def group_update(self, group_id, payload):
        """Update Group Profile
        https://developer.okta.com/docs/reference/api/groups/#update-group
        
        payload = {
            "profile": {
                "name": name,
                "description": description
            }
        }
        """

        api_path = "/api/v1/groups/%s" % group_id
        data = self.api_put(api_path, payload)
        return data
    
    def group_delete(self, group_id):
        """Delete Group
        https://developer.okta.com/docs/reference/api/groups/#remove-group"""

        api_path = "/api/v1/groups/%s" % group_id
        data = self.api_delete(api_path)
        return data
    
    def group_create(self, payload):
        """Add Group
        https://developer.okta.com/docs/reference/api/groups/#add-group
        
        payload = {
            "profile": {
                "name": name,
                "description": description
            }
        }
        """

        api_path = "/api/v1/groups"

        data = self.api_post(api_path, payload)
        return data
    
    def group_users(self, group_id):
        """List Group Users
        https://developer.okta.com/docs/reference/api/groups/#list-group-members"""

        api_path = "/api/v1/groups/%s/users" % group_id
        data = self.api_get(api_path)
        return data
    
    def group_users_add(self, group_id, user_id):
        """Add User to Group
        https://developer.okta.com/docs/reference/api/groups/#add-user-to-group"""

        api_path = "/api/v1/groups/%s/users/%s" % (group_id, user_id)
        data = self.api_put(api_path)
        return data
    
    def group_users_remove(self, group_id, user_id):
        """Remove User from Group
        https://developer.okta.com/docs/reference/api/groups/#remove-user-from-group"""

        api_path = "/api/v1/groups/%s/users/%s" % (group_id, user_id)
        data = self.api_delete(api_path)
        return data
    
    def group_apps(self, group_id):
        """List Group Apps
        https://developer.okta.com/docs/reference/api/groups/#list-assigned-applications"""

        api_path = "/api/v1/groups/%s/apps" % group_id
        data = self.api_get(api_path)
        return data
    
    def group_rules(self, payload=None):
        """List Group Rules
        https://developer.okta.com/docs/reference/api/groups/#list-group-rules"""

        api_path = "/api/v1/groups/rules"
        data = self.api_get(api_path, payload)
        return data
    
    def group_rule(self, rule_id):
        """Get Group Rule
        https://developer.okta.com/docs/reference/api/groups/#get-group-rule"""

        api_path = "/api/v1/groups/rules/%s" % rule_id
        data = self.api_get(api_path)
        return data

    def app_list(self, payload=None):
        """List Apps
        https://developer.okta.com/docs/reference/api/apps/#list-applications"""

        api_path = "/api/v1/apps"
        data = self.api_get(api_path)
        return data
    
    def app(self, app_id):
        """Get App
        https://developer.okta.com/docs/reference/api/apps/#get-application"""

        api_path = "/api/v1/apps/%s" % app_id
        data = self.api_get(api_path)
        return data