from socketIO_client import SocketIO, BaseNamespace


class SocketApi(object):
  class Namespace(BaseNamespace):
    def set_api(self, api):
      self._api = api

    def on_connect(self):
      #print('[Connected]')
      self._api._session = False
      self._api.connected = True
      #self._emitter.emit('connect')


    def on_update(self, *args):
      #self._emitter.emit('update', args)
      pass


    def on_disconnect(self):
      #print('[Disconnected]')
      self._api._session = False
      self._api.connected = False
      #self._emitter.emit('disconnect')


  def __init__(self, address, emitter):
    self._address = address
    #self._emitter = emitter
    self._session = False
    self.connected = False
    self._socket = None


  def setup_namespace(self, io, path):
    #print('new_wsapi:', msg)
    namespace = self.Namespace(io, path)
    namespace.set_api(self)
    return namespace


  def setup(self, project_id, master_key=None):
    self._project_id = project_id;
    self._master_key = master_key;
    
    if self._socket == None:
      self._socket = SocketIO(self._address, Namespace=self.setup_namespace)


  def close(self):
    self._socket.close()
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
    
    self._request_result = None

    self._socket.emit('message', request, self.return_result)
    self._socket.wait(seconds=2)

    return self._request_result


  def return_result(self, *args):
    result = args[0]

    if result['status'] == 'ok':
      if 'data' in result:
        self._request_result = result['data']

    else:
      #TODO throw error
      self._request_result = result['data']
      
#    return new Promise((resolve, reject) => {
#      self.socket.emit('message', request, response => {
#        if (response.status === 'ok') {
#          resolve(response.data);
#        } else if (typeof response.data === 'string') {
#          throw new SkyGridException(response.data);
#        } else {
#          throw new ValidationException(response.data);
#        }
#      });
#    });