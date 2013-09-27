from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

import requests

from OFS.Cache import Cacheable
from Products.PluggableAuthService.utils import createViewName

import logging

logger = logging.getLogger("Plone")


class RolesPlugin(BasePlugin, Cacheable):
    """Determine the (global) roles which a user has.
    """
    security = ClassSecurityInfo()

    security.declarePrivate('getRolesForPrincipal')
    def getRolesForPrincipal(self, principal, request=None):
        """principal -> (role_1, ... role_N)

        o Return a sequence of role names which the principal has.

        o May assign roles based on values in the REQUEST object, if present.
        """

        #add your code here

        view_name = createViewName('getRolesForPrincipal',principal)
        cached_info = self.ZCacheable_get(view_name)
        if cached_info is not None:
          return cached_info

        dssrm_url = self.dssrm_url
        application_id = self.application_id
        api_username = self.api_username
        api_key = self.api_key

        s = requests.Session()
        s.auth = (api_username,api_key)
        s.headers.update({'Accept':'application/vnd.roles-management.v1'})

        person = s.get(dssrm_url + 'api/people/' + str(principal) + '.json',verify=False).json()

        userRoles = [role['name'] for role in person['role_assignments'] if int(role['application_id']) == int(application_id)]
        self.ZCacheable_set(userRoles, view_name=view_name)

        return userRoles
