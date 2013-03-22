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

        application = s.get(dssrm_url + 'applications/' + application_id + '.json',verify=False).json()

        appRoles = [{role['token']:[member['loginid'] for member in role['members']]} for role in application['roles']]
        userRoles = []
        for role in appRoles:
          if str(principal) in role.values()[0]:
            userRoles.extend([key for key in role.keys()])
        self.ZCacheable_set(userRoles, view_name=view_name)
        return userRoles

