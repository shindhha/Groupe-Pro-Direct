#! /usr/bin/env python
#coding=utf-8

import os,sys,logging
import requests, json
from RaycnxDict import Raycnx
from datetime import date, timedelta,datetime
import pandas as pd
from email.utils import COMMASPACE
import smtplib
import ntpath
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.utils import make_msgid
from email.utils import formatdate
daty = str(date.today())
#daty = '2019-11-13'
filenamelog ="miseajourcrmedLog_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("date lancement programme: " + str(daty))


edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')



def recup_rejet():
    qry = "SELECT id_rejet,Date_rejet as Date, factoryprojectid as [Factory ID], Motif FROM rejet_edouarddenis_crm WHERE flag_envoie is null"
    print(qry)
    data = edouarddenis.execute_crud(qry, typ='kk')
    print(data)
    return data
def export_excel(dicto):
    df = pd.DataFrame.from_dict(dicto)
    #df = (df.T)
    print (df)
    logging.info(df)
    excelname = "/home/user1/programme_python/Export_rejet_ED/Export_rejet_le_" + daty+'.xlsx'
    df.to_excel(excelname,index=False)
    return excelname
def updateDicto(dicto):
    for  el in dicto:
        idrejet = el.get('id_rejet')
        query = "update rejet_edouarddenis_crm set flag_envoie ='sent' where id_rejet = {}".format(idrejet)
        if edouarddenis.execute_crud(query):
            logging.info('update rejet : ' +str(idrejet))
            continue
        continue

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


def send_mailHelios(send_to,message,files=None):    
    server="mx1.vivetic.mg"
    isTls=True
    send_from ='fabrice.razanajatovo@vivetic.mg'
    passwordikta ='SHijei1y'
    subject ="REJET DOUBLONS SYSTEM DU : " + str(daty)
    logging.info("Preparation de l'envoi mail :")
    logging.info("Sender : " + str(send_from))
    logging.info("subject : " + str(subject))
    logging.info("Date: " + str(daty))
    logging.info("Copie caché : iscc@vivetic.mg")    
    msg = MIMEMultipart('related')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    bcc =["iscc@vivetic.mg"]
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message,'html'))    
    for f in files or []:
        file_ = ntpath.basename(f)
        print(file_)
        #sys.exit()
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                f
            )
        
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(file_)
        msg.attach(part)
    username =send_from
    try:
      logging.info("Send mail ...")
      smtp = smtplib.SMTP(server,587)
      smtp.ehlo()
      #if isTls:
      smtp.starttls()
      smtp.ehlo()
      smtp.login(username,passwordikta)
      print ("send mail for " + str(send_to))
      smtp.sendmail(send_from, send_to+bcc, msg.as_string())
      smtp.close()
      logging.info("mail envoyé avec succès")
      return True
    except Exception as e:
      logging.info("mail not sent")
      logging.info(e)
      return False

if connecter_site():
    fileattache = []
    trouver = recup_rejet()
    fileattache.append(export_excel(trouver))
    message = """
    <b>Bonjour</b><br>
    <div>
        ci-joint en attaché un fichier contenant la liste des rejets systèmes du jour {}<br>
        <b>cordialement</b>,<br>
        <b>iscc</b>
    </div>
    """.format(daty)
    send_to = ["f.decker@edouarddenis.fr"] #f.decker@edouarddenis.fr
    #sys.exit()
    if send_mailHelios(send_to,message,files=fileattache):
        #updateko g lasa:
        updateDicto(trouver)
        print('fait')
    edouarddenis.closeo()
    
