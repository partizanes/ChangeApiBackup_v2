# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os, sys, time

from log import mainLog
from datetime import datetime
from external import createHardlinkCopy, lastBackupExits
from internal import runCommand, runCommandWithAnswer, getCurrentDate, createFilesList
from changeApi import getListOfChangedFiles
from const import days ,LOCAL_DIST, REMOTE_SERVER, SSH_DIST
from multiprocessing import Process
from statistic import process_item, getTotalAccount, updateUserReport

#### PKGACCT ####
def runPkgAcct(account):
    startTime = datetime.now()
    mainLog.debug('[runPkgAcct][{0}] Поток запущен'.format(account.user))

    cmd = '/usr/local/cpanel/scripts/pkgacct --skiphomedir --nocompress --skipquota --skiplogs --skipbwdata --backup --incremental {0} {1}/{2}/'.format(account.user, LOCAL_DIST, getCurrentDate())
    answer = runCommandWithAnswer(cmd)

    #mainLog.debug('[runPkgAcct][command] {0} [answer] {1}'.format(cmd, answer))
    mainLog.debug('[runPkgAcct][{0}] Поток завершен. Статус: {2}. Затраченное время: {1}'.format(account.user, datetime.now() - startTime, answer['success']))

    return answer['success']
###############

#### RSYNC ####
def runStandartRsync(account):
    startTime = datetime.now()
    mainLog.debug('[runStandartRsync][{0}] Поток запущен'.format(account.user))

    cmd = '/usr/bin/rsync -az  --delete . {3}:{1}/{2}/{0}/homedir/ '.format(account.user, SSH_DIST, getCurrentDate(), REMOTE_SERVER)
    answer = runCommandWithAnswer(cmd, cwd='/{0}/{1}'.format(account.partition, account.user))

    #mainLog.info('[runStandartRsync][command] {0} [answer] {1}'.format(cmd, answer))
    mainLog.debug('[runStandartRsync][{0}] Поток завершен. Статус: {2}. Затраченное время: {1}'.format(account.user, datetime.now() - startTime, answer['success']))

    return answer['success']
###############

#### RSYNC FILE ####
def runRsyncWithFilesList(account):
    try:
        startPath = os.path.dirname(os.path.realpath(sys.argv[0]))

        filesListPath = '{0}/fileslist/{1}/{2}'.format(startPath, getCurrentDate(), account.user)
        cmd = 'rsync -a --files-from={0} /{1}/{2}/ {4}:/backup3/s8_fcapi/{3}/{2}/homedir/'.format(
            filesListPath, account.partition, account.user,  getCurrentDate(), REMOTE_SERVER)
            
        #mainLog.info('[runRsyncWithFilesList][command] {0}'.format(command))
        #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, error = process.communicate()

        answer = runCommandWithAnswer(cmd)

        return answer['success']

    except Exception as exc:
        mainLog.error('[runRsyncWithFilesList][{0}] {1}'.format(account.user, exc.args))
###############

def runChangeApiRsync(account):
    # account is cpanelPartition(user,suspended,uid) 
    startTime = datetime.now()
    mainLog.debug('[runChangeApiRsync][{0}] Поток запущен.'.format(account.user))

    filesList = getListOfChangedFiles(account)

    if(len(filesList) == 0):
        mainLog.warning('[runChangeApiRsync][{0}] Файлов для синхронизации не обнаружено.'.format(account.user))
        return

    # Создание списка файлов для rsync
    if(createFilesList(filesList, account)):
        runRsyncWithFilesList(account)
        #TODO удаление файлов со списком синхронизации ?
    #else:
    #    mainLog.error('[createFilesList][{0}] Файл не был создан.'.format(account.user))
    #    # Отправить почту на support ?

    mainLog.debug('[runStandartRsync][{0}] Поток завершен. Затраченное время: {1}'.format(account.user, datetime.now() - startTime))


def runAccountBackup(account):
    startTime = datetime.now()
    mainLog.debug('[runAccountBackup][{0}] Поток запущен.'.format(account.user))

    status = createHardlinkCopy(account.user)
    updateUserReport(account.user, 'HardlinkCopy', status)
    #mainLog.error("createHardlinkCopy Status: {0}".format(status))

    pkgStatus = runPkgAcct(account)
    updateUserReport(account.user, 'PkgAcct', pkgStatus)

    if(int(account.suspended)):
        mainLog.debug("[runAccountBackup][{0}][{1}] Аккаунт приостановлен, копирование домашней директории отменено.".format(account.user, account.suspended))
        return

    # Копия уже существует , нету последней копии или сегодня день полной копии
    if(not status or not lastBackupExits(account.user) or days[datetime.today().strftime("%A")]):
        rsyncStatus = runStandartRsync(account)
        updateUserReport(account.user, 'rsyncStatus', rsyncStatus)
    else:
        changeApiStatus = runChangeApiRsync(account)
        updateUserReport(account.user, 'changeApiStatus', changeApiStatus)

    mainLog.debug('[runAccountBackup][{0}] Поток завершен. Затраченное время: {1}'.format(account.user, datetime.now() - startTime))
    updateUserReport(account.user, 'executeTime', datetime.now() - startTime)

def processingAccountData(accountsData):
    proc_count = []

    #current = 0
    #total   = len(accountsData)

    for account in accountsData:
        #current += 1
        
        mainLog.debug("[{0}/{1}] [{2}] Обработка аккаунта: {3}".format(process_item(), getTotalAccount(), accountsData[account][0].partition, accountsData[account][0].user))

        # Запуск runAccountBackup не более 6 потоков
        while(len(proc_count) > 6):
            
            #Очистка очереди процессов 
            for proc in proc_count:
             if not proc.is_alive():
                 proc_count.remove(proc)

            #mainLog.debug('[proc_count] more than 6. Sleeping...')
            time.sleep(0.5)
        
        proc = Process(target=runAccountBackup, args=(accountsData[account][0],))
        proc_count.append(proc)
        proc.start()