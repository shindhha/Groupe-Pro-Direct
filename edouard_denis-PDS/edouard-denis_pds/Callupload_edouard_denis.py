#! /usr/bin/python
# -*- coding: utf8  -*-

import unittest, time, re
import datetime
import time
import psycopg2
import psycopg2.extras
import glob
import os
import sys
import re
import psutil
from xml.dom import minidom
import pysftp

import zipfile
import shutil
import json
import base64
import pymssql
import requests 
#import urllib2
import ssl
import unidecode
import string


import datetime


#reload(sys)
#sys.setdefaultencoding("utf8")

PYTHONIOENCODING='UTF-8'






fichierlog = open("logs/" + os.path.basename(__file__) + ".log", "a")
lockFile='/var/tmp/' + os.path.basename(__file__) + '.lock'
#"""


class ProdDb():
    def __init__(self,sql=""):            
        self.db = None
        self.curseur_ = None
        self.setUp()
        self.request = sql
        
    def setRequest(self,ssql):
        self.request = ssql
        
    def setUp(self):
        self.db = psycopg2.connect("dbname=production user=pgtantely password=PasyVao2h2011  host= mcserver1.madcom.local")
        self.db.set_client_encoding('WIN1252') 
        self.db.set_isolation_level(0)
        self.curseur_  = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);
    
    def runSql(self,ssql):
        self.request = ssql
        self.docomand()
    
    def docomand(self):
        self.curseur_.execute(self.request)
    
    def execute(self):
        self.curseur_.execute(self.request)
    
    def openrecordset(self,ssql):
        self.request = ssql
        self.curseur_.execute(self.request)
        return self.curseur_.fetchall()
    
    def openrecordsetOne(self,ssql):
        self.request = ssql
        self.curseur_.execute(self.request)
        return self.curseur_.fetchone()
    


    def dcount(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self,champ,table,critere=""):
        ssql = ""
        if critere =="":            
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere
            
        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
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
            
        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
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
            
        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = ""
        if len(tbret)>0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        ret = str(tdate[1])       
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
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
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret


    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date -1 as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res=str(tdate[0])
        tb = res.split(ssep)
        
        ret = str(int(tb[1])) + "/" + str(int(tb[2])) + "/" + str(tb[0])
        return ret
    
    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
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

    def requete_select_mssql(self,mssql):
        self.req_select = mssql
        self.curseur_mssql.execute(self.req_select)
        
        return self.curseur_mssql.fetchall()
        

    def setNothing(self):
        self.db.close()
        self.db = None
        self.curseur_ = None
    






class Traitement():
    def set_error(self,num_err, val_err):
        self.error = num_err
        self.msg_error = val_err

    
   
     
     
    def clear_directories(self):
        try:                        
            folder = self.dir_zip
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    pass

            folder = self.dir_save
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    pass
                        
        except:
            pass
            
    
    def connect(hostname,username,password):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sms = "sms"
        with pysftp.Connection(host=hostname, username=username, password=password,port=2480,cnopts=cnopts) as sftp:
            sms = "connection succesfully"
            sftp = pysftp.Connection(host=hostname, username=username, password=password,port=2480,cnopts=cnopts)
        print (sms)


    def envoi_ftp(self):
        print ('debut envoie ftp')
        db_prod = ProdDb()
        flag_traitement = False
        req_name_file = " select trim(nom_client) ||' '||trim(prenom_client),trim(nom_commercial) ||' '|| trim(prenom_commercial),nom_fichier_mp3, date_call,statut,type_rdv from call_recording_edouard_denis where campaign ='%s' and (flag_up='N' or flag_up='E') and flag_down='O' order by date_call asc"%(self.campaign)
        print (req_name_file)
        name_file = db_prod.openrecordset(req_name_file)
        db_prod.setNothing()
#        return False
        
        try:
            connect("77.159.102.53","Put_RecordED","RecED31**")


        except :
            try:
                connect("77.159.102.53","Put_RecordED","RecED31**")
                
            except Exception as e:
                sms = "Erreur de connexion ftp :\n"+str(e)+"\n"
                print (sms)
                fichierlog.write(sms)
                self.erreur = True
                os.remove(lockFile)
                return                    
        
                
    
        self.nbr_envoi = 0
        if len(name_file)==0:
            sms = "Aucun element a envoye sur ftp\n"
            print (sms)
        else:            
            for fic in name_file:
