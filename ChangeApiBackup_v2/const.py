# -*- coding: utf-8 -*-
# by Part!zanes 2018

REMOTE_SERVER = 'user@server'
SSH_DIST      = 'pathToBackupDir'

EMAIL_FROM    = 'user@server'
MAIL_TO       = ['user@server', 'user@server']
SMTP_SERVER   = 'localhost'

# 1 - Full copy (rsync)
# 0 - Only changes (cloudlinux changeApi)
days = {
    'Monday'    : 1,
    'Tuesday'   : 0,
    'Wednesday' : 0,
    'Thursday'  : 1,
    'Friday'    : 0,
    'Saturday'  : 0,
    'Sunday'    : 0
    }