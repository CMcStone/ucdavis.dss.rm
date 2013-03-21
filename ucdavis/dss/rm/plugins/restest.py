import requests

dssrm_url = 'https://roles.dss.ucdavis.edu/'
application_id = '32'
api_username = 'Plone'
api_key = '8c50f2641a9f5fc5a6d6733ac3f646a6'


s = requests.Session()
s.auth = (api_username,api_key)
users = s.get(dssrm_url + 'applications/' + application_id + '.json').json()

role_ids = [roles['id'] for roles in users['roles']]

print roles

user_ids = []
group_ids = []
for role_id in role_ids:
  role = s.get(dssrm_url + 'roles/' + str(role_id) + '.json').json()
  user_ids = user_ids + ([user['id'] for user in role['entities'] if user['type'] == u'Person'])
  group_ids = group_ids + ([group['id'] for group in role['entities'] if user['type'] == u'Group'])

print user_ids
print group_ids

users = []
for user_id in user_ids:
  user = s.get(dssrm_url + 'people/' + str(user_id) + '.json').json()
  users.append({'id':user['loginid'],
                'login':user['loginid'],
                'pluginid':'dssrm',
                'editurl':dssrm_url + 'applications/#/entities/' + str(user['id'])
               })

for group_id in group_ids:
  group = s.get(dssrm_url + 'groups/' + str(group_id) + '.json').json()
  members = group['members']
  for member in members:
    users.append({'id':member['loginid'],
                  'login':member['loginid'],
                  'pluginid':'dssrm',
                  'editurl':dssrm_url + 'applications/#/entities/' + str(member['id'])
                 })

print users




user =  s.get(dssrm_url + 'people/' + 'jeremy' + '.json').json()
roles = [role['token'] for role in user['roles'] if role['application_id'] == int(application_id)]

print roles

properties = {'email':user['email'],
              'fullname':user['name']}

print properties
