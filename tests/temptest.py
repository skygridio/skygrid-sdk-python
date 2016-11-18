
#from skygrid.rest_api import RestApi
import sys
sys.path.insert(0, '../skygrid')

from rest_api import RestApi

r = RestApi("https://api.skygrid.io", "jeQEcCtj")
#print(r.endpoints["getServerTime"]())

#print(r.request("getServerTime"))
print(r.request("findDevices", {"constraints": None}))
print(r.request("fetchHistory", {"deviceId": "wJERCYld"}))
print(r.request("findUsers", {"constraints": None}))


print(r.request("login", {"email":"patrick@skygrid.io", "password": "cookie"}))




