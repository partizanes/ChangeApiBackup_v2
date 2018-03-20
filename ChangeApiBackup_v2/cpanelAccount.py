# -*- coding: utf-8 -*-
# by Part!zanes 2018

class cpanelAccount(object):
    def __init__(self, user, partition, suspended, uid):
        self.user      = user
        self.partition = partition
        self.suspended = suspended
        self.uid       = uid

