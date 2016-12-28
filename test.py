#!/usr/bin/python3
import skygrid
def fn(changes,device):
  for i in changes:
    print(i,device.get(i))
  print("~~end of {} entry~~".format(device.name()))

pr = skygrid.Project('RHlD5jC0',address="http://localhost:3081")
pr.login_master('tMX1b94v+Qmr8/r5RH66Bkjk')
print(pr.users())