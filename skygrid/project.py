from skygrid import API_BASE, DEFAULT_API

from .socket_api import SocketApi
from .rest_api import RestApi
from .device import Device
from .schema import Schema
from .subscription_manager import SubscriptionManager
from .user import User

from pyee import EventEmitter


class Project(object):
    """
      Instance object to allow interaction with a specific project in the Skygrid API

      Attributes
      __________
      _emitter : EventEmitter
        TODO: but its something to do with node events atm
    """
    _emitter = EventEmitter()

    def __init__(self, project_id, address=None, api=None, master_key=None):
        """
          Project Constructor

          Parameters
          __________
          project_id : str
            Unique identifier for the project, as named on dashboard.skygrid.io

          address : str, optional
            Custom URL to connect to as skygrid API server

          api : {None, 'rest', 'websocket'}
            Which type of API interface to use.
            If None is supplied, defaults to __init__.py->DEFAULT_API.

          master_key : str, optional
            Associated master key for the specified project, defaults to None.

          Raises
          ______
          NotImplementedError
            If the supplied API string is invalid, or simply hasn't been implemented yet.
        """

        if api == None:
            api = DEFAULT_API

        if address == None:
            address = API_BASE

        if api is 'websocket':
            self._api = SocketApi(address, project_id, self._emitter)
            # placing this here to discourage use of deprecation
            raise DeprecationWarning('Socketio websocket API likely to be deprecated in python, replaced with pure ws')

        elif api is 'rest':
            self._api = RestApi(address, project_id)
            raise FutureWarning('REST API not finished')

        else:
            raise NotImplementedError('Unknown API type')

        self._project_id = project_id
        self._master_key = master_key
        self._subscriptions = {}
        self._subscription_manager = SubscriptionManager(self._api)

        self._setup_listeners()

    @property
    def id(self):
        return self._project_id

    def login(self, email, password):
        """
          Log into the user that is a client of the project.
          Note: this is _not_ the credentials used to log into the dashboard
          Instead, this is a user of a project, created via the dashboard/signup API command

          Parameters
          __________
          email : str
            The email of the user to log in
          password : str
            The associated password
        """
        data = self._api.request('login', {'email': email, 'password': password})

        if 'token' in data:
            self._user = {'email': email,
                          'id': data['userId'],
                          'token': data['token']}

        elif type(data) is str:
            raise Exception(data)

        else:
            raise Exception('Unable to log in')

    def login_master(self, master_key):
        """
          TODO:
        """
        return self._api.request('loginMaster', {'masterKey': master_key})

    def logout(self):
        """
          Logs the current user out. Must be logged in first.
        """

        self._api.request('logout')
        self._user = None

    def signup(self, email, password, meta=None):
        """
          Creates a user as a client of the project.

          Parameters
          __________
          email : str
            The username for the user
          password : str
            Associated password for the newly created client
        """

        data = self._api.request('signup', {'email': email, 'password': password, 'meta': meta})

        if 'id' in data:
            return self.user(data['id']).fetch()

        elif type(data) is str:
            raise Exception(data)

        else:
            raise Exception('Unable to create new user')

    def user(self, user_id):
        """
          Fetch the user object from its unique identifier.

          Parameters
          __________
          user_id : str
            A user's unique identifier
        """
        return User(self._api, user_id)

    def users(self, constraints={}, fetch=True):
        """
          TODO:
        """
        users = self._api.request('findUsers', {'constraints': constraints, 'fetch': fetch})

        for index, user in enumerate(users):
            users[index] = self.user(user)

        return users

    def add_schema(self, name):
        """
          TODO:
        """
        data = self._api.request('addDeviceSchema', {'name': name})

        if 'id' in data:
            data = self.schema(schema['id']).fetch()

        elif type(data) is str:
            raise Exception(data)

        else:
            raise Exception('Unable to create new schema')

    def schema(self, schema_id):
        """
          TODO:
        """
        return Schema(self._api, schema_id)

    def schemas(self, constraints={}, fetch=True):
        """
          TODO:
        """

        schemas = self._api.request('findDeviceSchemas', {'constraints': constraints, 'fetch': fetch})

        for index, schema in enumerate(schemas):
            schemas[index] = self.schema(schema)

        return schemas

    def add_device(self, name, schema=None, schema_id=None):
        """
          TODO:
        """
        if schema_id is not None:
            device = self._api.request('addDevice', {'name': name, 'schemaId': schema_id})
            return self.device(device['id']).fetch()

        elif schema is not None:
            device = self._api.request('addDevice', {'name': name, 'schemaId': schema.id()})
            return self.device(device['id']).fetch()

        else:
            raise Exception('No schema provided')

    def device(self, device_id):
        """
          TODO:
        """
        return Device(self._api, device_id)

    def devices(self, constraints={}, fetch=True):
        """
          TODO:
        """
        devices = self._api.request('findDevices', {'constraints': constraints, 'fetch': fetch})

        for index, device in enumerate(devices):
            devices[index] = self.device(device)

        return devices

    def subscribe(self, settings={}, callback=None):
        """
          TODO:
        """
        if callback is None:
            raise Exception('No callback function provided')

        self._subscription_manager.add_subscription(settings, callback)

    def remove_subscriptions(self):
        """
          TODO:
        """
        return self._subscription_manager.remove_subscriptions()

    def close(self):
        """
          Close the current project, removing all active subscriptions,
          and API connections.
        """
        self.remove_subscriptions()
        self._api.close()

        self._projectId = None
        self._masterKey = None
        self._user = None

    def _setup_listeners(self):
        """
          TO-DO:
        """
        self._emitter.on('connect', self._event_connect)
        self._emitter.on('update', self._event_update)
        self._emitter.on('disconnect', self._event_disconnect)

    def _event_connect(self):
        """
          TODO:
        """
        self._subscription_manager.request_subscriptions()

    def _event_update(self, message):
        """
          TODO:
        """
        device = self.device(message['device'])
        self._subscription_manager.run(message['id'], message['changes'], device)

    def _event_disconnect(self):
        """
          TODO:
        """
        self._subscription_manager.invalidate_subscriptions()
