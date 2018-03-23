# -*- coding: utf-8 -*-
# by Part!zanes 2018

import sqlite3

class database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table')

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()

    def retrieveOne(self, sql):
        cursor = self._db.execute(sql)
        answer = cursor.fetchone()
        return (dict(answer) if answer else None)

    def retrieveAll(self, sql):
        cursor = self._db.execute(sql)
        answer = cursor.fetchall()
        return answer if answer else None

    @property
    def filename(self): return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self): self.close()

    @property
    def table(self): return self._table

    @table.setter
    def table(self, t): self._table = t

    @table.deleter
    def table(self): self._table = 'report'

    def close(self):
        self._db.close()
        del self._filename