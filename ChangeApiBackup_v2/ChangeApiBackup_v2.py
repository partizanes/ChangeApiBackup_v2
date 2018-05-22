#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# by Part!zanes 2018

from multiprocessing import Process

from log import mainLog
from datetime import datetime
from internal import createFilelistDir, mountOverSSH, umountOverSSH
from external import createCurrentBackupDir, createAdditionalCopy ,checkFreeSpace
from apiService import getAccountsDict
from service import processingAccountData
from mail import alertToSupport
from report import cleanUpReport, getTotalReport
from archive import runBackupRemovedAccount, runRemoveOutdateArchive
from cleanup import runCleanupOldBackups, runCleanupFilelist

# DEBUG TIMER START
startTime = datetime.now()

# Создаем папку резервного копирования с текущей датой
createCurrentBackupDir()

# Создаем папку для временного хранения списка измененных файлов
createFilelistDir()

# Монтируем sshfs зависимость для pkgacct
mountOverSSH()

# Проверяем наличие свободного места на смонтированном разделе
checkFreeSpace()

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

# Дополнительные резервные копии
createAdditionalCopy()

# Архивация удаленных аккаунтов
runBackupRemovedAccount()

# Удаление устаревших архивов (более 6 месяцев)
runRemoveOutdateArchive()

# Удаленние устаревших данных резервных копий
runCleanupOldBackups()

# Удаление устаревших списков файлов для rsync
runCleanupFilelist()

# Очистка базы данных от старых отчетов (более 5 дней)
cleanUpReport()

# Проводим размонтирование раздела sshfs
umountOverSSH()

# Считаем время исполнения скрипта
executionTime = datetime.now() - startTime

# DEBUG TIMER END
mainLog.info("[MAIN] Скрипт завершен. Время выполнения: {0} ".format(executionTime))

# Генерируем отчет
mainLog.info(getTotalReport(executionTime))