"""Class: RmHelper
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import interface
import plugins

class RmHelper( # -*- implemented plugins -*-
                    plugins.properties.PropertiesPlugin,
                    plugins.user_enumeration.UserEnumerationPlugin,
                    plugins.roles.RolesPlugin,
                               ):
    """Multi-plugin

    """

    meta_type = 'DSS Roles Management Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title



classImplements(RmHelper, interface.IRmHelper)

InitializeClass( RmHelper )
