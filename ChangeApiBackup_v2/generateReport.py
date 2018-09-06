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

# Генерируем отчет
report = getTotalReport(datetime.now())
mainLog.info(report)
alertToSupport("Система резервного копирования", report, ["host_admins@ok.by"])
