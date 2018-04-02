# -*- coding: utf-8 -*-
# by Part!zanes 2018

import os, sys, logzero
from logzero import setup_logger
from internal import getCurrentDate

path = "{0}/logs".format(os.path.dirname(os.path.realpath(sys.argv[0])))

if not os.path.exists(path):
    os.makedirs(path)

logFormatter = logzero.LogFormatter(fmt=u'%(color)s[%(asctime)s][%(levelname)s] %(message)s', datefmt=u'%Y-%m-%d %H:%M:%S')
mainLog = setup_logger(name="mainLog", logfile="{0}/mainlog_{1}.log".format(path, getCurrentDate().replace('-','_')), formatter=logFormatter)