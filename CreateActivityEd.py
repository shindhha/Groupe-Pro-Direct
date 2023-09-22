#! /usr/bin/env python
#coding=utf-8

import os,sys,logging
import requests, json
from RaycnxDict import Raycnx
from datetime import date, timedelta,datetime

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
date_p = datetime.now()
daty = str(date.today())
#daty = '2019-11-13'
log_name = '//home//user1//programme_python//logs//CreateAcitivy_log_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("date lancement programme: " + str(daty))
def SendMaxManMail(Adresseko, passwordko, hostako,ekipako,mess):

    # set up the SMTP server
    logging.debug('Initialisation de l envoi de mail')
    s = smtplib.SMTP(host=hostako, port=587)
    s.starttls()
    s.login(Adresseko, passwordko)

    # For each contact, send the email:
    #for name, email in zip(names, emails):
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = mess

        # Prints out the message body for our sake
   # print(message)

        # setup the parameters of the message
    msg['From']=Adresseko
    msg['To']=ekipako
    msg['Subject']="REPORT EDOUARD DENIS UPDATE CRM non abouti"

        # add in the message body
    msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()


edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
theuRl = "https://prd-ed-projet.azurewebsites.net/api/Project/SetActivity" 
headers = {'apikey': "ED-FACTORY-PROJET*2020","content-type": "application/json"}

def findDIndiceCalledAt():

    QueryLoad = """select tb.indice as INDICE from [31_RA_EDOUARD_DENIS] tb
        inner join [c1_31_RA_EDOUARD_DENIS] c1 on c1.indice = tb.indice
        where  c1.status = 1 and c1.detail in (1,3,6,5) and is_sent_crm='done' and set_activity is null"""
    logging.info(QueryLoad)
    print (QueryLoad)
    IndiceFlag = edouarddenis.execute_crud(QueryLoad, typ='kk')
    return IndiceFlag



def findData2crm(indice):
    logging.info("Recherche des donnes pour l'indice : " +str(indice))
#     query1 = """
#     SELECT

#  factoryprojectid,


#     /* sujet */
#         CASE
#             WHEN
#                  c1.status = 1 and c1.detail = 1 then 'R1 ' + tb.nom + ' '+ tb.prenom
#             WHEN
#                 c1.status = 1 and   c1.detail = 3 then 'Rtel ' + tb.nom + ' ' + tb.prenom
#             WHEN
#                 c1.status = 1 and c1.detail = 6 then 'RVisio ' + tb.nom + ' ' + tb.prenom
#             WHEN
#                 c1.status = 1 and c1.detail = 5 then 'Appel suite envoi de Doc'
#             ELSE
#                 ''
#         END sujet,

#         '1' as direction,


#              /* dure */

#         CASE
#             WHEN
#                  c1.status = 1 and c1.detail in (1,6) then '60'
#             WHEN
#                 c1.status = 1 and   c1.detail = 3 then '30'
#             WHEN
#                 c1.status = 1 and   c1.detail = 5 then '15'
#             ELSE
#                 ''
#         END duree,

#         'false' as message,

#           /* typeactivite */
#      CASE
#             WHEN
#                  c1.status = 1 and c1.detail in(1,3,6) then 'appointment'
#             WHEN
#                 c1.status = 1 and c1.detail = 5 then 'phonecall'
#             ELSE
#                 ''
#         END typeactivite,

#         tb.commentaires_agent as commentaire,

#             /* date debut */
#         CASE
#             WHEN
#                  c1.status = 1 and c1.detail = 1 then replace(replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(MINUTE,0,convert(datetime, tb.heure_rdv)),8),':',''),'/',''),'-','')
#             WHEN
#                 c1.status = 1 and   c1.detail = 3 then replace(convert(varchar,tb.date_rdv,103),'-','')  + replace(replace(convert(nvarchar,dateadd(MINUTE,0,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
#             WHEN
#                 c1.status = 1 and c1.detail = 6 then  replace(convert(varchar,convert(date,tb.date_rdv,103),120),'-','')  + replace(replace(convert(nvarchar,dateadd(hh,0,convert(datetime, tb.heure_rdv)),8),':',''),'/','')
#             WHEN
#                 c1.status = 1 and c1.detail = 5 then   replace(convert(varchar,dateadd(dd,2,convert(date,c1.date)),120),'-','')  + replace(convert(nvarchar,dateadd(MINUTE,0,convert(time,substring(c1.heure,0,3)+ ':' + substring(c1.heure,3,6))),8),':','') --
#             ELSE
#                 ''
#         END datedebut,


