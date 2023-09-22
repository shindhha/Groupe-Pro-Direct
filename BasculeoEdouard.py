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
filelog ='//home//user1//programme_python//logs//logbasculementED' + daty.replace('-','') + '.log'
logging.basicConfig(filename=filelog, level=logging.DEBUG)
logging.info("date lancement programme: " + str(date_p))
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
    msg['Subject']="REPORT EDOUARD DENIS BASCULEMENT non abouti"

        # add in the message body
    msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()


edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
theuRl = "http://ws-238.vivetic.com/BasculerEdouard/api/EdouardDenis" 
headers = {"content-type": "application/json"}

def findDIndiceCalledAt(daty_anio):

    QueryLoad = "SELECT INDICE FROM edouarddenis WHERE bascule ='bascule'"
    logging.info(QueryLoad)
    print (QueryLoad)
    IndiceFlag = edouarddenis.execute_crud(QueryLoad, typ='kk')
    return IndiceFlag



def findData2Toggle(indice):
    logging.info("Recherche des donnes pour l'indice : " +str(indice))
    query1 = """
    select code_postal, adresse, adresse2, ville, email, email2, prenom, nom, tel_mobile, tel_fixe, tel_professionnel,
    salutation, situation_logement, objectif_achat, date_acquisition, code_programme, projet_immo, commentaire, budget_max, horaire_rappel,
    utm_capaign, canal, utm_act, utm_source, utm_medium, factoryprojectid, imposition, date_naissance, profession, nom_formulaire, type_logement,
    surface_logement, taille_logement, budget_fourchette, code_lot, dept_rech, ville_rech, primo_accedant, rgpdin, rgpdout, type_bienED,
    nature_bien,indice as indice_debut,date_rdv,heure_rdv,id_commercial,id_lieu_rdv,bascule,revente,is_sms,flag_mail,drapp,programme_prodirect,
    programme_prodirect_val,raison_trna,raison_trna_val,'31_FORMULAIRE_ED' as camp_debut ,case when budget is null then '' Else budget End  as budget
    ,case when destination_achat is null then '' Else destination_achat End as destination_achat
    ,case when typo_formulaire is null then '' Else typo_formulaire End  as typo_formulaire from edouarddenis where indice = {}""".format(indice)
    logging.info("requette lancer:\n: " + query1)
    data = edouarddenis.execute_crud(query1, typ='kk')
    
    logging.info("contenu retourne")
    logging.info(data[0])    
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
def is_toggled(indice_):
    qery = "select count(*) trouve from [31_RA_EDOUARD_DENIS] where indice_debut = '{}'".format(indice_)
    print(qery)
    compte = edouarddenis.execute_crud(qery, typ='tt')
    logging.info(compte[0].get('trouve'))
    return compte[0].get('trouve')
def updateoGvita(indice):
    qk = "UPDATE edouarddenis SET bascule='done' where indice = {}".format(indice)
    print(qk)
    logging.info("mise à jour : " + str(qk))
    return edouarddenis.execute_crud(qk)
def recup_ligne(indice_):
    Qk = """
    select 
_commerciale,
admin_r,
admin_region,
adresse,
adresse2,
avoir_projet,
bascule,
budget_fourchette,
budget_max,
budgetm,
code_lot,
code_postal,
commentaires_agent,
date_naissance,
date_rdv,
daty,
dept_rech,
drapp,
email,
email2,
etage,
first_sale,
flag_mail,
heure_rdv,
horaire_rappel,
id_commercial,
id_lieu_rdv,
imposition,
is_sms,
is_sms_48_sent,
is_sms_sent,
is_toggle,
jsu_oe,
m2,
nature_bien,
nature_logement,
nom,
nom_formulaire,
objectif_ach,
objectif_achat,
ok_sms,
prenom,
primo_acc,
primo_accedant,
principale_investissement,
profession,
programme_prodirect,
projet_client,
projet_immo,
RAISON_TRNA,
revente,
Salutat,
salutation,
secteur_geo,
situation_log,
situation_logement,
taille_logement,
tel_fixe,
tel_mobile,
tel_professionnel,
type_bienED,
type_logemend,
ville,flag_crm, is_sent_crm,
ville_rech, case when budget is null then '' Else budget End  as budget
    ,case when destination_achat is null then '' Else destination_achat End as destination_achat
    ,case when typo_formulaire is null then '' Else typo_formulaire End  as typo_formulaire from edouarddenis where indice = {}""".format(indice_)
    #print(Qk)
    dataup = edouarddenis.execute_crud(Qk, typ="ttt")
    logging.info("data a updateder trouve: ")
    logging.info(dataup)
    updateoreto = {}
    for key, value in  dataup[0].items():
        if value and str(value).strip() !='' and str(value).lower() !='none' :
            updateoreto[key] = value
    print (updateoreto)
    logging.info(updateoreto)
    sqlUpdate = []
    sqlhead = " update [31_RA_EDOUARD_DENIS] set "
    for k, v in updateoreto.items():
        sqlUpdate.append(k + " = '" + str(v).replace("'","''").replace('"','') + "'")
    if len(sqlUpdate) > 0:
        sqlcomplet =  sqlhead + ', '.join(sqlUpdate) +' ' + 'where indice_debut =' + str(indice_)
        print(sqlcomplet)
        logging.info(sqlcomplet)
        return edouarddenis.execute_crud(sqlcomplet)
    else:
        print ('tout les colonne sont vide')
        logging.info('tout les colonne sont vide')
        return 0

    #edoaurddenis.execute(sqlcomplet)
    
    
