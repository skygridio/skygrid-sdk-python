from skygrid import API_BASE

from .api import Api
from .device import Device
from .schema import Schema
from .user import User


class Project(object):

  def __init__(self, project_id=None, address=None, api=None, master_key=None):
    self._api = Api()

    if api == None:
      api = 'websocket'

    if address == None:
      address = API_BASE

    self._project_id = project_id
    self._master_key = master_key
    #self._subscriptions = {};

    self._api.setup(address, api, project_id, master_key)


  def login(self, email, password):
    data = self._api.request('login', {'email': email, 'password': password})

    if 'token' in data:
      self._user = { 'email': email,
                     'id': data['userId'],
                     'token': data['token'] }

    elif type(data) is str:
      raise Exception(data)

    else:
      raise Exception('Unable to log in')
    
  
  def login_master(self, master_key):
    pass


  def logout(self):
    self._api.request('logout')
    self._user = None


  def signup(self, email, password, meta=None):
    data = self._api.request('signup', {'email': email, 'password': password, 'meta': meta})

    if 'id' in data:
      return self.user(data['id']).fetch()
    
    elif type(data) is str:
      raise Exception(data)
    
    else:
      raise Exception('Unable to create new user')


  def user(self, user_id):
    return User(self._api, user_id)


  def users(self, constraints={}, fetch = True):
    users = self._api.request('findUsers', {'constraints': constraints, 'fetch': fetch})

    for index, user in enumerate(users):
      users[index] = self.user(user)

    return users


  def add_schema(self, data):
    schema = self._api.request('addDeviceSchema', data)
    schema = self.schema(schema['id']).fetch()

    return schema


  def schema(self, schema_id):
    return Schema(self._api, schema_id)
  

  def schemas(self, constraints={}, fetch = True):
    schemas = self._api.request('findDeviceSchemas', {'constraints': constraints, 'fetch': fetch})

    for index, schema in enumerate(schemas):
      schemas[index] = self.schema(schema)

    return schemas


  def add_device(self, data):
    if type(data['schema']) is dict:
      data['schemaId'] = data['schema']['id']
    else:
      data['schemaId'] = data['schema']

    data.pop('schema', None)

    device = self._api.request('addDevice', data)

    return self.device(device['id']).fetch()


  def device(self, device_id):
    return Device(self._api, device_id)


  def devices(self, constraints={}, fetch=True):
    devices = self._api.request('findDevices', {'constraints': constraints, 'fetch': fetch})

    for index, device in enumerate(devices):
      devices[index] = self.device(device)

    return devices

  #   /**
  #  * Finds devices that adhere to the specified constraints.
  #  * @param  {object}  [constraints] The constraints to apply to the search.
  #  * @param  {Boolean} [fetch]  Determines whether the full device object should be fetched, or just the description.  Defaults to true.
  #  * @returns {Promise<Device, SkyGridException>} A promise that resolves to an array of all devices that were found.
  #  */
  # devices(constraints, fetch = true) {
  #   return this._api.request('findDevices', { 
  #     constraints: constraints,
  #     fetch: fetch
  #   }).then(devices => {
  #     return devices.map(item => {
  #       return this.device(item);
  #     });
  #   });
  # }

  # subscribe(settings, callback) {
  #   this._subscriptionManager.addSubscription(settings, callback);
  # }

  # removeSubscriptions() {
  #   return this._subscriptionManager.removeSubscriptions();
  # }

  # close() {
  #   return this.removeSubscriptions().then(() => {
  #     return this._api.close();
  #   }).then(() => {
  #     this._projectId = null;
  #     this._masterKey = null;
  #     this._user = null;
  #   });
  # }