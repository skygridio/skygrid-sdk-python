from requests import request

class RestApi(object):
  def __init__(self,address,project_id):
    self._address = address;
    self._project_id = project_id
    self._token = None;
    self._master_key = None

    self._endPoints = {
      'getServerTime': get_server_time
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
    r = request(
      params.get('method','GET').upper(),
      fullUrl,
      headers=params.get('headers',{}),
      data=params.get('body',{}))
    r.raise_for_status()
    return parseJSON(r)

  def close(self):
    pass

  def request(self,name,data=None):
    if(name not in self._endPoints):
      raise Exception('API end point {} does not exist on the REST API'.format(name))

    return self._endPoints[name](self,data)

def get_server_time(self,data):
  return self._fetchJson('/time', {'method':'get'})

def parseJSON(r):
  if(r.status_code != 204):
    return r.json()
  return {}
