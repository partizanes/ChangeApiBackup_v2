# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os, time

from log import mainLog
from datetime import datetime
from ssh import runRemoteSshWithShell
from const import SSH_DIST, LOCAL_DIST, REMOTE_SERVER
from internal import getCurrentDate, getLastDate


# Создает на удаленном сервере директорию с текущим днем
def createCurrentBackupDir():
    mainLog.info("[createCurrentBackupDir] Создаем папку резервного копирования с текущей датой.")
    return runRemoteSshWithShell('mkdir -p {0}/{1}'.format(SSH_DIST, getCurrentDate()))

# Проверяет существование предыдущей директории резервной копии
def lastBackupExits(username):
    return runRemoteSshWithShell('stat {0}/{1}/{2}'.format(SSH_DIST, getLastDate(), username))

## Проверяет существование текущий директории резервного копирования
def currentBackupExits(username):
    return runRemoteSshWithShell('stat {0}/{1}/{2}'.format(SSH_DIST, getCurrentDate(), username))

def currentHomedirExits(username):
    return runRemoteSshWithShell('stat {0}/{1}/{2}/homedir'.format(SSH_DIST, getCurrentDate(), username))

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

def createAdditionalCopy():
    
    # weekly
    if(datetime.today().strftime("%A") == 'Sunday'):
        runRemoteSshWithShell('mkdir -p {0}/weekly'.format(SSH_DIST))

        mainLog.info("[createAdditionalCopy] Создание hardlink недельной копии.")
        success = runRemoteSshWithShell('cp -nlar {0}/{1} {0}/weekly/'.format(SSH_DIST, getCurrentDate(), REMOTE_SERVER))

        if(success):
            mainLog.info("[createAdditionalCopy] Недельная копия создана успешно.")

            answer = runRemoteSshWithShellAnswer("ls {0}/weekly/".format(SSH_DIST))

            if(answer['success']):
                listBackup = [str for str in answer['out'].splitlines() if re.match(r'\d{4}-\d\d-\d\d', str)]

                current_timestamp = int(time.time())
                more_fifteen_days = current_timestamp - 1296000

                for dateStr in listBackup:
                    backup_timestamp = int(datetime.strptime(dateStr, '%Y-%m-%d').timestamp())

                    if(more_fifteen_days > backup_timestamp):
                        mainLog.error("[createAdditionalCopy] Директория будет удалена: {0}/weekly/{1}".format(SSH_DIST, dateStr))
                        runRemoteSshWithShellAnswer("nohup ionice -c3 rm -rf {0}/weekly/{1} > /dev/null 2>&1 &".format(SSH_DIST, dateStr))
                        
                        mainLog.debug(answer)

    # monthly
    if(datetime.now().day == 1):
        runRemoteSshWithShell('mkdir -p {0}/monthly'.format(SSH_DIST))

        mainLog.info("[createAdditionalCopy] Создание hardlink месячной копии.")
        success = runRemoteSshWithShell('cp -nlar {0}/{1} {0}/monthly/'.format(SSH_DIST, getCurrentDate(), REMOTE_SERVER))

        if(success):
            mainLog.info("[createAdditionalCopy] Месячная копия создана успешно")

            answer = runRemoteSshWithShellAnswer("ls {0}/monthly/".format(SSH_DIST))

            if(answer['success']):
                listBackup = [str for str in answer['out'].splitlines() if re.match(r'\d{4}-\d\d-\d\d', str)]

                current_timestamp = int(time.time())
                more_monthly = current_timestamp - 2592000

                for dateStr in listBackup:
                    backup_timestamp = int(datetime.strptime(dateStr, '%Y-%m-%d').timestamp())

                    if(more_monthly > backup_timestamp):
                        mainLog.error("[createAdditionalCopy] Директория будет удалена: {0}/monthly/{1}".format(SSH_DIST, dateStr))
                        runRemoteSshWithShellAnswer("nohup ionice -c3 rm -rf {0}/monthly/{1} > /dev/null 2>&1 &".format(SSH_DIST, dateStr))

                        mainLog.debug(answer)


def createArchiveDir():
    archiveDirPath = "{0}/archive".format(LOCAL_DIST)
    
    if(not os.path.isdir(archiveDirPath)):
        os.mkdir(archiveDirPath)