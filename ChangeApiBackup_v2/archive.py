# -*- coding: utf-8 -*-
# by julsi9 2018

import os, socket

from log import mainLog
from const import SSH_DIST
from internal import getListDir, getLastDate, getCurrentDate

hostname = socket.gethostname().split('.')[0]

def getRemovedAccount():
    """ Определение списка удаленных аккаунтов """
    try:
        usersYesteraday = getListDir("{0}/{1}".format(SSH_DIST, getLastDate()))
        usersToday = getListDir("{0}/{1}".format(SSH_DIST, getCurrentDate()))

        removedList = set(usersYesteraday) - set(usersToday)

        return removedList

    except Exception as exc:
        mainLog.error("[getRemovedAccount][Exception] {0}".format(exc.args))
        return None


def runCreateArchive(username):
    """ Создание архива аккаунта в папку archive """

    command = "/bin/tar -czf {0}/archive/{1}.{2}.{3}.tar.gz -C {0}/{4}/{2} .".format(SSH_DIST, hostname, username, getCurrentDate(), getLastDate())
    answer = os.system(command)
    
    mainLog.debug("[runCreateArchive][command] {0}".format(command))
    
    if (answer == 0):
        mainLog.info("[runBackupRemovedAccount] Архив {0} успешно создан".format(username))
        return True    
        
    mainLog.error("[runBackupRemovedAccount][Exception] Архив {0} не создан".format(username))
    return False
    

def runBackupRemovedAccount():
    for username in getRemovedAccount():
        runCreateArchive(username)
        
