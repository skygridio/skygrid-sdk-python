#!/usr/bin/python3
import skygrid, requests, json
def fn(changes,device):
  for i in changes:
    print(i,device.get(i))
  print("~~end of {} entry~~".format(device.name()))

# pr = skygrid.Project('RHlD5jC0',address="http://localhost:3081",api='socketio')
# print(pr.signup('jonas@mailinator.com','1234'))
pr = skygrid.Project('RHlD5jC0',address="http://localhost:3080",api='rest') 
try:
  pr.login_master('tMX1b94v+Qmr8/r5RH66Bkjk')
  print(pr.users())  
except requests.exceptions.HTTPError as err:
  print(err)
  print(err.request)
  print(err.request.body)
  print(err.request.headers)