#             /* date fin */
#         CASE
#             WHEN
#                  c1.status = 1 and c1.detail = 1 then replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(hh,1,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
#             WHEN
#                 c1.status = 1 and   c1.detail = 3 then replace(convert(varchar,tb.date_rdv,103),'-','')  + replace(replace(convert(nvarchar,dateadd(MINUTE,30,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
#             WHEN
#                 c1.status = 1 and c1.detail = 6 then  replace(replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(hh,1,convert(datetime, tb.heure_rdv)),8),':',''),'/',''),'-','')
#             WHEN
#                 c1.status = 1 and c1.detail = 5 then   replace(convert(varchar,dateadd(dd,2,convert(date,c1.date)),120),'-','')  + replace(convert(nvarchar,dateadd(MINUTE,15,convert(time,substring(c1.heure,0,3)+ ':' + substring(c1.heure,3,6))),8),':','')
# --
#             ELSE
#                 ''
#         END datefin ,

#         /* typerdv */
#         CASE
#             WHEN
#                  c1.status = 1 and c1.detail = 1 then 'R1'
#             WHEN
#                 c1.status = 1 and   c1.detail = 3 then 'Rtel'
#             WHEN
#                 c1.status = 1 and c1.detail = 6 then 'RVisio'
#             WHEN
#                 c1.status = 1 and c1.detail = 5 then 'Rdoc'
#             ELSE
#                 ''
#         END typerdv,

#         case when co.email is null then 'call-center@edouarddenis.fr' else co.email end as commercial

