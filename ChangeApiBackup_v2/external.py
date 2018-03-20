# -*- coding: utf-8 -*-
# by Part!zanes 2018

from log import mainLog
from ssh import runOverSSH
from const import SSH_DIST, REMOTE_SERVER
from internal import getCurrentDate, getLastDate


# Создает на удаленном сервере директорию с текущим днем
def createCurrentBackupDir():
    return runOverSSH('mkdir {0}/{1}'.format(SSH_DIST, getCurrentDate()))

# Проверяет существование предыдущей директории резервной копии
def lastBackupExits(username):
    return runOverSSH('stat {0}/{1}/{2}'.format(SSH_DIST, getLastDate(), username))

## Проверяет существование текущий директории резервного копирования
def currentBackupExits(username):
    return runOverSSH('stat {0}/{1}/{2}'.format(SSH_DIST, getCurrentDate(), username))

# Производит копирование на удаленном сервере предыдущего дня в текущий с использованием хардлинков
# при существовании предыдущей копии и отсутствием текущей
# в случае наличия текущей копии возвращает False без действий
def createHardlinkCopy(username):
    if(lastBackupExits(username) and not currentBackupExits(username)):
        return runOverSSH('cp -nlar {0}/{1}/{3} {0}/{2}/')
    elif(currentBackupExits(username)):
        return False