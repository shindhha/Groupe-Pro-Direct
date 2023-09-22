#! /usr/bin/env python
# -*- coding: utf8
import requests
import json
import datetime, sys, os,logging
from datetime import date, timedelta,datetime
from RaycnxDict import Raycnx
daty = str(date.today())
date_p= datetime.now()
print(date_p)
log_name = '//home//user1//programme_python//logs//acquitementRejet_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("********************************date lancement programme: " + str(date_p) + " ************************")
edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
urlAcquit = "https://prd-ed-projet.azurewebsites.net/api/Project/AcquitProject4CallCenter"
headersed = {'apikey': "ED-FACTORY-PROJET*2020",'Content-type': 'application/json'}
headers = {'Content-type': 'application/json'}
mineurl = "https://ws-238.vivetic.com/prod_v1_EdouardDenis/api/EdouardDenis"
concluscode = "DOUBLON SYSTEME"
def recupRejet():
    logging.info(" *** Recuperation des rejets *** ")
    query = "SELECT factoryprojectid FROM rejet_edouarddenis_crm WHERE flag_acquitement is null AND motif = 'REJET DOUBLONS'"
    logging.info(query)
    d = edouarddenis.execute_crud(query, typ='kk')
    logging.info(d)
    return d
    
def connecter_site(): 
  logging.info("connexion à la base de donnée")
  try:
    dict_tomatika = edouarddenis.connecting()
    logging.info("connexion réussi") 
    return True
  except:
    id_erreur="connection a la base"
    logging.debug("Erreur de connexion à la base")
    return False

def update_byidRejet (factoryprojectid,etat):
    logging.info("mise à jour flag_acquitement")
    sql = "UPDATE rejet_edouarddenis_crm set flag_acquitement = '{}' where factoryprojectid = '{}'".format(etat,factoryprojectid)
    logging.info(sql)
    edouarddenis.execute_crud(sql)
    
def acquiteproject (factoryid):
    indice = "R-"+factoryid
    logging.info("++++++++++++++++ lancement de l'acquitement pour le factoryprojectid = " + factoryid + " avec le callcenterprojectid ="  + indice+" +++++++++++++++")    
    acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":indice, "conclusioncode":concluscode }
    acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
    # THR20200708 : Ajout des infos in et out pour le WS
    logging.info(">>>>>")
    logging.info(acquiteb)
    logging.info(acquite)
    logging.info("<<<<<")
    # THR20200708 : Fin ajout infos
    error = acquite.get('error')
    codeError = error.get('erCode')
    Message = error.get('erMessage')
    if (Message is None and codeError is None):
        update_byidRejet(factoryid,'OK')
        print ("acquitement rejet ok ")
        logging.info("acquitement rejet ok pour la  factoryprojectid: " + factoryid)
    else:
        update_byidRejet(factoryid,'KO')
        print("acquitement rejet non abouti")
        logging.info("acquitement rejet n'est pas reussi")
        print ('contenu non traitable')
        logging.info(str(codeError) +': ' + str(Message))
        logging.info("********************contenu non traitable chez nous suivant le cahier de charge*********")
    logging.info("++++++++++++++ Fin de l'acquitement pour le factoryprojectid = " + factoryid + " avec le callcenterprojectid = "  + indice+" +++++++++++")    
if connecter_site():
    data = recupRejet()
    for e in data:
        f = e.get('factoryprojectid')
        print(f)
        #sys.exit()
        acquiteproject(f)
        #sys.exit()
    edouarddenis.closeo()
