# -*- coding: utf-8 -*-
# by Part!zanes 2018

import re
import subprocess

from log import mainLog
from const import REMOTE_SERVER
from cpanelAccount import cpanelAccount
from mail import alertToSupport

def getAccountsDict():
    try:
      mainLog.info("[getAccountsDict] Получаем список аккаунтов с whmapi1...")

      command = "/sbin/whmapi1 listaccts want=user,uid,partition,suspended"
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = process.communicate()

      cpanelAccountsDict = {}

      lines = str(output).split('-')

      for line in lines:
          try:
              partition = 'hosting/home' if (re.search(r'partition: (.+?)\\n', line).group(1) == 'hosting') else 'hosting2'
              suspended = re.search(r'suspended: (.+?)\\n', line).group(1)
              uid       = re.search(r'uid: (.+?)\\n', line).group(1)
              user      = re.search(r'user: (.+?)\\n', line).group(1)

              try:
                  cpanelAccountsDict[partition]
              except KeyError:
                  cpanelAccountsDict[partition] = {}

              try:
                  cpanelAccountsDict[partition][user]
              except KeyError:
                  cpanelAccountsDict[partition][user] = []

              cpanelAccountsDict[partition][user].append(cpanelAccount(user, partition, suspended, uid))

          except Exception as exc:
              pass

      mainLog.info("[getAccountsDict] Найдено {0} аккаунтов".format(sum(len(cpanelAccountsDict[partition]) for partition in cpanelAccountsDict)))

      return cpanelAccountsDict

    except Exception as exc:
        mainLog.error("[{0}][getAccountsDict][Exception] {1} ".format(REMOTE_SERVER, exc.args))
        alertToSupport("[{0}][getAccountsDict]".format(REMOTE_SERVER), "[Exception] {0} ".format(exc.args))
        exit()