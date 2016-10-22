#from .acl import Acl
from .util import *

class Device(object):
  
  def __init__(self, api, data=None):
    if data == None:
      raise Exception('No device data/ID supplied')

    self._api = api.api
    #self._subscriptionManager = api.subscriptionManager;

    self._changes = { 'properties': {} }
    self._fetched = False
    self._changed = False

    if type(data) is dict:
      fix_data_dates(data)
      self._data = data

      if 'properties' in data:
        self._fetched = True

    elif type(data) is str:
      self._data = { 'id': data, 'properties': {} }

    else:
      raise Exception('Invalid device data: {}'.format(type(data)))


  def id(self):
    return self._data['id']


  def name(self):
    if 'name' in self._changes:
      return self._changes['name']

    return self._data['name']


  def set_name(self, value):
    self._changes['name'] = value
    self._changed = True


  # def acl(self):
  #   if 'acl' not in self._changes:
  #     if 'acl' in self._data:
  #       self._changes.acl = Acl(self._data.acl)
  #     else:
  #       self._changes.acl = Acl()

  #     self._changed = True

  #   return self._changes.acl


  # def set_acl(self, value=None):
  #   if not value == None: # && typeof value === 'object') {
  #     if not value is Acl:
  #       value = Acl(value)

  #   self._changes.acl = value
  #   self._changed = true


  def log(self):
    if 'log' in self._changes:
      return self._changes['log']

    return self._data['log']


  def set_log(self, value):
    self._changes['log'] = value
    self._changed = True


  def is_complete(self):
    return self._fetched


  def is_dirty(self):
    return self._changed


  def schema_id(self):
    return self._data['schemaId']

  
  def schema(self):
    return Schema(self._api, self.schemaId)


  def properties(self):
    properties = {}

    for key in self._data['properties']:
      properties[key] = self._data['properties'][key]

    for key in self._changes['properties']:
      properties[key] = self._changes['properties'][key]
        
    return properties


  def set(self, name, value):
    self._changes['properties'][name] = value
    self._changed = True


  def get(self, name):
    if name in self._changes['properties']:
      return self._changes['properties'][name]
    
    if name in self._data['properties']:
      return self._data['properties'][name]
    
    raise Exception('Property does not exist')
  

  def property_exists(self, name):
    return name in self._data['properties']
  

  def save(self, properties=None):
    if not properties == None:
      for key in properties:
        self._changes['properties'][key] = properties[key]
        self._changed = True

    if self._changed:
      changes = prepare_changes(self._changes, {'deviceId': self.id()})

      device = self._api.request('updateDevice', changes)

      merge_fields(self._data, self._changes, ['name', 'log', 'properties'])
      #util.merge_acl(self._data, self._changes)

      self._changes = { 'properties': {} }
      self._changed = False
      
    return self


  def fetch(self):
    data = self._api.request('fetchDevice', {'deviceId': self._data['id']})

    if 'id' in data:
      fix_data_dates(data)
      self._data = data
      self._fetched = True

      return self

    else:
      raise Exception(data)


  def fetch_if_needed(self):
    if not self._fetched:
      return self.fetch()

    return self


  def history(self, start=None, end=None, limit=None):
    data = { 'deviceId': self.id }
    constraints = {}

    if not start == None:
      if start is str:
        #TODO start = new Date(start)
        pass

      #if start is Date:
      #  constraints.time = { '$gte': start }
      
      #else if start == 'object') {
      #  constraints = start;
      #}
    

    if not end == None:
      pass
      # if end is str:
      #   #end = new Date(end);
      
      # if (end instanceof Date) {
      #   if (!constraints.time) {
      #     constraints.time = {};
      #   }

      #   constraints.time.$lt = end;
      # }

    data['constraints'] = constraints

    if limit is int:
      data['limit'] = limit

    history = []

    points = self._api.request('fetchHistory', data)

    for point in points:
      #point['time'] = new Date('time')
      history.append(point)

    return history


  def remove(self):
    return self._api.request('deleteDevice', { 'deviceId': self._data['id'] })


  # def subscribe(callback):
  #   self._subscriptionManager.addSubscription({'deviceId': self.id}, 
  #   (device, changes) => {
  #     self._data = device._data;
  #     self._fetched = true;

  #     if (callback) {
  #       callback(self, changes);
  #     }
  #   });
  # }


  def discard_changes(self):
    self._changes = { 'properties': {} }
    self._changed = False