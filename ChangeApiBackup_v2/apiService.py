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
      command = 'whmapi1 listaccts want=user,uid,partition,suspended'
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      output, error = process.communicate()

      cpanelAccountsDict = {}

      lines = str(output).split('-')

      for line in lines:
          try:
              m = re.search(' \\\\n      partition: (.+?)\\\\n      suspended: (.+?)\\\\n      uid: (.+?)\\\\n      user: (.+?)\\\\n', line)

              partition = 'hosting/home' if (m.group(1) == 'hosting') else m.group(1)
              suspended = m.group(2)
              uid       = m.group(3)
              user      = m.group(4)

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
              mainLog.error('[LineParse] {0}'.format(line))
              pass

      return cpanelAccountsDict

    except Exception as exc:
        mainLog.error('[{0}][getAccountsDict][Exception] {1} '.format(REMOTE_SERVER, exc.args))
        alertToSupport('[{0}][getAccountsDict]','[Exception] {1} '.format(REMOTE_SERVER, exc.args))
        exit()