#! /usr/bin/env python3.7
#coding=utf-8
import os,sys,logging
import requests
import json
from Raycnx import Raycnx
from datetime import date, timedelta,datetime
daty =str(date.today())
print(daty)
filenamelog ="//home//user1//programme_python//logs//sendSms48h_AE_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("*************************************************** debut log *****************************")
logging.info("date lancement programme: " + str(daty))

EdouardSms = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
demain = date.today() + timedelta(2)
date_rdv = str(demain.strftime("%d/%m/%Y"))
lancementpgr = str(datetime.now()).split('.')[0]
print (lancementpgr)
#date_rdv = "28/05/2020"
print (date_rdv)
queryprospet = """
select ed.indice,
 CASE WHEN (case when tel_fixe is null or tel_fixe =''
      then
       case when tel_mobile is null or tel_mobile ='' then tel_professionnel else tel_mobile end
    else tel_fixe end )='' then num_appelant else
     (case when tel_fixe is null or tel_fixe =''
      then
       case when tel_mobile is null or tel_mobile ='' then tel_professionnel else tel_mobile end
    else tel_fixe end )

      end telprospet,
'Nom: ' + case when civilite is null then '' else civilite end  +' '+ case when co.nom is null then '' else co.nom end +' '+ case when co.prenom is null then '' else co.prenom end + 
' email: ' + case when co.email is null then '' else co.email end + ' tel: ' + case when co.telephone1 is null or co.telephone1 ='' then co.telephone2 else co.telephone1 end tel_com

from [31_EA_EDOUARD_DENIS] ed
inner join oe_commerciaux co on co.id = ed.id_commercial
where  ed.QUALIF_CODE ='1' and ed.QUALIF_DETAIL in ('1','3') and ed.is_sms_48_sent is null and date_rdv ='{}'

""".format(date_rdv)
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
  qry = " UPDATE [31_EA_EDOUARD_DENIS] set is_sms_48_sent ='{}', sms_48h_at=convert(varchar,getDate(),120) WHERE indice = {} ".format(message,indice)
  print (qry)
  if EdouardSms.execute_crud(qry):
    print('sms sent')

def sendSmsprospect(telprospet, infocom):
  message="""Vous avez prochainement rendez-vous avec votre conseiller Edouard Denis. Enregistrez sa fiche contact pour le joindre à tout moment. Merci de votre confiance. » Joint : la fiche contact du Commercial : {} """.format(infocom)  
  pistago ={
  'action':'send_sms',
  'auth_email':'dsi.france@groupe-prodirect.com',
  'auth_password':'**Api@Password',
  'from':'E.Denis',
  'to':'+33' + telprospet.replace(' ','')[-9:],
  'text':message
  }  
  print (pistago)
  responsol_ = requests.get("https://www.manivox.com/api_v2/json_api.php",params=pistago)
  return responsol_.json()
  #print (pistago)


if connecter_site():
  logging.info("lancement du programme at : " +str(lancementpgr))
  data_ = findDataOk(queryprospet)
  if len(data_) > 0:  
    for ele in data_:
      indice = ele[0]
       
      retour = sendSmsprospect(ele[1],ele[2])
      print(retour)  
      if retour["message"] == "successful":
        logging.info("indice : " + str(indice) + " Sms envoyer ") 
        print ("indice : " + str(indice) + " Sms envoyer ")
        flageoGlasa(indice,'done')
        #sys.exit()
      else:
        logging.info("Sms non envoyé pour l'indice : "+str(indice)+ ' cause : ' + retour["error"])
        print ("Sms non envoyé pour l'indice : "+str(indice)+ ' cause : ' + retour["error"])
        flageoGlasa(indice,'ko')
        #continue
  else:
    print ("auccun rendez-vous pour : " + str(demain))
  EdouardSms.closeo()


