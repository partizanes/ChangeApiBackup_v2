# -*- coding: utf-8 -*-
# by julsi9/part!zanes 2018

import re, time, datetime

from log import mainLog
from const import SSH_DIST
from ssh import runRemoteSshWithShellAnswer

### CLEANUP ###
def runCleanupOldBackups():
    answer = runRemoteSshWithShellAnswer("ls {0}".format(SSH_DIST))
    #mainLog.debug("[runCleanupOldBackups][answer] {0}".format(answer))

    if(answer['success']):
        listBackup = [str for str in answer['out'].splitlines() if re.match(r'\d{4}-\d\d-\d\d', str)]

        if(len(listBackup) < 6):
            mainLog.warning("[runCleanupOldBackups] Количество резервных копий меньше 6")
            return False

        current_timestamp = int(time.time())
        more_five_days = current_timestamp - 432000

        for dateStr in listBackup:
            backup_timestamp = int(datetime.datetime.strptime(dateStr, '%Y-%m-%d').timestamp())

            if(more_five_days > backup_timestamp):
                mainLog.error("[runCleanupOldBackups] Директория будет удалена: {0}/{1}".format(SSH_DIST, dateStr))
                answer = runRemoteSshWithShellAnswer("nohup ionice -c3 rm -rf {0}/{1} > /dev/null 2>&1 &".format(SSH_DIST, dateStr))

                mainLog.debug(answer)
        return True
    else:
        mainLog.error("[runCleanupOldBackups] Не удалось получить список директорий с удаленного сервера.")
        return False
################
