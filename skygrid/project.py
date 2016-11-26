from skygrid import API_BASE, DEFAULT_API

from .socket_api import SocketApi
from .rest_api import RestApi
from .device import Device
from .schema import Schema
from .subscription_manager import SubscriptionManager
from .user import User
from .util import ISO8601_format
from .exception import AuthenticationError, SkygridException

from datetime import datetime
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
            If None is supplied, defaults to DEFAULT_API as specified in __init__.py.

          master_key : str, optional
            Associated master key for the specified project, defaults to None.

          Raises
          ______
          NotImplementedError
            If the supplied API string is invalid, or simply hasn't been implemented yet.
        """

        self._user = None

        if api is None:
            api = DEFAULT_API

        if address is None:
            address = API_BASE

        if api == 'websocket':
            self._api = SocketApi(address, project_id, self._emitter)
            # placing this here to discourage use of deprecation
            raise DeprecationWarning('Socketio websocket API likely to be deprecated in python, replaced with pure ws')

        elif api == 'rest':
            self._api = RestApi(address, project_id)
            # raise FutureWarning('REST API not finished')

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
            raise SkygridException(data)

        else:
            raise AuthenticationError('Unable to log in')

    def login_master(self, master_key):
        """
        Log into the project using a masterkey.
        This is useful when accessing private API methods, such as signup, add_schema, and delete_device.

        Parameters
        __________
        master_key : str
            The unique master key for a given project

        Returns
        _______
        JSON response after logging in
        TODO: this may be changed.
        """
        self._master_key = master_key
        return self._api.request('loginMaster', {'masterKey': master_key})

    def logout(self):
        """
        Logs the current user out, no action if no user currently logged in.
        """
        self._api.request('logout')
        self._api._token = None
        self._user = None

    def logout_master(self):
        """
        Removes the stored master key
        """
        self._api._master_key = None
        self._master_key = None

    def signup(self, email, password, meta=None):
        """
        Creates a user as a client of the project.
        Required to be logged in using a masterkey.

        Parameters
        __________
        email : str
            The username for the new user
        password : str
            Associated password for the newly created client

        TODO: meta

        Returns
        _______
        user : User()
            Instance of the newly created user

        """
        arg = {'email': email, 'password': password}
        if meta:
            arg['meta'] = meta
        data, status_code = self._api.request('signup', arg)

        # TODO: delete the 403 code, it's currently a bug in the node server
        if status_code == 401 or status_code == 403:
            raise AuthenticationError('Unable to create new user:', data['data'])
        elif status_code == 400:
            raise SkygridException("Bad request:", data['data'])

        if 'id' in data:
            return self.user(data['id']).fetch()
        elif type(data) is str:
            raise Exception(data)


    def user(self, user_id):
        """
        Fetch the user object from its unique identifier.

        Parameters
        __________
        user_id : str
            A user's unique identifier
        """
        return User(self._api, user_id).fetch()

    def users(self, constraints={}, fetch=True):
        """
        TODO:
        """
        users, status_code = self._api.request('findUsers', {'constraints': constraints, 'fetch': fetch})

        if status_code == 401:
            raise AuthenticationError("Cannot fetch users, unauthorised:", users)
        elif status_code == 400:
            raise SkygridException("Error:", users)

        for index, user in enumerate(users):
            users[index] = self.user(user)

        return users

    def add_schema(self, name):
        """
          TODO:
        """
        data = self._api.request('addDeviceSchema', {'name': name})
        #TODO: fix
        if 'id' in data:
            data = self.schema(self.schema['id']).fetch()

        elif type(data) is str:
            raise Exception(data)

        else:
            raise Exception('Unable to create new schema')

    def schema(self, schema_id):
        """
          TODO:
        """
        return Schema(self._api, schema_id).fetch()

    def schemas(self, constraints={}, fetch=True):
        """
        Grab the current updated list of all schemas for the current project.

        Attributes
        __________
        constraints : dict
            TODO: explain usage
        fetch : bool
            Determines whether the full schema object should be fetched, or just the description.  Defaults to true.

        Returns
        _______
        A list of all Schema objects for this project
        """
        schemas = self._api.request('findDeviceSchemas', {'constraints': constraints, 'fetch': fetch})
        # we must construct a list of schema objects, which are injected with the schema data we already fetched
        return [Schema(self._api, sc) for sc in schemas]

    def add_device(self, name, schema=None, schema_id=None):
        """
          TODO:
        """
        if schema_id is not None:
            device, status_code = self._api.request('addDevice', {'name': name, 'schemaId': schema_id})
            return self.device(device['id']).fetch()

        elif schema is not None:
            device, status_code = self._api.request('addDevice', {'name': name, 'schemaId': schema.id})
            return self.device(device['id']).fetch()

        else:
            raise SkygridException('No schema provided')

    def device(self, device_id):
        """
          TODO:
        """
        return Device(self._api, device_id).fetch()

    def devices(self, constraints={}, fetch=True):
        """
          TODO:
        """
        devices = self._api.request('findDevices', {'constraints': constraints, 'fetch': fetch})
        return [Device(self._api, dv) for dv in devices]
        # for index, device in enumerate(devices):
        #     devices[index] = self.device(device)
        #
        # return devices

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

        self._project_id = None
        self._master_key = None
        self._user = None

    def get_time(self):
        """
        Get the server's current time (UTC)

        Returns
        -------
        time : datetime
            datetime object representing the current time

        """
        return datetime.strptime(self._api.request('getServerTime')[0], ISO8601_format)

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
