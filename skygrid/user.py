class User(object):

  def __init__(self, api, data):
    self._api = api
    
    self._changes = {}
    self._fetched = False
    self._changed = False

    if type(data) is dict:
      self._data = data

      if 'meta' in data:
        self._fetched = True
    
    elif  type(data) is str:
      self._data = { 'id': data }


  def id(self):
    return self._data['id']
  

  def email(self):
    if 'email' in self._changes:
      return self._changes['email']
    
    return self._data['email']


  def set_email(self, value):
    self._changes['email'] = value
    self._changed = True


  def meta(self):
    if 'meta' in self._changes:
      return self._changes['meta']
    
    return self._data['meta']


  def set_meta(self, value):
    self._changes['meta'] = value
    self._changed = True


  def set_password(self, value):
    self._changes['password'] = value
    self._changed = True


  def save(self):
    if self._api.using_master_key():
      raise Exception('Can only edit users when using the master key')

    if self._changed:
      self._changes['userId'] = self.id

      user = self._api.request('updateUser', self._changes)

      if 'email' in self._changes:
        self._data['email'] = self._changes['email']
      
      if 'meta' in self._changes:
        self._data['meta'] = self._changes['meta']

      self._changes = {}
      self._changed = False

    return self
      

  def fetch(self):
    data = self._api.request('fetchUser', {'userId': self.id})

    self._data = data
    self._fetched = True

    return self


  def fetch_if_needed(self):
    if not self._fetched:
      return self.fetch()

    return self


  def remove(self):
    return self._api.request('deleteUser', {'userId': self.id})


  def discard_changes(self):
    self._changes = {}