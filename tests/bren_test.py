import skygrid
from datetime import datetime

print('  ___ _         ___     _    _  ')
print(' / __| |___  _ / __|_ _(_)__| | ')
print(' \__ \ / / || | (_ | \'_| / _` | ')
print(' |___/_\_\\\\_, |\___|_| |_\__,_| ')
print('          |__/                  ')


#client = skygrid.Project('i6gzXAzL', address='localhost')
client = skygrid.Project('5DS8vHP7')



print('\nSchemas\n-------')

print('Fetch all schemas...')
schemas = client.schemas()
for schema in schemas:
  print('{} -> {} @ {}'.format(schema.id(), schema.name(), schema._data['updatedAt']))

# print('\nCreate new schema...')
# schema = client.add_schema('new schema')
# print('{} -> {}'.format(schema.id(), schema.name()))

print('\nFetch a schema...')
schema = client.schema('A9joRoDo').fetch()
print('{} -> {}\n(dirty:{}) (fetched:{})\n{}'.format(schema.id(), schema.name(), schema.is_dirty(), schema.is_complete(), schema.properties()))

print('\nFetch a property...')
property = schema.get_property('speed')
print('{}'.format(property))

print('\nUpdate property...')
schema.update_property('speed', 'number', 777)
property = schema.get_property('speed')
print('{}'.format(property))

print('\nAdd new property...')
schema.add_property('new_field', 'number', 0)
print('{} -> {}\n(dirty:{}) (fetched:{})\n{}'.format(schema.id(), schema.name(), schema.is_dirty(), schema.is_complete(), schema.properties()))

print('\nRemove property...')
schema.remove_property('speed')
print('{} -> {}\n(dirty:{}) (fetched:{})\n{}'.format(schema.id(), schema.name(), schema.is_dirty(), schema.is_complete(), schema.properties()))

# print('\nSave schema...')
# schema.save()

print('\nReset schema changes...')
schema.discard_changes()
print('{} -> {}\n(dirty:{}) (fetched:{})\n{}'.format(schema.id(), schema.name(), schema.is_dirty(), schema.is_complete(), schema.properties()))
property = schema.get_property('speed')
print('{}'.format(property))



print('\n\nDevices\n-------')


print('Fetch all devices...')
devices = client.devices()
for device in devices:
  print('{} -> {} @ {}'.format(device.id(), device.name(), device._data['updatedAt']))

print('\nCreate new device w/ schema object...')
device = client.add_device('using object', schema=schema)
print('{} -> {} (dirty:{}) (fetched:{})'.format(device.id(), device.name(), device.is_dirty(), device.is_complete()))
d_id1 = device.id()

print('\nCreate new device w/ schema id...')
device = client.add_device('using id', schema_id='A9joRoDo')
print('{} -> {} (dirty:{}) (fetched:{})'.format(device.id(), device.name(), device.is_dirty(), device.is_complete()))
d_id2 = device.id()

print('\nFetch all devices...')
devices = client.devices()
for device in devices:
  print('{} -> {} @ {}'.format(device.id(), device.name(), device._data['updatedAt']))

print('\nDelete a device...')
print('Deleting {}'.format(d_id1))
client.device(d_id1).fetch().delete()
print('Deleting {}'.format(d_id2))
client.device(d_id2).fetch().delete()

print('\nFetch all devices...')
devices = client.devices()
for device in devices:
  print('{} -> {} @ {}'.format(device.id(), device.name(), device._data['updatedAt']))

print('\nFetch a device...')
device = client.device('mPGXUKQq').fetch()
print('{} -> {} (dirty:{}) (fetched:{})\n{}'.format(device.id(), device.name(), device.is_dirty(), device.is_complete(), device.properties()))

print('\nGet device history')
start = datetime(2016, 9, 23)
end = datetime(2016, 10, 24)
print('{}'.format(device.history(start, end, limit=1)))

print('\nGet device property')
print('{}'.format(device.get('vin')))

print('{}'.format(device._data))

print('\nUpdate device property')
device.set('vin', "changes")

print('\nSave device')
device.save()

print('{}'.format(device._data))

print('\nList device properties')
print('{} -> {} (dirty:{}) (fetched:{})\n{}'.format(device.id(), device.name(), device.is_dirty(), device.is_complete(), device.properties()))



print('\n\nAuthentication\n-------')


# test logging in
print('\nLogin...')
user = client.login('test@test.com', 'password') #'brendan@skygrid.io', 'brendan')
print('{} : {} -> {}'.format(client._user['id'], client._user['email'], client._user['token']))

print('\nFetch all devices...')
devices = client.devices()
for device in devices:
  print('{} -> {} @ {}'.format(device.id(), device.name(), device._data['updatedAt']))

# print('\nLogout...')
# client.logout()

# print('\nFetch all devices...')
# devices = client.devices()
# for device in devices:
#   print('{} -> {} @ {}'.format(device.id(), device.name(), device._data['updatedAt']))


# # test signing up
# print('\nSignup\n------')

# try:
#   user = client.signup('brendan@brendan.com','brendan')
#   print('User: {}', user.email())

# except Exception as e:
#   print('Exception: {}'.format(e))


print('Done.')