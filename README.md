# SkyGrid
An API for the physical world.


## Important Note!

This package is a direct port of the SkyGrid Javascript SDK. At the moment, it is missing some key functionality, and many of the implemented features are not yet Pythonic. It is not yet recommended to use this SDK in production!

Additionally, this SDK is only Python 3+ friendly.


## Installation

PIP:
```
pip install skygrid
```

## Usage

### Interacting with devices

The Device object allows us to fetch the current state of the device from the SkyGrid backend, to update the state of the device, and subscribe to changes to that device.

```python
import skygrid

# Get a Project object that lets us interact with a SkyGrid project.
project = skygrid.project('PROJECT_ID')

# Gets a Device object that lets us interact with a device.
device = project.device('DEVICE_ID')
```

### Fetching data

First we'll cover the fetching of device data.  This is simply done with the fetch() method.
```python
device.fetch()
```
There is also the fetch_if_needed() method, which fetches data from the server if it has not yet been fetched.  Please note, however, this does not mean a device state will be fetched if it has previously been fetched and changed on the backend since this time.

### Setting data

Device properties can be set with the set() method, and retrieved with the get() method.  Any change made to a device instance is not pushed to the backend until the save() method is called.  

```python
device.set('speed', 100)
device.set('distance', 10)
device.save()
```
You can also directly set properties in the save method:
```python
device.save({
  speed: 100,
  distance: 10
})
```

Note that internally, all device changes are stored as a changeset until they are pushed to the server.  When accessing the Device instance locally, the changes will be returned when querying properties.  Changes can also be discarded any time before save() is called.
```python
device = project.device('DEVICE_ID')
device.get('speed') # 100
device.set('speed', 10)
device.get('speed') # 10
device.discard_changes()
device.get('speed') # 100
```
