#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# by Part!zanes 2018

from multiprocessing import Process

from log import mainLog
from datetime import datetime
from internal import createFilelistDir, mountOverSSH
from external import createCurrentBackupDir
from apiService import getAccountsDict
from service import processingAccountData
from mail import alertToSupport

from statistic import appendToTotalAccount, getTotalReport

# DEBUG TIMER START
startTime = datetime.now()


# Создаем папку резервного копирования с текущей датой
createCurrentBackupDir()

# Создаем папку для временного хранения списка измененных файлов
createFilelistDir()

# Монтируем sshfs зависимость для pkgacct
mountOverSSH()

# Получаем список аккаунтов сгрупированных по разделу
accountsPartitionList = getAccountsDict()

procs = []
    
mainLog.info("[MAIN] Запускаем каждый найденый раздел в отдельном потоке .")

for partition in accountsPartitionList:

    appendToTotalAccount(len(accountsPartitionList[partition]) + 1) 

    proc = Process(target=processingAccountData, args=(accountsPartitionList[partition],))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()


# TODO Архивация удаленных аккаунтов

# TODO Удаленние устаревших данных резервных копий
## TODO implement cleanup fileslist/date dirs old then 5 days

# Проводим размонтирование раздела sshfs
umountOverSSH()

# Выводим отчет
mainLog.warning("[Report] {0}".format(getTotalReport()))

# DEBUG TIMER END
mainLog.info("[MAIN] Скрипт завершен. Время выполнения: {0} ".format(datetime.now() - startTime))