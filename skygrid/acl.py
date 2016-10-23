from .user import User
from .util import *

PUBLIC_KEY = '*'


def validate_access_type(access_type):
  if accessType is 'create' or accessType is 'read' or \
  accessType is 'udpate' or accessType is 'delete':
     return

  raise Exception('Access type \'{}\' invalid, must be' \
   + ' one of the following: create, read, update, delete'.format(access_type))


class Acl(object):
  def __init__(self, data):
    if data:
      if type(data) is 'Acl':
        self._permissions_by_id = deep_clone(data._permissions_by_id)
      
      else:
        self._permissions_by_id = deep_clone(data)

    else:
      self._permissions_by_id = {}


  def permissions(self):
    return self._permissions_by_id


  def is_empty(self):
    return objectEmpty(self._permissions_by_id)


  def set_access(self, user_id, access_type, allowed):
    if type(access_type) is str:
      self._set_access(user_id, access_type, allowed)

    elif type(access_type) is list:
      for item in access_type:
        self._set_access(user_id, item, allowed)


  def set_public_access(self, access_type, allowed):
    self.setAccess(PUBLIC_KEY, access_type, allowed)


  def get_access(self, user_id, access_type):
    return self._getAccess(user_id, access_type)
  

  def get_public_access(self, access_type):
    return self._getAccess(PUBLIC_KEY, access_type)


  def removeAccess(self, user_id, access_type):
    if type(access_type) is str:
      self._remove_access(user_id, access_type)

    elif type(access_type) is list:
      for item in access_type:
        self._remove_access(user_id, item)


  def remove_public_access(self, access_type):
    self.remove_access(PUBLIC_KEY, access_type)


  # def toJSON(self):
  #   return deepClone(self._permissionsById);
  # }

  def _set_access(user_id, access_type, allowed=None):
    validate_access_type(access_type)

    if type(user_id) is User:
      user_id = user_id['id']

    if type(user_id) is not str:
      raise Exception('userId must be a string.')


    if allowed is None:
      pass
    
    elif type(allowed) is not bool:
      raise Exception('allowed must be either true or false.')


    permissions = self._permissions_by_id[userId]

    if permissions is None:
      if allowed is None:
        return
      else:
        permissions = {}
        self._permissions_by_id[userId] = permissions


    if allowed is not None:
      permissions[access_type] = allowed
      self._permissions_by_id[user_id] = permissions

    else:
      permissions.pop(access_type, None)

      if object_empty(permissions):
        self._permissions_by_id[user_id]


  def _get_access(self, user_id, access_type):
    validate_access_type(access_type)

    if type(user_id) is User:
      user_id = user_id.id

    permissions = self._permissions_by_id[user_id]
    if permissions is None:
      return

    return permissions[access_type]


  def _remove_access(user_id, access_type=None):
    acl = self._permissions_by_id[user_id]

    if acl is not None:
      if access_type is not None:
        validate_access_type(access_type)
        acl.pop(access_type, None)
        self._permissions_by_id[user_id] = acl

      if access_type is None and object_empty(acl):
        self._permissions_by_id.pop(user_id, None)