#     from [31_RA_EDOUARD_DENIS] tb
#     inner join [c1_31_RA_EDOUARD_DENIS] c1 on tb.indice = c1.indice
#     left join oe_commerciaux co on co.id = tb.id_commercial
#     where tb.indice ={}""".format(indice)

    # Correction Thierry ------------------------------------------------------
    query1 = """
    SELECT

 factoryprojectid,


    /* sujet */
        CASE
            WHEN
                 c1.status = 1 and c1.detail = 1 then 'R1 ' + tb.nom + ' '+ tb.prenom
            WHEN
                c1.status = 1 and   c1.detail = 3 then 'Rtel ' + tb.nom + ' ' + tb.prenom
            WHEN
                c1.status = 1 and c1.detail = 6 then 'RVisio ' + tb.nom + ' ' + tb.prenom
            WHEN
                c1.status = 1 and c1.detail = 5 then 'Appel suite envoi de Doc'
            ELSE
                ''
        END sujet,

        '1' as direction,


             /* dure */

        CASE
            WHEN
                 c1.status = 1 and c1.detail in (1,6) then '60'
            WHEN
                c1.status = 1 and   c1.detail = 3 then '30'
            WHEN
                c1.status = 1 and   c1.detail = 5 then '15'
            ELSE
                ''
        END duree,

        'false' as message,

          /* typeactivite */
     CASE
            WHEN
                 c1.status = 1 and c1.detail in(1,3,6) then 'appointment'
            WHEN
                c1.status = 1 and c1.detail = 5 then 'phonecall'
            ELSE
                ''
        END typeactivite,

        tb.commentaires_agent as commentaire,

            /* date debut */
        CASE
            WHEN
                 c1.status = 1 and c1.detail = 1 then replace(replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(MINUTE,0,convert(datetime, tb.heure_rdv)),8),':',''),'/',''),'-','')
            WHEN
                c1.status = 1 and   c1.detail = 3 then replace(convert(varchar,tb.date_rdv,103),'-','')  + replace(replace(convert(nvarchar,dateadd(MINUTE,0,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
            WHEN
                c1.status = 1 and c1.detail = 6 then  replace(convert(varchar,convert(date,tb.date_rdv,103),120),'-','')  + replace(replace(convert(nvarchar,dateadd(hh,0,convert(datetime, tb.heure_rdv)),8),':',''),'/','')
            WHEN
                c1.status = 1 and c1.detail = 5 then   replace(convert(varchar,dateadd(dd,2,convert(date,c1.date)),120),'-','')  + replace(convert(nvarchar,dateadd(MINUTE,0,convert(time,substring(c1.heure,0,3)+ ':' + substring(c1.heure,3,6))),8),':','') --
            ELSE
                ''
        END datedebut,


            /* date fin */
        CASE
            WHEN
                 c1.status = 1 and c1.detail = 1 then replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(hh,1,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
            WHEN
                c1.status = 1 and   c1.detail = 3 then replace(convert(varchar,tb.date_rdv,103),'-','')  + replace(replace(convert(nvarchar,dateadd(MINUTE,30,convert(datetime, tb.heure_rdv)),8),'-',''),':','')
            WHEN
                c1.status = 1 and c1.detail = 6 then  replace(replace(replace(convert(varchar,convert(date,tb.date_rdv,103),120) + convert(nvarchar,dateadd(hh,1,convert(datetime, tb.heure_rdv)),8),':',''),'/',''),'-','')
            WHEN
                c1.status = 1 and c1.detail = 5 then   replace(convert(varchar,dateadd(dd,2,convert(date,c1.date)),120),'-','')  + replace(convert(nvarchar,dateadd(MINUTE,15,convert(time,substring(c1.heure,0,3)+ ':' + substring(c1.heure,3,6))),8),':','')
--
            ELSE
                ''
        END datefin ,

        /* typerdv */
        CASE
            WHEN
                 c1.status = 1 and c1.detail = 1 then 'R1'
            WHEN
                c1.status = 1 and   c1.detail = 3 then 'Rtel'
            WHEN
                c1.status = 1 and c1.detail = 6 then 'RVisio'
            WHEN
                c1.status = 1 and c1.detail = 5 then 'Rdoc'
            ELSE
                ''
        END typerdv,

        case when co.email is null then 'call-center@edouarddenis.fr' else co.email end as commercial

    from [31_RA_EDOUARD_DENIS] tb
    inner join [c1_31_RA_EDOUARD_DENIS] c1 on tb.indice = c1.indice
    left join oe_commerciaux co on co.id = tb.id_commercial
    where tb.indice ={}""".format(indice)
    # Fin correction

    print(query1)
    #sys.exit()
    logging.info("requette lancer:\n: " + query1)
    data = edouarddenis.execute_crud(query1, typ='kk')
    print (data[0])
    logging.info("contenu retourne")
    logging.info(data[0])
    #sys.exit()
    return data[0]

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
def updategOk(indice):
    qry = "UPDATE [31_RA_EDOUARD_DENIS] set set_activity ='fait', setactivity_done_at = convert(varchar,getDate(),120) where indice = {}".format(indice)
    if edouarddenis.execute_crud(qry):
        print ("flager with success")
        #sys.exit()

if connecter_site():
    print ("init service web")
    logging.info("************************** debut programme  at "+  str(date_p) +" ***********************")
    for el in findDIndiceCalledAt():
        indigo = str(el.get("INDICE"))
        logging.info("************************************ debut traitement pour l'indice : "  + str(indigo) + "********************************")
        trouve =findData2crm(indigo)
        if len(trouve) > 0 :
            factoryprojectid =  trouve.get("factoryprojectid")
            logging.info("************************* creat activity for factorypprojectid : " + str(factoryprojectid) + " ****************************")
            dataretr = json.dumps(trouve)
            logging.info(dataretr)
            print (dataretr)
            #sys.exit()
            retourta =requests.post(theuRl,data = dataretr, headers=headers).json() 
            logging.info("retour crm : " + str(retourta))
            print(retourta)
            error = retourta.get('error')
            messageR = retourta.get('message','tsymisy')
            isErrorInMessage = 'error' not in messageR.split(' ')
            logging.info("Message trouve dans le retour CRM: " + str(messageR) + " isErrorInMessage :" + str(isErrorInMessage) )
            print("Message trouve dans le retour CRM: " + str(messageR) + " isErrorInMessage :" + str(isErrorInMessage))
            #codeError = error.get('erCode')
            #message = error.get('erMessage')
            
            if (error is None or error =='' or isErrorInMessage):
                 print('creation activité ok')
                 logging.info("creation activité ok pour l'indice : " + str(indigo))
                 updategOk(indigo)
            else:
                logging.info("creation activite non abouti")
        else:
            logging.info("no data find pour l'indice " + str(indigo))
        continue
    edouarddenis.closeo()
