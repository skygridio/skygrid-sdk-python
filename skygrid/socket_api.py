from socketIO_client import SocketIO, BaseNamespace
from time import sleep
import threading

class SocketApi(object):
  class Namespace(BaseNamespace):
    def set_api(self, api):
      self._api = api


    def on_connect(self):
      self._api._session = False
      self._api.connected = True
      self._api._emitter.emit('connect')


    def on_disconnect(self):
      self._api._session = False
      self._api.connected = False
      self._api._emitter.emit('disconnect')


  def on_update(self, *args):
    self._emitter.emit('update', args[0])


  def setup_namespace(self, io, path):
    namespace = self.Namespace(io, path)
    namespace.set_api(self)
    return namespace


  def __init__(self, address=None, project_id=None, emitter=None):
    self._address       = address
    self._project_id    = project_id
    self._master_key    = None
    self._session       = False
    self.connected      = False
    self._socket        = None
    self._socket_thread = None
    self._request       = None

    self._emitter       = emitter

    if self._socket == None:
      self._socket = SocketIO(self._address, Namespace=self.setup_namespace)

      self._socket.on('update', self.on_update)

      self._socket_thread = threading.Thread(target=self._manage_socket)
      self._socket_thread.daemon = True
      self._socket_thread.start()


  def _manage_socket(self):
    # this is a bit average, but the scoketIO_client library
    # requires blocking (for wait()) to receive updates for subscriptions
    while True:
      if not self._request:
        self._socket.wait(seconds=0.2)

      else:
        self._socket.emit('message', self._request, self.return_result)
        self._socket.wait_for_callbacks()

        self._request = None


  def close(self):
    self._socket_thread = None
    self._socket = None


  def request(self, name, data=None):
    if self._session:
      return self.make_request(name, data)

    self.make_request('createSession', {'projectId': self._project_id})
    self._session = True

    if not self._master_key == None:
      self.make_request('loginMaster', {'masterKey': self._master_key});
    
    return self.make_request(name, data);

  
  def make_request(self, name, data=None):
    request = {'type': name}

    if not data == None:
      request['data'] = data
    else:
      request['data'] = {}

    self._request_result = None
    self._request = request

    # TODO allow for timeout
    while self._request_result is None:
      sleep(0.2)

    result = self._request_result
    self._request_result = None

    return result


  def return_result(self, *args):
    result = args[0]

    if 'status' in result and result['status'] == 'ok':
      if 'data' in result:
        self._request_result = result['data']
      else:
        self._request_result = True

    elif 'status' in result and result['status'] != 'ok':
      raise Exception(result['data'])

    else:
      raise Exception('Unexpected response from server')