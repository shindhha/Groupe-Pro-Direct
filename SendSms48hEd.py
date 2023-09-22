#! /usr/bin/env python3.7
#coding=utf-8
import os,sys
import requests,logging
import json
from Raycnx import Raycnx
from datetime import date, timedelta,datetime
daty = str(date.today())
EdouardSms = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
log_name = '//home//user1//programme_python//logs//SendSms_ED_48h_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
demain = date.today() + timedelta(2)
date_rdv = str(demain.strftime("%d/%m/%Y"))
date_p = datetime.now()
#date_rdv ="27/05/2020"
print (date_rdv)
logging.info('date RDV trouve avant 48h ' + str(date_rdv))
queryprospet = """
select ed.indice,
 case when tel_fixe is null or tel_fixe ='' 
      then 
       case when tel_mobile is null or tel_mobile ='' then tel_professionnel else tel_mobile end
    else tel_fixe end  telprospet,
'Nom: ' + civilite +' '+ co.nom +' '+co.prenom + ' email: ' + co.email + ' tel: ' + case when co.telephone1 is null or co.telephone1 ='' then co.telephone2 else co.telephone1 end tel_com
from [31_RA_EDOUARD_DENIS] ed
inner join oe_commerciaux co on co.id = ed.id_commercial
where ed.is_sms ='sms' and ed.is_sms_sent is not null and ed.is_sms_48_sent is null and date_rdv = '{}'

""".format(date_rdv)
def findDataOk(Qry):
  data =[]  
  try:    
    data = EdouardSms.execute_crud(Qry,typ="kk")
    #logging.info('donne trouve :' + data)
    return data
  except Exception as e:
    print (e)      
    return 0

def connecter_site(): 
  try:    
    dict_tomatika = EdouardSms.connecting()
    logging.info('connextion site ok')
    return True
  except:
    id_erreur="connection a la base"
    logging.info('connextion site ko')
    return False
def flageoGlasa(indice):
  qry = " UPDATE [31_RA_EDOUARD_DENIS] set is_sms_48_sent ='done',sms_48h_at = convert(varchar, getDate(),120) WHERE indice = {} ".format(indice)
  print (qry)
  logging.info('mise à jour indice : ' + str(indice) + 'ok')
  if EdouardSms.execute_crud(qry):
    print('sms sent')

def sendSmsprospect(telprospet, infocom):
  message="""Vous avez prochainement rendez-vous avec votre conseiller Edouard Denis. Enregistrez sa fiche contact pour le joindre à tout moment. Merci de votre confiance. » Joint : la fiche contact du Commercial : {} """.format(infocom)  
  pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'E.Denis',
  'to':'+33' + telprospet[-9:],
  'text':message
  }  
  responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
  return responsol_.json()
  #print (pistago)


if connecter_site():
  logging.info("***********************lancement de programme at : " + str(date_p) + " *****************")
  data_ = findDataOk(queryprospet)
  print(data_)
  print("nombre d'indice trouver : " + str(len(data_)))
  #sys.exit()
  if len(data_) > 0:  
    for ele in data_:
      indice = ele[0]
      #sys.exit() 
      retour = sendSmsprospect(ele[1],ele[2])
      print(retour)
      logging.info(retour)  
      if retour["message"] == "successful":    
        print ("indice : " + str(indice) + " Sms envoyer ")
        logging.info("indice : " + str(indice) + " Sms envoyer ")
        flageoGlasa(indice)
      else:
        print ("Sms non envoyé pour l'indice : "+str(indice)+ ' cause : ' + retour["error"])
        logging.info("Sms non envoyé pour l'indice : "+str(indice)+ ' cause : ' + retour["error"])
        flageoGlasa(indice)
        #continue
      #sys.exit()
  else:
    print ("auccun rendez-vous pour : " + str(demain))
  EdouardSms.closeo()

