# -*- coding: utf-8 -*-
# by Part!zanes 2018

from log import mainLog
from const import REMOTE_SERVER

def runOverSSH(subcmd):
    """ Runs the subcmd over ssh, you must 
        ensure that all special characters are 
        escaped in the subcommand.
        Return bool result of execution.
    """  

    command = "ssh {REMOTE_SERVER} '{subcmd}'".format(REMOTE_SERVER=REMOTE_SERVER, subcmd=subcmd)
    answer  = os.system(command)

    mainLog.debug("[runOverSSH][command] {0} [answer] {1}".format(command, answer))

    if(answer == 0):
        return True

    return False