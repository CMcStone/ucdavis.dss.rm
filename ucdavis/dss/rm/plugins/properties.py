from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
import requests

from OFS.Cache import Cacheable
from Products.PluggableAuthService.utils import createViewName

class PropertiesPlugin(BasePlugin, Cacheable):
    """ Return a property set for a user.
    """
    security = ClassSecurityInfo()

    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """ user -> {}

        o User will implement IPropertiedUser.

        o Plugin should return a dictionary or an object providing
          IPropertiesPlugin.

        o Plugin may scribble on the user, if needed (but must still
          return a mapping, even if empty).

        o May assign properties based on values in the REQUEST object, if
          present
        """

        #add your code here

        view_name = createViewName('getPropertiesForUser',user.getId())
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

        user_info = s.get(dssrm_url + 'api/people/' + user.getId() + '.json',verify=False).json()

        if user_info:
          properties = {'email':user_info['email'],
                        'fullname':user_info['name']}
          self.ZCacheable_set(properties,view_name=view_name)
          return properties
        else:
          return {}
