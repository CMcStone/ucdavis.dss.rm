"""Class: RmHelper
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import interface
import plugins

from OFS.Cache import Cacheable

class RmHelper( # -*- implemented plugins -*-
                    plugins.user_factory.UserFactoryPlugin,
                    plugins.properties.PropertiesPlugin,
                    plugins.user_enumeration.UserEnumerationPlugin,
                    plugins.roles.RolesPlugin,
                    BasePlugin, Cacheable      ):
    """Multi-plugin

    """

    meta_type = 'DSS Roles Management Helper'
    security = ClassSecurityInfo()


    _properties = BasePlugin._properties + (
            {'id'    : 'dssrm_url',
             'label' : 'Base URL for DSS RM Server',
             'type'  : 'string',
             'mode'  : 'w',
            },
            {'id'    : 'application_id',
             'label' : 'Numeric ID for application associated with Plone instance',
             'type'  : 'string',
             'mode'  : 'w',
            },
            {'id'    : 'api_username',
             'label' : 'Username for RM API Key',
             'type'  : 'string',
             'mode'  : 'w',
            },
            {'id'    : 'api_key',
             'label' : 'RM API Key',
             'type'  : 'string',
             'mode'  : 'w',
            })


    def __init__( self, id, title=None, dssrm_url=None, application_id=None,
                  api_username=None, api_key=None ):
        self._setId( id )
        self.title = title
        if dssrm_url:
            self.dssrm_url = dssrm_url
        if application_id:
            self.application_id = application_id
        if api_username:
            self.api_username = api_username
        if api_key:
            self.api_key = api_key

    manage_options = (
                      BasePlugin.manage_options
                      + Cacheable.manage_options
                      )

classImplements(RmHelper, interface.IRmHelper)

InitializeClass( RmHelper )
