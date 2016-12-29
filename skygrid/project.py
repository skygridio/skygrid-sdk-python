from skygrid import API_BASE, SOCKETIO_BASE, DEFAULT_API

from .socket_api import SocketApi
from .device import Device
from .schema import Schema
from .subscription_manager import SubscriptionManager
from .user import User

from pyee import EventEmitter


class Project(object):

  _emitter = EventEmitter()
  _self = None

  def __init__(self, project_id, address=None, api=None, master_key=None):
    _self = self

    if api == None:
      api = DEFAULT_API


    if api is 'websocket':
      if address == None:
        address = SOCKETIO_BASE
      self._api = SocketApi(address, project_id, self._emitter)

    elif address is 'rest':
      raise Exception('Rest api not supported')

    else:
      raise Exception('Unknown api type')

    self._project_id = project_id
    self._master_key = master_key
    self._subscriptions = {}
    self._subscription_manager = SubscriptionManager(self._api)

    self._setup_listeners()


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
    return self._api.request('loginMaster', { 'masterKey': master_key})


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


  def users(self, constraints={}, fetch=True):
    users = self._api.request('findUsers', {'constraints': constraints, 'fetch': fetch})

    for index, user in enumerate(users):
      users[index] = self.user(user)

    return users


  def add_schema(self, name):
    data = self._api.request('addDeviceSchema', {'name': name})

    if 'id' in data:
      data = self.schema(schema['id']).fetch()

    elif type(data) is str:
      raise Exception(data)

    else:
      raise Exception('Unable to create new schema')


  def schema(self, schema_id):
    return Schema(self._api, schema_id)


  def schemas(self, constraints={}, fetch=True):
    schemas = self._api.request('findDeviceSchemas', {'constraints': constraints, 'fetch': fetch})

    for index, schema in enumerate(schemas):
      schemas[index] = self.schema(schema)

    return schemas


  def add_device(self, name, schema=None, schema_id=None):
    if schema_id is not None:
      device = self._api.request('addDevice', {'name': name, 'schemaId': schema_id})
      return self.device(device['id']).fetch()

    elif schema is not None:
      device = self._api.request('addDevice', {'name': name, 'schemaId': schema.id()})
      return self.device(device['id']).fetch()

    else:
      raise Exception('No schema provided')


  def device(self, device_id):
    return Device(self._api, device_id)


  def devices(self, constraints={}, fetch=True):
    devices = self._api.request('findDevices', {'constraints': constraints, 'fetch': fetch})

    for index, device in enumerate(devices):
      devices[index] = self.device(device)

    return devices


  def subscribe(self, settings={}, callback=None):
    if callback is None:
      raise Exception('No callback function provided')

    self._subscription_manager.add_subscription(settings, callback)


  def remove_subscriptions(self):
    return self._subscription_manager.remove_subscriptions()


  def close(self):
    self.remove_subscriptions()
    self._api.close()

    self._projectId = None
    self._masterKey = None
    self._user = None


  def _setup_listeners(self):
    self._emitter.on('connect',    self._event_connect)
    self._emitter.on('update',     self._event_update)
    self._emitter.on('disconnect', self._event_disconnect)


  def _event_connect(self):
    self._subscription_manager.request_subscriptions()


  def _event_update(self, message):
    device = self.device(message['device'])
    self._subscription_manager.run(message['id'], message['changes'], device)


  def _event_disconnect(self):
    self._subscription_manager.invalidate_subscriptions()