# -*- coding: utf-8 -*-
# by Part!zanes 2018

import MySQLdb
from log import mainLog

class Datebase(object):
   def __init__(self, host, user, passwd, db, charset):
      self.conn = MySQLdb.connect(host=host, user=user,passwd=passwd, db=db, charset=charset)
      self.cur = self.conn.cursor()

   def rows(self):
      return self.cur.rowcount

   def __enter__(self):
      return Datebase()

   def __exit__(self, exc_type, exc_val, exc_tb):
      if self.conn:
         self.conn.close()

   def query(self,sql):
      try:
         self.conn.ping(True)
         self.cur.execute(sql)
      except Exception as exc:
         mainLog.error("[query] {0}".format(exc))

   def retrieveOne(self, sql):
      try:
         self.conn.ping(True)
         self.cur.execute(sql)

         answer = self.cur.fetchone()

         return answer
      except Exception as exc:
         mainLog.error("[retrieveOne] {0}".format(exc))

      return None

   def retrieveAll(self, sql):
      try:
         self.conn.ping(True)
         self.cur.execute(sql)

         answer = self.cur.fetchall()

         return answer

      except Exception as exc:
         mainLog.error("[retrieveAll] {0}".format(exc))

      return None
