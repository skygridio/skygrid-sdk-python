from .util import *

from datetime import datetime

from .exception import SkygridException, AuthenticationError
from .schema import Schema


class Device(object):
    """
    Represents a device in the SkyGrid system.
    """

    def __init__(self, api, data):
        """
        TODO:
        Parameters
        ----------
        api
        data
        """

        # TODO: fix the function parameters - they really should be two optional args

        if data is None:
            raise Exception('No device data/ID supplied')

        self._api = api
        self._changes = {'properties': {}}
        self._fetched = False
        self._changed = False

        if type(data) is dict:
            # TODO: this is incorrect - this does not imply
            # TODO: changes, as this does not force push
            fix_data_dates(data)
            self._data = data

            if 'properties' in data:
                self._fetched = True

        elif type(data) is str:
            self._data = {'id': data, 'properties': {}}
        else:
            raise Exception('Invalid device data: {}'.format(type(data)))

    @property
    def id(self):
        return self._data['id']

    def is_complete(self):
        return self._fetched

    def is_dirty(self):
        return self._changed

    def schema_id(self):
        return self._data['schemaId']

    def schema(self):
        """
        Get the device's schema
        Returns
        -------
        schema : Schema
            The unfulfilled schema of the device
        """
        return Schema(self._api, self.schemaId)

    def properties(self):
        properties = {}

        for key in self._data['properties']:
            properties[key] = self._data['properties'][key]

        for key in self._changes['properties']:
            properties[key] = self._changes['properties'][key]

        return properties

    def __getitem__(self, name):
        # TODO: warning if not fetched nor changed

        if name in self._changes['properties']:
            return self._changes['properties'][name]
        if name in self._data['properties']:
            return self._data['properties'][name]

        raise SkygridException("Property does not exist")

    def __setitem__(self, name, value):
        self._changes['properties'][name] = value
        self._changed = True

    def __contains__(self, name):
        return name in self._data['properties']

    def save(self, properties=None):
        """
        Save the changes to SkyGrid

        Parameters
        ----------
        properties : dict, optional
            additional parameters to be saved
        """

        # add the properties
        if properties is not None:
            for key in properties:
                self._changes['properties'][key] = properties[key]
                self._changed = True

        if self._changed:
            changes = prepare_changes(self._changes, {'deviceId': self.id})

            # TODO what is device being used for?
            device, status_code = self._api.request('updateDevice', changes)

            # TODO: check status_code

            merge_fields(self._data, self._changes, ['name', 'log', 'properties'])
            # merge_acl(self._data, self._changes)

            # nullify the changes (perhaps we shouldn't if the status code was invalid)
            self.discard_changes()

    def fetch(self):
        """
        TODO:
        """

        data, status_code = self._api.request('fetchDevice', {'deviceId': self._data['id']})

        # TODO: check status_code

        # TODO:Data might be the incorrect format - I dunno
        # TODO: what about if fetch was performed after changes have been made?

        if status_code == 400:
            raise SkygridException("Invalid device id/data to fetch, err: ", data)
        elif status_code == 401:
            raise AuthenticationError("Insufficient credentials supplied", data)

        if 'id' in data:
            fix_data_dates(data)
            self._data = data
            self._fetched = True

            return self
        else:
            raise Exception(data, status_code)

    def fetch_if_needed(self):
        """
        Fetch the device state if it has never been fetched
        """
        if not self._fetched:
            self.fetch()

    def history(self, start=None, end=None, limit=None):
        """
        Fetch the history of the current device
        Parameters
        ----------
        start : datetime
            The date from which the history should begin
        end : datetime
            The date from which the history should end
        limit : int
            The maximum number of datapoints to return

        Returns
        -------
        history : list
            List of all history points received
        """
        data = {'deviceId': self.id}
        constraints = {}

        if start is not None:
            if type(start) is datetime:
                constraints['time'] = {'$gte': date_to_string(start)}
            else:
                # TODO: better exception
                raise Exception('Invalid start date')

        if end is not None:
            if type(end) is datetime:
                if 'time' not in constraints:
                    constraints['time'] = {'$lt': date_to_string(end)}
                else:
                    constraints['time']['$lt'] = date_to_string(end)
            else:
                # TODO: better exception
                raise Exception('Invalid end date')

        data['constraints'] = constraints

        if type(limit) is int:
            data['limit'] = limit
        else:
            # TODO: better exception
            raise Exception('Invalid limit type')

        history = []

        points, status_code = self._api.request('fetchHistory', data)

        # TODO: check status_code & points

        for point in points:
            history.append(point)

        return history

    def delete(self):
        """
        Deletes the current device off skygrid

        Raises
        ______
        skygrid.AuthenticationError
            If the user currently logged in user does not have the privileges to delete the object
        skygrid.SkygridException
            If the device could not be removed (perhaps, invalid device id, device doesn't exist, etc)

        """
        res, status_code = self._api.request('deleteDevice', {'deviceId': self.id})
        if status_code == 401:
            raise AuthenticationError("Could not delete user, not authorised", res)
        elif status_code == 400:
            raise SkygridException("Invalid removal:", res)

    def discard_changes(self):
        """
        Discard the currently queued changes
        """
        self._changes = {'properties': {}}
        self._changed = False
