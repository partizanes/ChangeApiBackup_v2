# -*- coding: utf-8 -*-
# by Part!zanes 2018

import sqlite3
import threading

from const import DBPATH

class LockableSqliteConnection(object):
    def __init__(self, dburi):
        self.lock = threading.Lock()
        self.connection = sqlite3.connect(dburi, uri=True, check_same_thread=False)
        self.cursor = None
    
    def __enter__(self):
        self.lock.acquire()
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, type, value, traceback):
        self.lock.release()
        self.connection.commit()
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

lock = LockableSqliteConnection(DBPATH)

def sql_do(sql):
    with lock:
        lock.cursor.execute(sql)

def retrieveOne(sql):
    with lock:
        cursor = lock.cursor.execute(sql)
        answer = lock.cursor.fetchone()

        return answer 

def retrieveAll(sql):
    with lock:
        cursor = lock.cursor.execute(sql)
        answer = cursor.fetchall()

        return answer