#from rest_api import RestApi
from .socket_api import SocketApi


class Api(object):

  def __init__(self):
    self._emitter = None
    self.api = None


  def add_listener(self, name, callback):
    self._emitter.add_listener(name, callback)


  def request(self, name, data=None):
    return self.api.request(name, data)