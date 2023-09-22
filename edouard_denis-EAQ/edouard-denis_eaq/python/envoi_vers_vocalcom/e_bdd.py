#!/usr/bin/env python
# -*- coding: cp1252  -*-

import psycopg2
import psycopg2.extras


class CurrentDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=saisie user=postgres password=123456  host= localhost")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
        
    def getfieldslist(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            ret.append(s_nom)
        return ret
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()

    def runSql(self,ssql):
        self.request = ssql
        self.docomand()


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dmin(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getfieldsstruct(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            s_typ = self.transformtype( str(rs["data_type"]) )
            arr = {}
            arr["fieldname"] = s_nom
            arr["fieldtype"] = s_typ
            ret.append(arr)
        return ret

    def transformtype(self,stypename):
        ret = "text"
        type_for_string = ["""char""","character","character varying","text"]
        type_for_num = ["real","bigint","integer","numeric","smallint"]
        type_for_date = ["timestamp with time zone","timestamp without time zone","date"]
        if stypename in type_for_string:
            ret = "text"
        elif stypename in type_for_num:
            ret = "num"
        elif stypename in type_for_date:
            ret = "date"
        else:
            ret = "text"
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret

    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None


class ProdDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=production user=pgtantely password=PasyVao2h2011  host= mcserver1.madcom.local")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor);
#        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
#        self.curseur  = self.db.cursor();

    def getfieldslist(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            ret.append(s_nom)
        return ret

    def getfieldsstruct(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            s_typ = self.transformtype( str(rs["data_type"]) )
            arr = {}
            arr["fieldname"] = s_nom
            arr["fieldtype"] = s_typ
            ret.append(arr)
        return ret

    def transformtype(self,stypename):
        ret = "text"
        type_for_string = ["""char""","character","character varying","text"]
        type_for_num = ["real","bigint","integer","numeric","smallint"]
        type_for_date = ["timestamp with time zone","timestamp without time zone","date"]
        if stypename in type_for_string:
            ret = "text"
        elif stypename in type_for_num:
            ret = "num"
        elif stypename in type_for_date:
            ret = "date"
        else:
            ret = "text"
        return ret
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dmin(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret



    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None


class SdsiDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=sdsi user=prep1 password=pp1p  host= 1mcserver1.madcom.local")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()

    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None


class ClientDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=nomination_etl port=5433 user=iscc password=R9mtA}&7  host= 192.168.10.43")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dmin(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret



    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None

class SauvDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=Call_database user=pgtantely password=PasyVao2h2011  host= 192.168.10.70")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);

    def getfieldslist(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            ret.append(s_nom)
        return ret

    def getfieldsstruct(self,nomtable):
        ret = []
        sql_schema = "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='%s'  ORDER BY ordinal_position" %(nomtable)
        trs = self.openrecordset(sql_schema)
        for rs in trs:
            s_nom = str(rs["column_name"])
            s_typ = self.transformtype( str(rs["data_type"]) )
            arr = {}
            arr["fieldname"] = s_nom
            arr["fieldtype"] = s_typ
            ret.append(arr)
        return ret

    def transformtype(self,stypename):
        ret = "text"
        type_for_string = ["""char""","character","character varying","text"]
        type_for_num = ["real","bigint","integer","numeric","smallint"]
        type_for_date = ["timestamp with time zone","timestamp without time zone","date"]
        if stypename in type_for_string:
            ret = "text"
        elif stypename in type_for_num:
            ret = "num"
        elif stypename in type_for_date:
            ret = "date"
        else:
            ret = "text"
        return ret
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dmin(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret



    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None


class SdsiDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=sdsi user=prep1 password=pp1p  host= 1mcserver1.madcom.local")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()

    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None


class ClientDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=nomination_etl port=5433 user=iscc password=R9mtA}&7  host= 192.168.10.43")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
        
    def docomand(self):
        self.curseur.execute(self.request)

    def execute(self):
        self.curseur.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dmin(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            if tbret[0]['theretour']==None:
                ret = ""
            else:                
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere
            
        self.curseur.execute(ssql)
        tbret = self.curseur.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        return ret



    def runSql(self,ssql):
        self.request = ssql
        self.docomand()

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur.execute(ssql)
        tdate = self.curseur.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])
        
        imois = int(tb[1])
        ijour = int(tb[2])
        
        if ijour<10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret



    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur = None



