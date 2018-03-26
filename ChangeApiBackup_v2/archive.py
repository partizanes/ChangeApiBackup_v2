# -*- coding: utf-8 -*-
# by julsi9 2018

import os, socket

from log import mainLog
from const import LOCAL_DIST
from datetime import datetime
from internal import getListDir, getLastDate, getCurrentDate

hostname = socket.gethostname().split('.')[0]

def getRemovedAccount():
    """ Определение списка удаленных аккаунтов """
    try:
        usersYesteraday = getListDir("{0}/{1}".format(LOCAL_DIST, getLastDate()))
        usersToday = getListDir("{0}/{1}".format(LOCAL_DIST, getCurrentDate()))

        if(not len(usersYesteraday) or not len(usersToday)):
            mainLog.error("[getRemovedAccount] Архивация отменена. getListDir вернул пустой список.")
            return []

        removedList = set(usersYesteraday) - set(usersToday)

        return removedList

    except Exception as exc:
        mainLog.error("[getRemovedAccount][Exception] {0}".format(exc.args))
        return None


def runCreateArchive(username):
    """ Создание архива аккаунта в папку archive """
    startTime = datetime.now()
    mainLog.info("[runCreateArchive][{0}] Запущен процесс создания архива...".format(username))

    command = "/bin/tar -czf {0}/archive/{1}.{2}.{3}.tar.gz -C {0}/{4}/{2} .".format(LOCAL_DIST, hostname, username, getCurrentDate(), getLastDate())
    mainLog.debug("[runCreateArchive][command] {0}".format(command))
    answer = os.system(command)
    
    if (answer == 0):
        mainLog.info("[runBackupRemovedAccount][{0}] Архив успешно создан. Затраченное время: {1}".format(username, datetime.now() - startTime))
        return True    
        
    mainLog.error("[runBackupRemovedAccount][Exception][{0}] При создании архива произошла ошибка.".format(username))
    return False
    

def runBackupRemovedAccount():
    listRemovedAccount = getRemovedAccount()

    mainLog.info("[runBackupRemovedAccount] Обнаружено {0} удаленных аккаунтов для архивации.".format(len(listRemovedAccount)))

    for username in listRemovedAccount:
        runCreateArchive(username)
        
