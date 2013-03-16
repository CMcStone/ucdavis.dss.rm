from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_rm_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_rm_form' )


def manage_add_rm_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add a UC Davis DSS Roles Management Helper to the PluggableAuthentication Service."""

    sp = plugin.RmHelper( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'rmHelper+added.'
                                      % dispatcher.absolute_url() )


def register_rm_plugin():
    try:
        registerMultiPlugin(plugin.RmHelper.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_rm_plugin_class(context):
    context.registerClass(plugin.RmHelper,
                          permission = manage_users,
                          constructors = (manage_add_rm_form,
                                          manage_add_rm_helper),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
