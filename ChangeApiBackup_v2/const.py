# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os,sys

REMOTE_SERVER = 'user@server'
SSH_DIST      = 'pathToBackupDir'
LOCAL_DIST    = 'pathToLocalDir'

FILELIST_DIR  = 'fileslist'

EMAIL_FROM    = 'user@server'
MAIL_TO       = ['user@server', 'user@server']
SMTP_SERVER   = 'localhost'

DB_HOST       = 'localhost'
DB_NAME       = 'database'
DB_TABLE      = 'table'
DB_USER       = 'user'
DB_PASS       = 'password'
DB_ENCODING   = 'utf8'

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