#                if True:
                    
                try:
                    print (" *****************  ************")
                    db_prod = ProdDb()
                    nom_client_complet = fic[0]
                    nom_commercial_complet = fic[1]
                    fichier = fic[2]
                    date_call = fic[3]
                    statut = fic[4]
                    type_rdv = fic[5]
                    print ('nom client : ',nom_client_complet)
                    print ('nom commercial : ',nom_commercial_complet)
                    print ('nom fichier : ',fichier)
                    print ('date_call : ',date_call)
                    print ('statut : ',statut)
                    print ('Type RDV : ',type_rdv)
                    print("record: ",self.dir_record)
                    os.chdir(self.dir_record)
                    file = open(fichier, 'r')  
                                     
                    print (self.dir_fichier_client)
                    
                    sftp.cwd(self.dir_fichier_client)
                    try:
                        sftp.chdir(self.dir_fichier_client)
                    except IOError:
                        sftp.mkdir(self.dir_fichier_client)
                        sftp.chdir(self.dir_fichier_client)

                    rep_commercial = self.dir_fichier_client + nom_commercial_complet
                    try:
                        sftp.chdir(rep_commercial)
                    except IOError:
                        sftp.mkdir(rep_commercial)
                        sftp.chdir(rep_commercial)
                    
                    if statut == "ACCORD":
                        if "RDV" in type_rdv:
                            sousdossier = "RDV"
                        elif "TRANSFERT ABOUTI" == type_rdv:
                            sousdossier = "TRANSFERT ABOUTI"
                        elif "TRANSFERT NON ABOUTI" == type_rdv:
                            sousdossier = "TRANSFERT NON ABOUTI"
                    else:
                        sousdossier = "REFUS"
                    
                    rep_final = rep_commercial +'/'+ sousdossier +'/'
                    try:
                        sftp.chdir(rep_final)
                    except IOError:
                        sftp.mkdir(rep_final)
                        sftp.chdir(rep_final)
                    
                    
                      
                    #rep_date = date_call
                    #datem = datetime.datetime.strptime(str(rep_date), "%Y-%m-%d")
                    #year = datem.year
                    #rep_year = self.dir_fichier_client+str(year)        
                    #month = datem.month
                    #tab_month = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
                    #mois = tab_month[int(month)-1]                    
                    #rep_month = rep_year + "/" + str(mois)
                    #rep_final = rep_month + "/" + str(rep_date)
                    
                    
                    
 
                    print ("source: ",self.dir_record+fichier)
                    print ("dest: ",rep_final+"/"+fichier)

                    if (sftp.put(self.dir_record+fichier, rep_final+"/"+fichier)):                        
                        file.close()
                        print ('envoi ftp de ',fichier,' avec succes')                        
                        req_updt = " update call_recording_edouard_denis set flag_up = 'O', date_envoie =now()::date where campaign ='%s' and nom_fichier_mp3='%s' "%(self.campaign,fichier)
                        db_prod.runSql(req_updt)
                        self.nbr_envoi += 1
                        db_prod.setNothing()
                        
                        self.couper_livre(fichier)
                        
                          
                except Exception as e:
                    sms = "Erreur d'envoie du fichier :"+ str(fichier) +"\n"+str(e)+"\n"
                    req_updt_ = " update call_recording_edouard_denis set flag_down = 'N' where campaign ='%s' and nom_fichier_mp3='%s' "%(self.campaign,fichier)
                    db_prod.runSql(req_updt_)                    
                    print (sms)
                    fichierlog.write(sms)
                    self.erreur = True
                    
            #db_prod.setNothing()
            flag_traitement = True
            sms = "Nombre fichier envoyé sur ftp : "+str(self.nbr_envoi)+"\n"
            print (sms)
            print (flag_traitement)
        return flag_traitement

    
    def couper_livre(self,fichier):
        db_prod = ProdDb()
        req_name_file = " select nom_fichier_mp3 from call_recording_edouard_denis where campaign ='%s' and flag_up='O' and flag_down='O' and nom_fichier_mp3 = '%s' "%(self.campaign,fichier)
        name_file = db_prod.openrecordset(req_name_file)
        print (name_file)
            

        for fic in name_file:
            fichier = fic[0]
            try:
                print ('deplacement de '+str(fichier))
                shutil.move (self.dir_record  + fichier,self.dir_backup + fichier)
            except:
                print ("deplacement echoue de "+str(fichier))
        print ("fin deplacement")
        

        db_prod.setNothing()
    
    
    def __init__(self):
        try:
        #if True:
            logTraitement = "************BEGIN************\n"
            
            print (logTraitement)
#            if os.path.exists(lockFile)==True:
#                os.remove(lockFile)
            
            if os.path.exists(lockFile)==False:
                fichierlock=open(lockFile,'w')
                fichierlock.close() 
                
                self.campaign = "EDOUARD DENIS"
                self.lastcampaign = "0056"
                self.table = "[PROD_EDOUARD].[dbo].[vw_edouarddenis]"
                self.table_prod = "[DB_PROGRAMME].[dbo].[ODcallsReto]"
                
                self.renamed = ""

                self.currentDir = "/home/iam/PROD/BANDE_AUDIO/EDOUARD_DENIS"
                self.dir_temp= self.currentDir + "/TEMP/" 
                self.dir_save = self.currentDir + "/SAVE/" 
                self.dir_zip = self.currentDir + "/UNZIP/"
                self.dir_record = self.currentDir + "/RECORD/"
                self.dir_backup = self.currentDir+"/FICHIERS LIVRES/" 
                self.dir_fichier_client = "/Donnees/EDOUARD_DENIS/"
                
                 
                
                
                #####exterieur####
                logTraitement+="Envoie Ftp\n"
                self.envoi_ftp()
                logTraitement+="Fin envoie Ftp\n"
            if os.path.exists(lockFile)==True:
                print ("true")
                os.remove(lockFile)
            else:
                print ("false")
            
            
            print ("Fin traitement")
            logTraitement+= "************Fin traitement************\n"
            logTraitement=logTraitement.encode("utf8")
            fichierlog.write(str(logTraitement))
            
        except Exception as inst:
            
            logTraitement = '*******************'+time.strftime("%Y-%m-%d")+'*******************'+'\n'
            logTraitement+=  'type ERREUR:'+str(type(inst))+'\n'
            logTraitement+=  'CONTENU:'+str(inst)+'\n'
            logTraitement=logTraitement.encode("utf8")
            fichierlog.write(str(logTraitement))
            fichierlog.close()
            if os.path.exists(lockFile)==True:
                os.remove(lockFile)
           
            
if __name__=="__main__":
    Traitement()        
                         
   
                            
    
