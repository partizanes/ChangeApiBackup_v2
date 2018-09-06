# -*- coding: utf-8 -*-
# by Part!zanes 2018

from log import mainLog
from const import DB_HOST, DB_NAME, DB_TABLE, DB_USER, DB_PASS, DB_ENCODING
from internal import getCurrentDate
from db import Datebase

db = Datebase(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_ENCODING)

def createUserReport(username):
    db.query("INSERT IGNORE INTO {0} VALUES (CURDATE(), '{1}', 0, 0, 0, 0, 0, 0)".format(DB_TABLE, username))

def updateUserReport(username, key, value):
    db.query("UPDATE {0} SET {1} = {2} WHERE `date` = CURDATE() AND username = '{3}'".format(DB_TABLE, key, value, username))

def cleanUpReport():
    #print(retrieveAll("SELECT * FROM report WHERE (`date` <= DATE('now', 'localtime', '-5 days'))"))
    mainLog.debug("[cleanUpReport] Запускаем очистку базы данных отчетов от устаревших данных.")
    
    db.query("DELETE FROM {0} WHERE `date` <= (CURDATE() - INTERVAL 5 DAY)".format(DB_TABLE))

def getTotalReport(time):
    output = "Дата отчета: {0}. Время выполения: {1}  \n".format(getCurrentDate(), time)

    # Получаем список аккаунтов с успешным копированием 
    answer = db.retrieveOne("SELECT COUNT(*) FROM {0} WHERE `date` = CURDATE() AND (`rsyncStatus` = 1 OR `changeApiSync` = 1 OR `suspended` = 1) AND `hardlinkCopy` = 1 AND `pkgAcct` = 1".format(DB_TABLE))

    if(answer):
        output += "\nКоличество аккаунтов с успешно завершеной резервной копией: {0}\n\n".format(answer[0])
    #########################################################################################

    # Список новых аккаунтов
    answer = db.retrieveAll("SELECT * FROM {0} WHERE `date` = CURDATE() AND `hardlinkCopy` = 0 AND `username` NOT IN (SELECT `username` FROM {0} WHERE `date` = CURDATE() - INTERVAL 1 DAY)".format(DB_TABLE))

    if(answer):
        output += "\nНовые аккаунты:\n"

        for row in answer:
            output += "Username: {0: <16} pkgAcct: {1: <3} rsyncStatus: {2: <3} executeTime: {3: <3}\n".format(row[1], row[3], row[4], row[7])
    #########################################################################################

    # Получаем список аккаунтов с неудачным резервным копированием 
    answer = db.retrieveAll("SELECT * FROM {0} WHERE `date` = CURDATE() AND `rsyncStatus` = 0 AND `changeApiSync` = 0 AND `suspended` = 0".format(DB_TABLE))
    
    if(answer):
        output += "\nСписок аккаунтов с неудачным резервным копированием:\n"
        
        for row in answer:
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    #########################################################################################


    # Получаем список аккаунтов для который не удалось создать предварительную hardlink копию
    answer = db.retrieveAll("SELECT * FROM {0} WHERE `date` = CURDATE() AND `hardlinkCopy` = 0 AND `username` IN (SELECT `username` FROM report WHERE `date` = CURDATE() - INTERVAL 1 DAY)".format(DB_TABLE))

    if(answer):
        output += "\nПредварительная hardlink копия не создана или уже существует:\n"
        
        for row in answer:
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    #########################################################################################

    # Получаем список аккаунтов с неудачным pkgAcct
    answer = db.retrieveAll("SELECT * FROM {0} WHERE `date` = CURDATE() AND `pkgAcct` = 0".format(DB_TABLE))
    
    if(answer):
        output += "\nPkgAcct завершился с ошибками:\n"
        
        for row in answer:
            output += "Username: {0: <16} hardlinkCopy: {1: <3} pkgAcct: {2: <3} rsyncStatus: {3: <3} changeApiSync: {4: <3} suspended: {5: <3} executeTime: {6: <3}\n".format(
                row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    #########################################################################################

    return output