#! /usr/bin/env python3.7
#coding=utf-8
import os,sys, logging
import requests
import json
from Raycnx import Raycnx
from datetime import date, timedelta, datetime
EdouardSms = Raycnx(host='51.255.68.172', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
daty = str(date.today())
date_p = datetime.now()
print (daty)

log_name = '//var//log_iscc//send_sms_formulaire_log_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("date lancement programme: " + str(daty))

queraka = """SELECT tb.indice , c1.TEL FROM edouarddenis tb
  INNER JOIN c1_edouarddenis c1 ON tb.indice = c1.indice
  WHERE status in (90,92,93) and Flag_sms_injoignable = 'sms'
  AND TEL <>'' AND TEL is not NULL
  AND Date >='20220105'
"""

def connecter_site(): 
  try:    
    dict_tomatika = EdouardSms.connecting()    
    return True
  except:
    id_erreur="connection a la base"
    return False
def flageoGlasa(indice):
  qry = " UPDATE [edouarddenis] set Flag_sms_injoignable ='done' WHERE indice = {} ".format(indice)
  #print (qry)
  if EdouardSms.execute_crud(qry):
    logging.info('sms sent')
def flageoGtsylasa(indice):
  qry = " UPDATE [edouarddenis] set Flag_sms_injoignable ='ko' WHERE indice = {} ".format(indice)
  #print (qry)
  if EdouardSms.execute_crud(qry):
    logging.info('sms not sent')

def sendSomeso(tel):
    message = "Edouard DENIS immobilier bonjour, nous avons tenté de vous joindre. N’hésitez pas à nous recontacter au 0800950750 de 9h à 19h du lundi au samedi"
    pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'E.Denis',
  'to':'+33'+ tel.replace(' ','')[-9:],
  'text':message
  }
    logging.info(pistago)
    print(pistago)
    responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
    logging.info(responsol_)
    return responsol_.json()

if connecter_site():
  logging.info("********************** lancement du programme at : " + str(date_p) + "**********************")
  try:
    data_ = EdouardSms.execute_crud(queraka,typ="kk")
    print(data_)
  except Exception as e:
    print (e)    
  #sys.exit()
  try:
    print(len(data_))
  except Exception as e:
    print("pas d'enregistrement trouve")
    sys.exit()
  if len(data_) > 0:
    for ele in data_:
      indice = ele[0]
      TEL = ele[1]
      retour = sendSomeso(TEL)
      print (retour)
      #sys.exit()
      if retour["message"] == "successful":
        print ("indice : " + str(indice) + " ,Sms envoyé ")
        logging.info("indice : " + str(indice) + " ,Sms envoyé ")
        flageoGlasa(indice)
      else:
        print("indice: " + str(indice) + " ,Sms non envoyé")
        logging.info("indice: " + str(indice) + " ,Sms non envoyé")
        flageoGtsylasa(indice)

  else:
    print ("aucun SMS à envoyer: " + daty)
  EdouardSms.closeo()