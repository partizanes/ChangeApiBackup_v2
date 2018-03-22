# -*- coding: utf-8 -*-
# by Part!zanes 2018

totalReport =  { 'accounts':{} }
totalAccount = 0
counter = 0

### COUNTER SYSTEM ###
def process_item():
    global counter
    counter += 1
    return counter

def getTotalAccount():
    global totalAccount
    return totalAccount

def appendToTotalAccount(count):
    global totalAccount
    totalAccount += count
######################


### STATISTIC ###
#def updateSystemReport(key, value):
#    dict[key] = value

def updateUserReport(username, key, value):
  try:
    dict['accounts'][username]
  except KeyError:
    dict['accounts'][username] = {}
    
  
  dict['accounts'][username][key] = value

def getTotalReport():
    return dict
#################



