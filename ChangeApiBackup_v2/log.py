# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os, logzero
from logzero import setup_logger

if not os.path.exists('logs'):
    os.makedirs('logs')

logFormatter = logzero.LogFormatter(fmt=u'%(color)s[%(asctime)s][%(levelname)s] %(message)s', datefmt=u'%Y-%m-%d %H:%M:%S')
mainLog = setup_logger(name="mainLog", logfile="logs/mainlog.log", formatter=logFormatter)