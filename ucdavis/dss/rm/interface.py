from Products.PluggableAuthService import interfaces
  
class IRmHelper(# -*- implemented plugins -*-
                    interfaces.plugins.IPropertiesPlugin,
                    interfaces.plugins.IUserEnumerationPlugin,
                    interfaces.plugins.IRolesPlugin,
                                ):
    """interface for RmHelper."""
