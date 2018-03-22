# -*- coding: utf-8 -*-
# by Part!zanes 2018

import time

from log import mainLog
from internal import runCommandWithAnswer


def getListOfChangedFiles(account):
    timestamp = int(time.time() - 90000)

    try:
        cmd = '/usr/bin/cloudlinux-backup-helper -u {0} -t {1}'.format(account.uid, timestamp)
        answer = runCommandWithAnswer(cmd)

        #mainLog.info('[getListOfChangedFiles][command] {0} [answer] {1}'.format(cmd, answer))

        # При большом количестве обращений база данных может быть заблокирована.
        if('database is locked' in answer['err']):
            mainLog.error('[getListOfChangedFiles] База данных заблокирована. Повторяем запрос.')
            return getListOfChangedFiles(account)

        if(answer['success']):
            output = answer['out'].splitlines()
            filesList = []
                
            prefix = '{0}:/{1}/{2}/'.format(account.uid, account.partition, account.user)

            for line in output:
                if(prefix in line):
                    line = line.replace(prefix, '')

                    if('//deleted' in line):
                        mainLog.warning("[getListOfChangedFiles] Удаляем из списка синхронизации: {0}".format(line))

                        try:
                            filesList.remove(line.replace('//deleted',''))
                        except:
                            mainLog.error("[getListOfChangedFiles][EXCEPTION][REMOVE] fileline: {0}".format(filesList, ))
                            pass
                    else:
                        filesList.append(line)
                
            return filesList

        else:
            mainLog.error('[getListOfChangedFiles][{0}] Answer from change api don`t success. [answer] {1}'.format(account.user, answer))
            ##TODO Start Rsync --> this

    except Exception as exc:
        mainLog.error("[getListOfChangedFiles] {0}".format(exc.args))

    return []