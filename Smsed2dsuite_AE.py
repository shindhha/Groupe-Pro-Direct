#! /usr/bin/env python3.7
#coding=utf-8
import os,sys, logging
import requests
import json
from Raycnx import Raycnx
from datetime import date, timedelta, datetime
EdouardSms = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
daty = str(date.today())
print (daty)
from time import strftime
lancementpgr = str(datetime.now()).split('.')[0]
print (lancementpgr)

log_name = '//home//user1//programme_python//logs//send_sms_edouard_ae_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("date lancement programme: " + str(daty))

queryprospet = """
select ed.indice,
case when salutation is null then 'Monsieur/Madame' else salutation end salutation,
case when ed.nom is null then '' else ed.nom end as nom,
CASE WHEN (case when tel_fixe is null or tel_fixe =''
      then
       case when tel_mobile is null or tel_mobile ='' then tel_professionnel else tel_mobile end
    else tel_fixe end )='' then num_appelant else 
     (case when tel_fixe is null or tel_fixe =''
      then
       case when tel_mobile is null or tel_mobile ='' then tel_professionnel else tel_mobile end
    else tel_fixe end )
     
      end telprospet,
ed.date_rdv, ed.heure_rdv,
case when co.telephone1 is null or co.telephone1 ='' then co.telephone2 else co.telephone1 end tel_com,
case when li.ville is null then '' else li.ville end + ' ' + case when li.cp is null then '' else li.cp end +' '+ case when li.adresse is null then '' else li.adresse end + ' ' 
+ case when  li.complement is null then '' else li.complement end as lieu_rdv   
from [31_EA_EDOUARD_DENIS] ed
left join oe_commerciaux co on co.id = ed.id_commercial
left join oe_lieu_rdv li on li.id_lieu = ed.id_lieu_rdv
where ed.is_sms ='sms' and ed.is_sms_sent is null and ed.set_activity='fait' and ed.date >='20200526'
"""
def findDataOk(Qry):
  data =[]  
  try:    
    data = EdouardSms.execute_crud(Qry,typ="kk")
    return data
  except Exception as e:
    print (e)      
    return 0

def connecter_site(): 
  try:    
    dict_tomatika = EdouardSms.connecting()    
    return True
  except:
    id_erreur="connection a la base"
    return False
def flageoGlasa(indice,message):
  qry = " UPDATE [31_EA_EDOUARD_DENIS] set is_sms_sent ='{}',send_sms_at = convert(varchar, getDate(),120) WHERE indice = {} ".format(message,indice)
  #print (qry)
  if EdouardSms.execute_crud(qry):
    logging.info('sms sent')

def flagSmsProspect(indice, etat):
  qry = " UPDATE [31_EA_EDOUARD_DENIS] set is_sms_sent ='done', send_sms_at=convert(varchar, getDate(),120),etat_sms_prospect='{}' WHERE indice = {} ".format(etat,indice)
     #print (qry)
  if EdouardSms.execute_crud(qry):
    logging.info('update flagSmsProspect ok')
    return 0
  logging.info('probleme update flagSmsProspect')
  return 0

def flagSmsCommerciale(indice, etat):
  qry = " UPDATE [31_EA_EDOUARD_DENIS] set is_sms_sent ='done', send_sms_at=convert(varchar, getDate(),120),etat_sms_commercial='{}' WHERE indice = {} ".format(etat,indice)
     #print (qry)
  if EdouardSms.execute_crud(qry):
    logging.info('update flagSmsCommerciale ok')
    return 0
  logging.info('probleme update flagSmsCommerciale')
  return 0


