#from rest_api import RestApi
from .socket_api import SocketApi


class Api(object):

  def __init__(self):
    self._emitter = None
    self.api = None


  def using_master_key(self):
    return not self.master_key == None


#  def connected():
#    if self.socket and self._current == self.socket:
#      return self.socket.connected
#
#    return False


  def setup(self, address, api_type, project_id, master_key=None):
    self._apis = {
      #rest: RestApi(address),
      'websocket': SocketApi(address, self._emitter)
    }

    self._address = address
    self.project_id = project_id
    self.master_key = master_key

    self.set_api_type(api_type)


  def set_api_type(self, name):
    next = self._apis[name]

    if next:
      if self.api:
        self.api.close()

      next.setup(self.project_id, self.master_key)
      self.api = next

    else:
      print('unknown api')
      # throw error- throw new Error(`API type '${name}' unknown`)


  def add_listener(self, name, callback):
    self._emitter.add_listener(name, callback)


  def request(self, name, data=None):
    return self.api.request(name, data)