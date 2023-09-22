#!/usr/bin/env python3.7
# coding=utf-8

import csv
import datetime
import logging,sys,os
from datetime import date, timedelta
import pymssql


def updateLead(leadParam):
    closureHour = '19:00'
    currentDate = datetime.datetime.now()
    # print (len(leadParam))
    for i in range(len(leadParam)):
        rappelStart = leadParam[i][1][0]
        addTime = datetime.timedelta(minutes=3)
        newDate = currentDate + addTime
        print('indice: ', leadParam[i][0])
        logging.debug('indice: %s', leadParam[i][0])
        print('date en cour:', currentDate)
        logging.debug('date en cour: %s', currentDate)
        if compareHour(newDate, closureHour):
            print('closure hour attempted')
            logging.debug('closure hour attempted')
            currentDate = currentDate + datetime.timedelta(days=1)
            currentDate = currentDate.replace(hour=9, minute=5)
        else:
            print('valid time')
            logging.debug('valid time')
            currentDate = newDate
        rappelDate = rappelStart + formatTime(currentDate)
        print(leadParam[i][1], ' => ', rappelDate)
        logging.debug('%s => %s', leadParam[i][1], rappelDate)
        print()
        logging.debug('')
        indiceUpdate = str(leadParam[i][0])
        print(indiceUpdate)
        updateRequest(indiceUpdate, rappelDate)


def readCsv(pathArg):
    file = open(pathArg)
    fileReader = csv.reader(file)
    rows = []
    for row in fileReader:
        rows.append(row)
    file.close()
    return rows


def GetIndice() :
    rows = []
    query = """
         SELECT indice from [C1_31_RA_EDOUARD_DENIS] 
         WHERE priorite in (0,-1000,-989,-11,-10) and status in (92,93,94,95) and
         convert(varchar(8), substring(convert (varchar ,rappel),2,10) ) < convert (varchar(8) , getdate() ,112)
    """
    cursor.execute(query)
    data = cursor.fetchall()
    print(str(data))
    if not data :
        print("Pas d'indice trouver")
        logging.debug("pas d'indice trouver")
        sys.exit()
    for row in data : 
        rows.append(row)
    return rows    

def getLead(tabIndice):
    # print("izy", len(tabIndice))
    res = []
    try:
        # [PROD_EDOUARD].[dbo].[C1_31_RA_EDOUARD_DENIS]
        querySelect = """SELECT indice,rappel FROM [PROD_EDOUARD].[dbo].[C1_31_RA_EDOUARD_DENIS] as tb 
        where indice in ( %s ) """ % tabIndice

        cursor.execute(querySelect)
        res = cursor.fetchall()

    except pymssql.StandardError as e:
        print('exception select: ', e)
        logging.debug('exception select %s', e)

    # except Exception as eCommon:
    #    print('exception code: ', eCommon)
    #    logging.debug('exception code %s', eCommon)

    return res
    # logging.debug(today)
    # logging.debug()


def formatTime(timeParam):
    return timeParam.strftime("%Y%m%d%H%M")


def compareHour(dateTest, hourRef):
    hourTest = dateTest.time()
    HourRef = datetime.time.fromisoformat(hourRef)
    if hourTest > HourRef:
        return True
    return False


def updateRequest(indices, rappel):
    queryUpdate = """update [PROD_EDOUARD].[dbo].[C1_31_RA_EDOUARD_DENIS] set priorite = '0', rappel = '%s'
    where indice in ( %s )""" % (rappel, indices)

    try:
        cursor.execute(queryUpdate)
        conn.commit()
    except pymssql.StandardError as e:
        print('exception update: ', e)
        print()
        logging.debug('exception update %s', e)
        logging.debug('')


# main
conn = pymssql.connect('5.196.127.163', 'read_write', '0wY!3M8cQ#Kw', 'PROD_EDOUARD')
cursor = conn.cursor()

a = GetIndice()
a = str(a)
a = a.replace(",)" , "")
a = a.replace(", (" , ",")
a = a [2 :len(a)-1]
print(a)
#sys.exit()
# indiceTab = []
# lead = []
aujourdhui = date.today()
logName = '//home//user1//programme_python//logs//ra_ed_'+ str(aujourdhui).replace('-','') +'.log'
print (logName)
logging.basicConfig(filename=logName,level=logging.DEBUG)
indiceTab = a
lead = getLead(indiceTab)
# print(lead)
total = len(lead) 
try:
    updateLead(lead)
    print('fiche total:', total)
    logging.debug('fiches totales: %s', total)
except Exception as eCommon:
    print('exception code: ', eCommon)
    logging.debug('exception code %s', eCommon)

# for line in lead:
#    print(line)

conn.close()
