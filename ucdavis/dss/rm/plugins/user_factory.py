from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from Products.PlonePAS.plugins.ufactory import PloneUser

class UserFactoryPlugin(BasePlugin):
    """Create a new IPropertiedUser.
    """

    security = ClassSecurityInfo()

    security.declarePrivate('createUser')
    def createUser(self, user_id, name):
        """ Return a user, if possible.

        o Return None to allow another plugin, or the default, to fire.
        """

        #add your code here
        return PloneUser(user_id, name)

