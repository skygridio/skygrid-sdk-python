from requests import request
import json
import urllib

class RestApi(object):
  def __init__(self,address,project_id):
    self._address = address;
    self._project_id = project_id
    self._token = None;
    self._master_key = None

    self._endPoints = {
      'getServerTime': get_server_time,
      'login':login,
      'logout':logout,
      'loginMaster':login_master,
      'signup':signup,
      'fetchUser':fetch_user,
      'findUsers':find_users,
      'deleteUser':delete_user,
      'requestPasswordReset':request_password_reset,
      'resetPassword':reset_password,
      'fetchProject':fetch_project,
      'updateProject':update_project,
      'addDeviceSchema':add_device_schema,
      'findDeviceSchemas':find_device_schemas,
      'fetchDeviceSchema':fetch_device_schema,
      'updateDeviceSchema':update_device_schema,
      'deleteDeviceSchema':delete_device_schema,
      'findDevices':find_devices,
      'addDevice':add_device,
      'fetchDevice':fetch_device,
      'updateDevice':update_device,
      'deleteDevice':delete_device,
      'fetchHistory':fetch_history
    }

  def _fetchJson(self,url,params):
    if ('headers' not in params):
      params['headers'] = {}
    params['headers']['Accept'] = 'application/json'
    params['headers']['Content-Type'] = 'application/json'

    if(self._token):
      params['headers']['X-Access-Token'] = self._token
    else:
      if(self._master_key):
        params['headers']['X-Master-Key'] = self._master_key
      params['headers']['X-Project-ID'] = self._project_id

    fullUrl = self._address + url
    data = ''
    if 'body' in params:
      data = json.dumps(params['body'])
      
    r = request(
      params.get('method','').upper(),
      fullUrl,
      headers=params.get('headers',{}),
      data=data)
    r.raise_for_status()
    return parseJSON(r)

  def close(self):
    pass

  def request(self,name,data=None):
    if(name not in self._endPoints):
      raise Exception('API end point {} does not exist on the REST API'.format(name))

    return self._endPoints[name](self,data)
    
# endpoints
def get_server_time(self,data):
  return self._fetchJson('/time', {'method':'get'})

def signup(self,data):
  return self._fetchJson('/users',{
    'method':'post',
    'body':data
  })
  
def login(self,data):
  response = self._fetchJson('/login',{
    'method':'post',
    'body':data
  })
  self._token = response.json().get('token',None)
  return response

def logout(self,data):
  return self._fetchJson('/logout',{'method':'post'})

def login_master(self,data):
  self._master_key = data.get('masterKey','')
  return {
    # HACK: to not cause an error in parseJSON
    'status_code':204
  }

def fetch_user(self,data):
  return self._fetchJson('/users/{}'.format(data['userId']),{'method':'get'})

def find_users(self,data):
  return self._fetchJson(
    generateQueryUrl('/users',data.get('constraints',{})),
    {'method':'get'}
  )

def delete_user(self,data):
  return self._fetchJson(
    '/users/{}'.format(data['userId']),
    { 'method' : 'delete'}
  )
  
def request_password_reset(self,data):
  return self._fetchJson(
    '/users/requestPasswordReset',
    { 'method' : 'post', 'body' : data}
  )
  
def reset_password(self,data):
  return self._fetchJson(
    '/users/resetPassword',
    { 'method' : 'post', 'body' : data}
  )
  
def fetch_project(self,data):
  return self._fetchJson(
    '/projects/{}'.format(data['projectId']),
    { 'method' : 'get'}
  )

def update_project(self,data):
  return self._fetchJson(
    '/projects/{}'.format(data['projectId']),
    { 'method' : 'put', 'body' : data}
  )

def add_device_schema(self,data):
  return self._fetchJson(
    '/schemas',
    { 'method' : 'post', 'body' : data}
  )
  
def find_device_schemas(self,data):
  return self._fetchJson(
    generateQueryUrl('/schemas',data.get('constraints',{})),
    { 'method' : 'get'}
  )
  
def fetch_device_schema(self,data):
  return self._fetchJson(
    '/schemas/{}'.format(data['schemaId']),
    { 'method' : 'get'}
  )

def update_device_schema(self,data):
  schemaId = data['schemaId']
  data.pop('schemaId')
  return self._fetchJson(
    '/schemas/{}'.format(schemaId),
    { 'method' : 'put', 'body': data}
  )

def delete_device_schema(self,data):
  return self._fetchJson(
    '/schemas/{}'.format(data['schemaId']),
    { 'method' : 'delete' }
  )

def find_devices(self,data):
  return self._fetchJson(
    generateQueryUrl('/devices',data.get('constraints',{})),
    { 'method' : 'get' }
  )
  
def add_device(self,data):
  return self._fetchJson(
    '/devices',
    { 'method' : 'post', 'body' : data }
  )

def fetch_device(self,data):
  return self._fetchJson(
    '/devices/{}'.format(data['deviceId']),
    { 'method' : 'get' }
  )

def update_device(self,data):
  deviceId = data['deviceId']
  data.pop('deviceId')
  return self._fetchJson(
    '/devices/{}'.format(deviceId),
    { 'method' : 'put', 'body' : data}
  )

def delete_device(self,data):
  return self._fetchJson(
    '/devices/{}'.format(data['deviceId']),
    { 'method' : 'delete' }
  )

def fetch_history(self,data):
  return self._fetchJson(
    '/history/{}'.format(data['deviceId']),
    { 'method' : 'get' }
  )
# end endpoints

def parseJSON(r):
  if(r.status_code != 204):
    return r.json()
  return {}
  
def generateQueryUrl(url, queries):
	if (queries):
    #http://stackoverflow.com/questions/946170/equivalent-javascript-functions-for-pythons-urllib-quote-and-urllib-unquote
		url += '?where=' + urllib.quote(json.dumps(queries), safe='~()*!.\'');
	return url
