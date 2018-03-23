# -*- coding: utf-8 -*-
# by Part!zanes 2018

from log import mainLog
from ssh import runRemoteSshWithShell
from const import SSH_DIST, REMOTE_SERVER
from internal import getCurrentDate, getLastDate


# Создает на удаленном сервере директорию с текущим днем
def createCurrentBackupDir():
    mainLog.info("[createCurrentBackupDir] Создаем папку резервного копирования с текущей датой.")
    return runRemoteSshWithShell('mkdir {0}/{1}'.format(SSH_DIST, getCurrentDate()))

# Проверяет существование предыдущей директории резервной копии
def lastBackupExits(username):
    return runRemoteSshWithShell('stat {0}/{1}/{2}'.format(SSH_DIST, getLastDate(), username))

## Проверяет существование текущий директории резервного копирования
def currentBackupExits(username):
    return runRemoteSshWithShell('stat {0}/{1}/{2}'.format(SSH_DIST, getCurrentDate(), username))

# Производит копирование на удаленном сервере предыдущего дня в текущий с использованием хардлинков
# при существовании предыдущей копии и отсутствием текущей
# в случае наличия текущей копии возвращает False без действий
def createHardlinkCopy(username):
    #mainLog.error("[createHardlinkCopy] lastBackupExits: {0} currentBackupExits: {1} total: {2}".format(lastBackupExits(username), currentBackupExits(username), (lastBackupExits(username) and not currentBackupExits(username))))

    if(lastBackupExits(username) and not currentBackupExits(username)):
        mainLog.info("[createHardlinkCopy][{0}] Создание hardlink копии over ssh".format(username))
        return runRemoteSshWithShell('cp -nlar {0}/{1}/{3} {0}/{2}/'.format(SSH_DIST, getLastDate(), getCurrentDate(), username, REMOTE_SERVER))

    elif(currentBackupExits(username)):
        mainLog.info("[createHardlinkCopy][{0}] Обнаружена текущая копия, будет произведен rsync.".format(username))
        return False