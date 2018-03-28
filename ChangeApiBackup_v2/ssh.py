# -*- coding: utf-8 -*-
# by Part!zanes 2018

import subprocess

from log import mainLog
from const import REMOTE_SERVER

def runRemoteSshWithShell(subcmd):
    """ Runs the subcmd over ssh, you must ensure that all special characters are
        escaped in the subcommand. Return bool result of execution.
    """

    cmd = "ssh {REMOTE_SERVER} '{subcmd}'".format(REMOTE_SERVER=REMOTE_SERVER, subcmd=subcmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()

    mainLog.debug("[runRemoteSshWithShell] {0}".format({'success': True if p.returncode == 0 else False , 'out': out.decode("utf-8"), 'err': err.decode("utf-8"), 'cmd': cmd}))

    if(p.returncode == 0):
        return True
    
    return False

def runRemoteSshWithShellAnswer(subcmd):
    """ Runs the subcmd over ssh, you must ensure that all special characters are
        escaped in the subcommand. Return bool result of execution.
    """

    cmd = "ssh {REMOTE_SERVER} '{subcmd}'".format(REMOTE_SERVER=REMOTE_SERVER, subcmd=subcmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()

    #mainLog.debug("[runRemoteSshWithShell] {0}".format({'success': True if p.returncode == 0 else False , 'out': out.decode("utf-8"), 'err': err.decode("utf-8"), 'cmd': cmd}))

    return ({'success': True if p.returncode == 0 else False , 'out': out.decode("utf-8"), 'err': err.decode("utf-8")})
    #if(p.returncode == 0):
    #    return True
    
    #return False