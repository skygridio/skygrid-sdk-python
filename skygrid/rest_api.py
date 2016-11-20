import requests
from .api import Api
import json
from .exception import *

DEBUG = True


class RestApi(Api):
    """
    Concrete API class that utilises the SkyGrid REST API interface.
    """

    def __init__(self, address, project_id):
        """
        RestAPI Constructor

        Parameters
        __________
        address : str
            The REST API URL
        project_id : str
            The unique identifier for the project to be interacted with.
        """
        self._endpoints = None
        self._address = address
        self._project_id = project_id
        self._master_key = None
        self._token = None

    def _fetch_json(self, path, data):
        """
        Simply performs a HTTP request following orders of data, to path specified

        Parameters
        __________
        path : str
            Which dir to fetch from
        data : json dict
            Parameters for the request, including HTTP verb

        Returns
        _______
        dict
            JSON object representing the response
        """

        if "method" not in data:
            raise ValueError("Request method not specified")

        ret_val = None

        # set up HTTP headers
        headers = data['headers'] if 'headers' in data else {}
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        if self._token:
            headers['X-Access-Token'] = self._token
        else:
            if self._master_key:
                headers['X-Master-Key'] = self._master_key
            headers['X-Project-ID'] = self._project_id

        payload = ""
        if "body" in data:
            payload = json.dumps(data["body"])

        method = data.pop("method")
        url = self._address + path

        # perform the correct request as per the method
        if "get" == method:
            # pass payload as URL params for get request
            ret_val = requests.get(url, headers=headers, params=payload)
        elif "post" == method:
            # pass payload as body data for other methods
            ret_val = requests.post(url, headers=headers, data=payload)
        elif "delete" == method:
            ret_val = requests.delete(url, headers=headers, data=payload)
        elif "put" == method:
            ret_val = requests.put(url, headers=headers, data=payload)
        else:
            raise ValueError("invalid method passed to fetchJson")

        if ret_val.status_code == 401:
            raise AuthenticationError("Invalid credentials")

        if len(ret_val.text) == 0:
            return {}
        return ret_val.json()

    @staticmethod
    def generate_query_url(url, queries=None):
        """
        Return a URL encoding of the supplied
        """
        if queries is not None:
            url += "?where=" + requests.utils.quote(json.dumps(queries))
        return url

    @property
    def endpoints(self):
        """
        Returns the endpoints applicable to this API

        Returns
        _______
        dict
            Key/value dict of endpoint names, and their associated lambda functions
        """
        # if the dictionary has not been registered, register it
        if self._endpoints is None:
            self._endpoints = {
                "signup": lambda data: self._fetch_json("/users", {"method": "post", "body": data}),

                "login": lambda data: self._update_token(self._fetch_json("/login", {"method": "post", "body": data})),
                # TODO: implement - also, don't hurt me for temporary exec
                "loginMaster": lambda data: exec('raise NotImplementedError("loginMaster unimplemented")'),

                "logout": lambda data=None: self._fetch_json("/logout", {"method": "post"}),

                "fetchUser": lambda data: self._fetch_json("/users/{}".format(data["userId"]), {"method": "get"}),

                "findUsers": lambda data: self._fetch_json(RestApi.generate_query_url("/users", data["constraints"]),
                                                           {"method": "get"}),

                "deleteUser": lambda data: self._fetch_json("/users/{}".format(data["userId"]), {"method": "delete"}),

                "findDeviceSchemas": lambda data: self._fetch_json(
                    RestApi.generate_query_url("/schemas", data["constraints"]), {"method": "get"}),

                "addDeviceSchema": lambda data: self._fetch_json("/schemas", {"method": "post", "body": data}),

                "fetchDeviceSchema": lambda data: self._fetch_json("/schemas/{}".format(data["schemaId"]),
                                                                   {"method": "get"}),

                "updateDeviceSchema": lambda data: self._fetch_json("/schemas/{}".format(data.pop("schemaId")),
                                                                    {"method": "put", "body": data}),

                "deleteDeviceSchema": lambda data: self._fetch_json("/schemas/{}".format(data["schemaId"]),
                                                                    {"method": "delete"}),

                "findDevices": lambda data: self._fetch_json(
                    RestApi.generate_query_url("/devices", data["constraints"]),
                    {"method": "get"}),

                "addDevice": lambda data: self._fetch_json("/devices", {"method": "post", "body": data}),

                "fetchDevice": lambda data: self._fetch_json("/devices/{}".format(data["deviceId"]), {"method": "get"}),

                "updateDevice": lambda data: self._fetch_json("/devices/{}".format(data.pop("deviceId")),
                                                              {"method": "put", "body": data}),

                "deleteDevice": lambda data: self._fetch_json("/devices/{}".format(data["deviceId"]),
                                                              {"method": "delete"}),

                "fetchHistory": lambda data: self._fetch_json("/history/{}".format(data["deviceId"]),
                                                              {"method": 'get'}),

                "getServerTime": lambda data=None: self._fetch_json("/time", {"method": "get"})
            }

        return self._endpoints

    def _update_token(self, data):
        """
        Simply updates self.token to the data.token
        """
        if 'status' in data and data['status'] == 'error':
            raise AuthenticationError(data['data'])
        elif 'results' in data:
            raise ProjectError(data)
        elif 'token' not in data:
            raise ValueError("Token missing from data response", data)

        self._token = data["token"]
        return data

    def request(self, name, data=None):
        """
        Request an endpoint procedure to be called.

        Parameters
        __________
        name : str
            The name of the endpoint we wish to call
        data : dict, optional
            The associated data for the request, defaults to None

        Returns
        _______
        The JSON object returned by the server for this request
        """
        # attempt to execute the requested endpoint
        reqFunc = self.endpoints[name]
        return reqFunc(data)

    def close(self):
        """
        Unused for REST API
        """
        # Future HTTP cleanup requests would be placed here
        pass
