from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
import requests

class PropertiesPlugin(BasePlugin):
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

        dssrm_url = self.dssrm_url
        application_id = self.application_id
        api_username = self.api_username
        api_key = self.api_key

        s = requests.Session()
        s.auth = (api_username,api_key)

        user_info = s.get(dssrm_url + 'people/' + user.getId() + '.json',verify=False).json()
        if user_info:
          properties = {'email':user_info['email'],
                        'fullname':user_info['name']}
          return properties
        else:
          return {'email':'jeremy@ucdavis.edu','fullname':"Foo Bar Baz"}
