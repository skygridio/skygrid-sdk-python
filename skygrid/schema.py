# from .acl import Acl
from .util import *


class Schema(object):
    def __init__(self, api, data=None):
        if data is None:
            raise Exception('No device data/ID supplied')

        self._api = api
        self._data = data

        self._changes = {'properties': {}}
        self._fetched = False
        self._changed = False

        if type(data) is dict:
            self._data = data

            if 'properties' in data:
                self._fetched = True

        elif type(data) is str:
            self._data = {'id': data, 'properties': {}}

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        if 'name' in self._changes:
            return self._changes['name']

        return self._data['name']

    def set_name(self, value):
        self._changes['name'] = value
        self._changed = True

    @property
    def description(self):
        if 'description' in self._changes:
            return self._changes['description']

        return self._data['description']

    def set_description(self, value):
        self._changes['description'] = value
        self._changed = True

    # def acl(self):
    #   if (!self._changes.acl) {
    #     if (self._data.acl) {
    #       self._changes.acl = new Acl(self._data.acl);
    #     } else {
    #       self._changes.acl = new Acl();
    #     }

    #     self._changed = true;
    #   }

    #   return self._changes.acl;
    # }

    # /**
    #  * Sets the Access-Control-List (ACL) associated with self schema.
    #  * @param {object|Acl} value The ACL object.
    #  */
    # set acl(value) {
    #   if (value && typeof value === 'object') {
    #     if (!(value instanceof Acl)) {
    #       value = new Acl(value);
    #     }
    #   }

    #   self._changes.acl = value;
    #   self._changed = true;
    # }

    def is_complete(self):
        return self._fetched

    def is_dirty(self):
        return self._changed

    def properties(self):
        properties = []

        for key in self._data['properties']:
            if key not in properties:
                properties.append(key)

        for key in self._changes['properties']:
            # if the property has been marked for removal
            if self._changes['properties'][key] is None:
                properties.remove(key)

            elif key not in properties:
                properties.append(key)

        return properties

    def add_property(self, name, ttype, default):
        self._changes['properties'][name] = {
            'type': ttype,
            'default': default
        }

        self._changed = True

    def update_property(self, name, ttype, default):
        if name in self._data['properties'] or name in self._changes['properties']:
            self._changes['properties'][name] = {
                'type': ttype,
                'default': default
            }

            self._changed = True

        else:
            raise Exception('Property does not exist')

    def get_property(self, name):
        if name in self._changes['properties']:
            return self._changes['properties'][name]

        if name in self._data['properties']:
            return self._data['properties'][name]

        raise Exception('Property does not exist')

    def remove_property(self, name):
        self._changes['properties'][name] = None
        self._changed = True

    def save(self):
        if self._api.using_master_key():
            raise Exception('Can only edit users when using the master key')

        if self._changed:
            changes = prepare_changes(self._changes, {'schemaId': self.id()})

            schema = self._api.request('updateDeviceSchema', changes)

            if type(schema) is str:
                raise Exception(schema)

            merge_fields(self._data, self._changes, ['name', 'description', 'properties'])
            # merge_acl(self._data, self._changes)

            self._changes = {'properties': {}}
            self._changed = False

        return self

    def fetch(self):
        data = self._api.request('fetchDeviceSchema', {'schemaId': self.id()})

        self._data = data
        self._fetched = True

        return self

    def fetch_if_needed(self):
        if not self._fetched:
            return self.fetch()

        return self

    def remove(self):
        return self._api.request('deleteDeviceSchema', {'schemaId': self.id})

    def discard_changes(self):
        self._changes = {'properties': {}}
        self._changed = False
