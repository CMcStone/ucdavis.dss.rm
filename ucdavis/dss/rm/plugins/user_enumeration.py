from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
import requests

from OFS.Cache import Cacheable
from Products.PluggableAuthService.utils import createViewName

class UserEnumerationPlugin(BasePlugin, Cacheable):
    """Allow querying users by ID, and searching for users.

    o XXX:  can these be done by a single plugin?
    """

    security = ClassSecurityInfo()

    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self,
                       id=None,
                       login=None,
                       exact_match=False,
                       sort_by=None,
                       max_results=None,
                       **kw):
        """-> ( user_info_1, ... user_info_N )

        o Return mappings for users matching the given criteria.

        o 'id' or 'login', in combination with 'exact_match' true, will
          return at most one mapping per supplied ID ('id' and 'login'
          may be sequences).

        o If 'exact_match' is False, then 'id' and / or login may be
          treated by the plugin as "contains" searches (more complicated
          searches may be supported by some plugins using other keyword
          arguments).

        o If 'sort_by' is passed, the results will be sorted accordingly.
          known valid values are 'id' and 'login' (some plugins may support
          others).

        o If 'max_results' is specified, it must be a positive integer,
          limiting the number of returned mappings.  If unspecified, the
          plugin should return mappings for all users satisfying the criteria.

        o Minimal keys in the returned mappings:

          'id' -- (required) the user ID, which may be different than
                  the login name

          'login' -- (required) the login name

          'pluginid' -- (required) the plugin ID (as returned by getId())

          'editurl' -- (optional) the URL to a page for updating the
                       mapping's user

        o Plugin *must* ignore unknown criteria.

        o Plugin may raise ValueError for invalid criteria.

        o Insufficiently-specified criteria may have catastrophic
          scaling issues for some implementations.
        """

        #add your code here

        cachekey = { 'id' : id,
                     'login' : login,
                     'exact_match' : exact_match,
                     'sort_by' : sort_by,
                     'max_results' : max_results,
                     'kwargs' : kw
                   }

        view_name = createViewName('enumerateUsers',cachekey)
        cached_info = self.ZCacheable_get(view_name)
        if cached_info is not None:
          return cached_info

        dssrm_url = self.dssrm_url
        application_id = self.application_id
        api_username = self.api_username
        api_key = self.api_key

        s = requests.Session()
        s.auth = (api_username,api_key)

        # Plone may search by either login or id, but they're always the same
        if id == None and login != None:
          id=login
        if login == None and id != None:
          login=id

        if exact_match:
            user = s.get(dssrm_url + 'people/' + login + '.json',verify=False).json()
            if user:
                userdict = {'id':user['loginid'],
                            'login':user['loginid'],
                            'pluginid':self.getId(),
                            'editurl':dssrm_url + 'applications/#/entities/' + str(user['id']),
                            'fullname':user['name']
                           }
                self.ZCacheable_set([userdict],view_name=view_name)
                return [userdict]
            else:
                return [{}]

        application = s.get(dssrm_url + 'applications/' + application_id + '.json',verify=False).json()
        members = []
        for role in application['roles']:
          for member in role['members']:
            if member['id'] not in [m['id'] for m in members]:
              members.append({'id':member['loginid'],
                              'login':member['loginid'],
                              'pluginid':self.getId(),
                              'editurl':dssrm_url + 'applications/#/entities/' + str(member['id']),
                              'fullname':member['name']
                             })
        if 'name' in kw.keys():
          members = [member for member in members if kw['name'].upper() in member['fullname'].upper()]
        if sort_by:
          members = sorted(members, key=lambda k: k['login'])
        if max_results:
          members = members[0:max_results]
        self.ZCacheable_set(members,view_name=view_name)
        return members
