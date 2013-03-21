from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

import requests

from OFS.Cache import Cacheable
from Products.PluggableAuthService.utils import createViewName



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
        user_info = s.get(dssrm_url + 'people/' + str(principal) + '.json',verify=False).json()
        if user_info:
          roles = [role['token'] for role in user_info['roles'] if role['application_id'] == int(application_id)]
          self.ZCacheable_set(roles, view_name=view_name)
          return roles
        else:
          return []
