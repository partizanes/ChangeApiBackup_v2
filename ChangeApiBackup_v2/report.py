# -*- coding: utf-8 -*-
# by Part!zanes 2018

from log import mainLog
from db import database
from const import DBPATH, DBTABLE
from internal import createDatebaseDir, getCurrentDate


# Создаем папку для базы данных
createDatebaseDir()

# Инициализируем подключение к базе данных
db = database(filename = DBPATH, table = DBTABLE)

# Создание структуры таблицы
db.sql_do("""
            CREATE TABLE IF NOT EXISTS `report` (
	            `date`	datetime,
	            `username`	varchar(16),
	            `hardlinkCopy`	INTEGER DEFAULT 0,
	            `pkgAcct`	INTEGER DEFAULT 0,
	            `rsyncStatus`	INTEGER DEFAULT 0,
	            `changeApiSync`	INTEGER DEFAULT 0,
                `suspended`     INTEGER DEFAULT 0,
	            `executeTime`	INTEGER
            )
""")

def createUserReport(username):
    db.sql_do("INSERT OR IGNORE INTO {0} VALUES (DATE('now','localtime'), '{1}', 0, 0, 0, 0, 0, 0)".format(DBTABLE, username))

def updateUserReport(username, key, value):
    db.sql_do("UPDATE {0} SET {1} = {2} where `date` = DATE('now','localtime') and username = '{3}'".format(DBTABLE, key, value, username))

def cleanUpReport():
    #print(db.retrieveAll("SELECT * FROM report WHERE (`date` <= DATE('now', 'localtime', '-5 days'))"))
    mainLog.debug("[cleanUpReport] Запускаем очистку базы данных отчетов от устаревших данных.")
    db.sql_do("DELETE FROM report WHERE (`date` <= DATE('now', 'localtime', '-5 days'))")

def dict_from_row(row):
    return dict(zip(row.keys(), row)) 

def getTotalReport(time):
    output = "Дата отчета: {0}. Время выполения: {1}  \n".format(getCurrentDate(), time)

    # Получаем список аккаунтов с успешным копированием 
    answer = db.retrieveOne("SELECT COUNT(*) FROM report WHERE (`date` = DATE('now', 'localtime')) AND (`rsyncStatus` = 1 OR `changeApiSync` = 1) AND `hardlinkCopy` = 1 AND `pkgAcct` = 1")
    
    if(answer):
        output += "\nКоличество аккаунтов с успешно завершеной резервной копией: {0}\n\n".format(answer['COUNT(*)'])
    #########################################################################################

    # Список новых аккаунтов
    answer = db.retrieveOne("SELECT * FROM report WHERE (`date` = DATE('now', 'localtime')) AND `hardlinkCopy` = 0 AND `username` NOT IN (SELECT `username` FROM report WHERE (`date` = DATE('now', 'localtime', '-1 days')))")
    
    if(answer):
        output += "\nНовые аккаунты:\n"

    for row in answer:
        userReport = dict_from_row(row)
        output += "Username: {0: <16} pkgAcct: {1: <3} rsyncStatus: {2: <3} executeTime: {3: <3}\n".format(
                userReport['username'], userReport['pkgAcct'], userReport['rsyncStatus'], userReport['executeTime'])
    #########################################################################################

    # Получаем список аккаунтов с неудачным резервным копированием 
    answer = db.retrieveAll("SELECT * FROM report WHERE (`date` = DATE('now', 'localtime')) AND `rsyncStatus` = 0 AND `changeApiSync` = 0 AND `suspended` = 0")
    
    if(answer):
        output += "\nСписок аккаунтов с неудачным резервным копированием:\n"
        
        for row in answer:
            userReport = dict_from_row(row)
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                userReport['username'], userReport['hardlinkCopy'], userReport['pkgAcct'], userReport['rsyncStatus'], userReport['changeApiSync'], userReport['suspended'], userReport['executeTime'])
    #########################################################################################


    # Получаем список аккаунтов для который не удалось создать предварительную hardlink копию
    answer = db.retrieveAll("SELECT * FROM report WHERE (`date` = DATE('now', 'localtime')) AND `hardlinkCopy` = 0 AND `username` IN (SELECT `username` FROM report WHERE (`date` = DATE('now', 'localtime', '-1 days')))")
    
    if(answer):
        output += "\nПредварительная hardlink копия не создана или уже существует:\n"
        
        for row in answer:
            userReport = dict_from_row(row)
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                userReport['username'], userReport['hardlinkCopy'], userReport['pkgAcct'], userReport['rsyncStatus'], userReport['changeApiSync'], userReport['suspended'], userReport['executeTime'])
    #########################################################################################

    # Получаем список аккаунтов с неудачным pkgAcct
    answer = db.retrieveAll("SELECT * FROM report WHERE (`date` = DATE('now', 'localtime')) AND `pkgAcct` = 0")
    
    if(answer):
        output += "\nPkgAcct завершился с ошибками:\n"
        
        for row in answer:
            userReport = dict_from_row(row)
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                userReport['username'], userReport['hardlinkCopy'], userReport['pkgAcct'], userReport['rsyncStatus'], userReport['changeApiSync'], userReport['suspended'], userReport['executeTime'])
    #########################################################################################

    return output

    