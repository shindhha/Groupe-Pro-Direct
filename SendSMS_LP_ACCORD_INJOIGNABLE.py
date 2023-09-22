#! /usr/bin/env python
#coding=utf-8
import os,sys,logging
import requests, json
from datetime import date, timedelta,datetime
import pymssql
import smtplib



daty = date.today()


conn = pymssql.connect('5.196.127.163', 'read_write', '0wY!3M8cQ#Kw', 'VIVETIC_PROD')
cursor = conn.cursor(as_dict=True)

date_p = datetime.now()
filenamelog ="//var//log_iscc//SMS_LP_ACCORD_INJOIGNABLE_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("****************************date lancement programme: " + str(date_p)+" ******************************")

def flageoGlasa(indice):
  qry = " UPDATE [LP_PROMOTION_CONFIRMATION_RDV] set Etat_sms ='done' , DATY_SMS='{}' WHERE indice = {} ".format(daty,indice)
  #print (qry)
  cursor.execute(qry)
  conn.commit()
  logging.info('sms sent')

def flageoGtsylasa(indice):
  qry = " UPDATE [LP_PROMOTION_CONFIRMATION_RDV] set Etat_sms ='ko' , DATY_SMS='{}' WHERE indice = {} ".format(daty, indice)
  cursor.execute(qry)
  conn.commit()
  logging.info('sms not sent')

def sendSomeso_akaoro(tel,comaka,date,heure):
    message = """Bonjour, 

Suite à notre conversation de ce jour, nous vous confirmons votre rendez-vous avec Madame/Monsieur {}, le {} à {}.

Nous restons à votre disposition pour tout renseignement au 0805 804 803. 

Cordialement ,
L’équipe LP PROMOTION""".format(comaka,date,heure)
    pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'lppromotion',
  'to':'+33'+ tel.replace(' ','')[-9:],
  'text':message
  }
    logging.info(pistago)
    print("Envoi en cours...")
    responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
    logging.info(responsol_)
    return responsol_.json()

def sendSomeso_injoinaka(tel,comaka,date,heure):
    message = """Bonjour, 

Nous vous confirmons votre rendez-vous avec Madame/Monsieur  {}, le {} à {}.

Nous restons à votre disposition pour tout renseignement au 0805 804 803. 

Cordialement ,
L’équipe LP PROMOTION""".format(comaka,date,heure)
    pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'lppromotion',
  'to':'+33'+ tel.replace(' ','')[-9:],
  'text':message
  }
    logging.info(pistago)
    print("Envoi en cours...")
    responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
    logging.info(responsol_)
    return responsol_.json()    

REQUEST = "SELECT indice , telephone , NOM_COMMERCIAL, DATE_RDV, HEURE_RDV , SMS,DATE_NOUVEAU_RDV, HEURE_NOUVEAU_RDV FROM LP_PROMOTION_CONFIRMATION_RDV WHere (Etat_sms is NULL Or Etat_sms ='') and SMS in ('MODIFICATION_SMS','ACCORD_SMS','INJOIGNABLE_SMS')"
cursor.execute(REQUEST)
data = cursor.fetchall()

if len(data) > 0 :
  print(data[0])
  indice = data[0]["indice"]
  tel = data[0]["telephone"]
  com = data[0]["NOM_COMMERCIAL"]
  Date = data[0]["DATE_RDV"]
  Ora = data[0]["HEURE_RDV"]
  print (data[0]["SMS"])
  if data[0]["SMS"] == "ACCORD_SMS" :

    avereno = sendSomeso_akaoro(tel,com,Date,Ora)
    if avereno["message"] == "successful" :
      flageoGlasa(indice)
      print("lasa")
    else :
      flageoGtsylasa(indice)
      print("Tsy lasa")
  elif data[0]["SMS"] == "INJOIGNABLE_SMS" :
    avereno = sendSomeso_injoinaka(tel,com,Date,Ora)
    if avereno["message"] == "successful" :
      flageoGlasa(indice)
      print("lasa")
    else :
      flageoGtsylasa(indice)
      print("Tsy lasa")
  elif data[0]["SMS"] == "MODIFICATION_SMS" :	
    Date = data[0]["DATE_NOUVEAU_RDV"]
    Ora = data[0]["HEURE_NOUVEAU_RDV"]
    avereno = sendSomeso_akaoro(tel,com,Date,Ora)
    if avereno["message"] == "successful" :
      flageoGlasa(indice)
      print("lasa")
    else :
      flageoGtsylasa(indice)
      print("Tsy lasa")
else :
  print("Pas de traitement")
conn.close()