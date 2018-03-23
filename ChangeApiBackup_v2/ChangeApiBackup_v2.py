#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# by Part!zanes 2018

from multiprocessing import Process

from log import mainLog
from datetime import datetime
from internal import createFilelistDir, mountOverSSH, umountOverSSH
from external import createCurrentBackupDir
from apiService import getAccountsDict
from service import processingAccountData
from mail import alertToSupport
from report import cleanUpReport, getTotalReport

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
    proc = Process(target=processingAccountData, args=(accountsPartitionList[partition],))
    procs.append(proc)
    proc.start()

for proc in procs:
    proc.join()

# TODO Архивация удаленных аккаунтов

# TODO Удаленние устаревших данных резервных копий

# TODO implement cleanup fileslist/date dirs old then 5 days

# Очистка базы данных от старых отчетов (более 5 дней)
cleanUpReport()

# Проводим размонтирование раздела sshfs
umountOverSSH()

# Считаем время исполнения скрипта
executionTime = datetime.now() - startTime

# Генерируем отчет
report = getTotalReport(executionTime)

# DEBUG TIMER END
mainLog.info("[MAIN] Скрипт завершен. Время выполнения: {0} ".format(executionTime))

print(report)