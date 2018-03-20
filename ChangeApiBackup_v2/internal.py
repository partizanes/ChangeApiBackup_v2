# -*- coding: utf-8 -*-
# by Part!zanes 2018

def createFilelistDir():
    if(not os.path.isdir('fileslist')):
        os.mkdir('fileslist')

    path = 'fileslist/{0}'.format(getCurrentDate())

    if(not os.path.isdir(path)):
        os.mkdir(path)

    # TODO implement cleanup fileslist/date dirs old then 5 days