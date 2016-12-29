#!/usr/bin/python3
import skygrid
def fn(changes,device):
  for i in changes:
    print(i,device.get(i))
  print("~~end of {} entry~~".format(device.name()))

pr = skygrid.Project('RHlD5jC0',address="http://localhost:3081",api='socketio')
print(pr.fetchServerTime())
pr = skygrid.Project('RHlD5jC0',address="http://localhost:3080",api='rest')
print(pr.fetchServerTime())