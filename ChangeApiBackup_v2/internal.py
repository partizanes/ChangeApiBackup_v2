# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os, sys, subprocess

from log import mainLog
from datetime import datetime, timedelta
from const import REMOTE_SERVER, FILELIST_DIR, SSH_DIST, LOCAL_DIST

### FILELIST ###
def createFilelistDir():
    mainLog.info("[createFilelistDir] Создаем папку для временного хранения списка измененных файлов.")

    try:

        pathToFilelist = "{0}/{1}".format(os.path.dirname(os.path.realpath(sys.argv[0])), FILELIST_DIR)

        if(not os.path.isdir(pathToFilelist)):
            os.mkdir(pathToFilelist)

        pathToFilelistCurrenttDate = '{0}/{1}/{2}'.format(os.path.dirname(os.path.realpath(sys.argv[0])), FILELIST_DIR, getCurrentDate())

        if(not os.path.isdir(pathToFilelistCurrenttDate)):
            os.mkdir(pathToFilelistCurrenttDate)

        return True
    except Exception as exc:
        return exc.args

def createFilesList(filesList, account):
    path = "{0}/{3}/{1}/{2}".format(os.path.dirname(os.path.realpath(sys.argv[0])), getCurrentDate() , account.user, FILELIST_DIR)
    mainLog.debug("[createFilesList] {0}".format(path))

    try:
        file = open(path, 'w')
        file.write('\n'.join(filesList))
        file.close()
        return True

    except Exception as exc:
        mainLog.error("[createFilesList][{0}] {1}".format(account.user, exc.args))
        return False
################

### DATETIME ###
def getLastDate():
    return str(datetime.today() - timedelta(days=1)).split()[0]

def getCurrentDate():
    return str(datetime.today()).split()[0]

def getSubDayDate(day):
    """ Возвращает дату минус количество дней"""
    return str(datetime.today() - timedelta(days=day)).split()[0]

################

### COMMAND ###
def runCommand(cmd):
    answer = os.system(cmd)

    if(answer == 0):
        return True

    return False

def runCommandWithAnswer(cmd, cwd='.'):

    p = subprocess.Popen(cmd.split(), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    return ({'success': True if p.returncode == 0 else False , 'out': out.decode("utf-8"), 'err': err.decode("utf-8")})
################

### MOUNT ###
def mountOverSSH():
    mainLog.info("[mountOverSSH] Монтируем sshfs раздел.")

    answer = runCommandWithAnswer('sshfs {REMOTE_SERVER}:{SSH_DIST} {LOCAL_DIST}'.format(REMOTE_SERVER=REMOTE_SERVER, SSH_DIST=SSH_DIST, LOCAL_DIST=LOCAL_DIST))

    if(answer['success']):
        mainLog.info("[mountOverSSH] sshfs смонтирован.")
        return True
    elif('mountpoint is not empty' in answer['err']):
        mainLog.warning("[mountOverSSH] sshfs уже смонтирован.")
        return True
    else:
        mainLog.error("[mountOverSSH][Exception] {0}".format(answer))
        exit()

def umountOverSSH():
    mainLog.info("[umountOverSSH] Размонтируем sshfs раздел.")

    answer = runCommandWithAnswer('umount {LOCAL_DIST}'.format(LOCAL_DIST=LOCAL_DIST))

    if(answer['success']):
        mainLog.info("[umountOverSSH] sshfs размонтирован.")
        return True
    else:
        mainLog.error("[umountOverSSH][ERROR] {0}".format(answer))
        return False
################

### DIR ###
def getListDir(path):
    if(os.path.isdir(path)):
        return os.listdir(path)

    mainLog.error("[getListDir][EXCEPTION] Директория недоступна: {0}".format(path))
    return []
################    

### SIZE UTIL ###

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

################  