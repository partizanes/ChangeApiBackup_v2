# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os

from datetime import datetime, timedelta

def createFilelistDir():
    if(not os.path.isdir('fileslist')):
        os.mkdir('fileslist')

    path = 'fileslist/{0}'.format(getCurrentDate())

    if(not os.path.isdir(path)):
        os.mkdir(path)

    # TODO implement cleanup fileslist/date dirs old then 5 days


### DATETIME ###
def getLastDate():
    return str(datetime.today() - timedelta(days=1)).split()[0]

def getCurrentDate():
    return str(datetime.today()).split()[0]
################