def sendSmsCommercial(indice):
    qInfocom = """select case when salutation is null then 'Monsieur/Madame' else salutation end salutation, case when tb.nom is null then '' else tb.nom end nom,
    case when tb.prenom is null then '' else tb.prenom end prenom, date_rdv,
    heure_rdv, tel_mobile +' - '+ tel_fixe + ' - ' + tel_professionnel as tel_prospet, 
    case when com.telephone1 is null or com.telephone1 ='' then com.telephone2 else com.telephone1 end as tel_commercial
    from  [31_EA_EDOUARD_DENIS] tb
    left join oe_commerciaux com on com.id = ISNULL(case when tb.id_commercial='' then null else tb.id_commercial end,0)
    where indice ={}""".format(indice)
    
    #logging.info("requette lancer:\n: " + query1)
    data = EdouardSms.execute_crud(qInfocom, typ='kk')
    
    #logging.info("contenu retourne")
    #logging.info(data[0])    
    param = (data[0])
    return sendCom(param[0],param[1],param[2],param[3],param[4],param[5],param[6])

def sendCom(salutation, nom, prenom, date_rdv,heure_rdv,tel_prospect,telcom):
    message = "Vous avez un nouveau RDV avec {} {} {} le {} à {} . Joignable au {}".format(salutation, nom, prenom,date_rdv, heure_rdv,tel_prospect)
    pistago ={
      'action':'send_sms',
      'auth_email':'dsi.france@groupe-prodirect.com',
      'auth_password':'**Api@Password',
      'from':'E.Denis',
      'to':'+33'+ str(telcom).replace(' ','')[-9:],
      'text':message
    }
    logging.info(pistago)
    print(pistago)
    responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
    logging.info(responsol_)
    return responsol_.json()

def sendSmsprospect(salutation, nom,tel_com, date_rdv, heure_rdv, lieu_rdv,tel_prospet):
  message="""{} {}, commercial(N° {}) vous recevra le {} à {} au {}. Votre conseiller Edouard Denis""".format(salutation, nom, tel_com, date_rdv, heure_rdv, lieu_rdv)
  pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'E.Denis',
  'to':'+33'+ str(tel_prospet).replace(' ','')[-9:],
  'text':message
  }
  print (pistago)
  responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
  logging.info(responsol_)
  return responsol_.json()
  #print (pistago)


if connecter_site():
  logging.info("debut et lancement du programme a : " + str(lancementpgr))
  data_ = findDataOk(queryprospet)
  logging.info("rechercher des donnes")
  logging.info(data_)
  print(data_)
  #sys.exit()
  if len(data_) > 0:
    for ele in data_:
      indice = ele[0]
      comretour = sendSmsCommercial(indice)
      print (comretour)
      logging.info("########## RETOUR sendSmsCommercial ##########")
      logging.info(str(datetime.now()).split('.')[0])
      logging.info(comretour)
      logging.info("########## FIN sendSmsprospect #############")
      #sys.exit()
      retour = sendSmsprospect(ele[1],ele[2],ele[6],ele[4],ele[5],ele[7],ele[3])
      print(retour)
      logging.info("########## RETOUR sendSmsprospect ##########")
      logging.info(str(datetime.now()).split('.')[0])
      logging.info(retour)
      logging.info("########## FIN sendSmsprospect #############")
      if retour["message"] == "successful":
        print ("indice : " + str(indice) + " Sms envoyer ")
        logging.info("indice : " + str(indice) + " Sms envoyer ")
        flagSmsProspect(indice, 'ok')
        flageoGlasa(indice,'done')
      else:
        print ("indice : " + str(indice) + " Sms non envoyer ")
        logging.info("indice : " + str(indice) + " Sms non envoyer ") 
        flagSmsProspect(indice, 'ko')
        flageoGlasa(indice,'ko')
      if comretour["message"] == "successful":
        print("indice:" + str(indice) + " sms envoyer au commerciaux")
        logging.info("indice:" + str(indice) + " sms envoyer au commerciaux")
        flageoGlasa(indice,'done')
        flagSmsCommerciale(indice, 'ok')
      else:
        print("indice:" + str(indice) + " sms nom envoyer au commerciaux")
        logging.info("indice:" + str(indice) + " sms nom envoyer au commerciaux")
        flageoGlasa(indice,'ko')
        flagSmsCommerciale(indice, 'ko')
      
      #sys.exit()
  else:
    print ("auccun rendez-vous pour : " + daty)
    logging.info("aucun sms a envoyer le : " + str(lancementpgr))
  EdouardSms.closeo()