def getStatusop1(indice):
    kata = "SELECT status,CONCAT('O',replace(convert(varchar(10),dateadd(d,1,date),120),'-',''),heure) as date_rappel from c1_edouarddenis where indice ={}".format(indice)
    data = edouarddenis.execute_crud(kata,typ='kk')[0]
    return data

if connecter_site():
    print ("init service web at " + str(date_p))
    for el in findDIndiceCalledAt(daty):
        indigo = str(el.get("INDICE"))
        
        trouve =findData2Toggle(indigo)
        if len(trouve) > 0 :        
            idpros =  trouve.get("indice_debut")
            #print(idpros)
            #sys.exit()
            
            
            if is_toggled(indigo):
                print("update it")
                if recup_ligne(indigo):
                    updateoGvita(indigo)
                    continue
                    
                else:
                    print("mise à jour ko pour l'indice" + str(indigo))
                    updateoGvita(indigo)
                #sys.exit()
            else:
                print("create it")
                #sys.exit()
                dataretr = json.dumps(trouve)
                logging.info(dataretr)
                retourta =requests.post(theuRl,data = dataretr, headers=headers).json()
                if retourta =="PhoneNumberError ":
                    print("erreur d'injection pour l'indiice " + str(indigo))
                    continue
                #sys.exit()
                if retourta.get('message') == "injection success" and retourta.get('error') =="":
                    datama = getStatusop1(indigo)
                    status = datama.get('status')
                    date_rappel = datama.get('date_rappel')
                    logging.info('status: ' + str(status) + ' date_rappel : ' + str(date_rappel))
                    if str(status) =="99":
                        print('tafiditra ato satria 99 ')
                        queryUpdate ="""
                       UPDATE [c1_31_RA_EDOUARD_DENIS]
                       SET PRIORITE = 0, DATE = ed.DATE, HEURE = ed.HEURE, VERSOP = ed.VERSOP, RAPPEL = '{}', TV = ed.TV, ID_TV = ed.ID_TV , STATUSGROUP = ed.STATUSGROUP,
                       STATUS = 95, LIB_STATUS = 'relance', DETAIL = 0,  LIB_DETAIL = '', DUREE = ed.DUREE, MIXUP = ed.MIXUP, NIVABS = 1
                       FROM [c1_31_RA_EDOUARD_DENIS] t
                        inner join [31_RA_EDOUARD_DENIS] ra on ra.indice = t.indice
                        inner join edouarddenis d on d.indice = ra.indice_debut
                        inner join [c1_EdouardDenis] ed on ed.indice = d.indice
                       where ra.indice_debut = '{}'
                        """.format(date_rappel,indigo)

                    else:
                        print ('nakato satria tsy 99')
                        queryUpdate = """
                    UPDATE [c1_31_RA_EDOUARD_DENIS]
                    SET PRIORITE = ed.PRIORITE, DATE = ed.DATE, HEURE = ed.HEURE, VERSOP = ed.VERSOP, RAPPEL = ed.RAPPEL, TV = ed.TV, ID_TV = ed.ID_TV , STATUSGROUP = ed.STATUSGROUP,
                    STATUS = ed.STATUS, LIB_STATUS = ed.LIB_STATUS, DETAIL = ed.DETAIL,  LIB_DETAIL = ed.LIB_DETAIL, DUREE = ed.DUREE, MIXUP = ed.MIXUP, NIVABS = 1
                    FROM [c1_31_RA_EDOUARD_DENIS] t
                    inner join [31_RA_EDOUARD_DENIS] ra on ra.indice = t.indice
                    inner join edouarddenis d on d.indice = ra.indice_debut
                    inner join [c1_EdouardDenis] ed on ed.indice = d.indice
                    where ra.indice_debut = '{}'
                    """.format(indigo)
                    print(queryUpdate)
                    logging.info("query update op2 :" + str(queryUpdate))
                    if edouarddenis.execute_crud(queryUpdate):
                        deleteGra = """update c1_edouarddenis set priorite =-10, versop = -1 where indice ={}; update edouarddenis set bascule = 'done' where indice ={}""".format(indigo,indigo)
                        if edouarddenis.execute_crud(deleteGra):
                            logging.info('basculement fait pour ' +str(indigo))
                            recup_ligne(indigo)
            #sys.exit() 
        else:
            logging.info("auccun data trouve pour l'indice " + str(indigo))
            #sys.exit()
    edouarddenis.closeo()