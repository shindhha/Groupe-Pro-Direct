
#! /usr/bin/env python coding=utf-8


import os,sys,logging, uuid
import requests, json
from RaycnxDict import Raycnx
from datetime import date, timedelta,datetime

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import glob

lancementpgr = str(datetime.now()).split('.')[0]
print (lancementpgr)

daty = str(date.today())
print (daty)

indicesSpecifiques = []
if len(sys.argv) > 1:
    indicesSpecifiques = sys.argv[1].split(',')

#daty = '2020-07-08'
filenamelog ="//var//log_iscc//sendEdouard2crm_AE_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("*************************************************** debut log *****************************")
logging.info("date lancement programme: " + str(lancementpgr))
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
setActivityurl = "https://prd-ed-projet.azurewebsites.net/api/Project/SetActivity"
urlprod = "https://prd-ed-projet.azurewebsites.net/api/Project/CreateOrUpdateProject4CallCenter" 
prod = {'apikey': "ED-FACTORY-PROJET*2020", 'content-type': 'application/json'}



preprod = {'apikey':'EDOUARD-DENIS','content-type':'application/json'}
urlPreprod ="https://rct-ed-callcenter.azurewebsites.net/api/Project/CreateOrUpdateProject4CallCenter"






def findDIndiceCalledAt(daty_anio):
    # THR20200605 : Ajout du filtre supplémentaire pour prendre en compte les flag_no_com qui ne sont pas 1
    QueryLoad = """select ed.indice as INDICE from [31_EA_EDOUARD_DENIS] ed
    where QUALIF_CODE in (1,2,3,91,99) and COALESCE(lib_detail,'') not in ('DOUBLONS','RACCROCHE','') and (is_sent_crm is null or is_sent_crm='') and flag_no_com is null and date >='20200526' """
    # THR20200619 : Sélectionner que les fiches dont la date d'appel est aujourd'hui
    daty_anio = str(daty_anio).replace('-','')
    QueryLoad = "SELECT ed.indice AS INDICE FROM [31_EA_EDOUARD_DENIS] ed WHERE QUALIF_CODE IN (1,2,3,91,99) AND COALESCE(lib_detail,'') NOT IN ('DOUBLONS','RACCROCHE','') AND is_sent_crm IS NULL AND flag_no_com IS NULL AND date ='" + str(daty_anio) + "'"
	
    QueryLoad = "SELECT ed.indice AS INDICE FROM [31_EA_EDOUARD_DENIS] ed WHERE (is_sent_crm IS NULL AND QUALIF_CODE IS NOT NULL AND flag_no_com IS NULL AND date ='" + str(daty_anio) + "') or (QUALIF_CODE IN (1,2,3,91,99) AND COALESCE(lib_detail,'') NOT IN ('DOUBLONS','RACCROCHE','') AND is_sent_crm IS NULL AND flag_no_com IS NULL AND date ='" + str(daty_anio) + "')" 
	
    if len(indicesSpecifiques):
        strIndices = ",".join(indicesSpecifiques)
        QueryLoad = "SELECT ed.indice AS INDICE FROM [31_EA_EDOUARD_DENIS] ed WHERE QUALIF_CODE IN (1,2,3,91,99) AND COALESCE(lib_detail,'') NOT IN ('DOUBLONS','RACCROCHE','') AND (is_sent_crm is null or is_sent_crm='') AND flag_no_com IS NULL AND ed.indice in (" + strIndices + ")"

    logging.info(QueryLoad)
    print (QueryLoad)
    IndiceFlag = edouarddenis.execute_crud(QueryLoad, typ='kk')
    print(IndiceFlag)
    return IndiceFlag



def findData2crm(indice):
    logging.info("Recherche des donnes pour l'indice : " +str(indice))
    query1 = """
    select ed.indice as callcenterprojectid,
    factoryprojectid,
    case when date_acquisition is null or date_acquisition='' then replace(convert(varchar, getDate(),120),' ','T') else date_acquisition end date_acquisition,
    ed.nom,
    ed.prenom,
    ed.email,
    tel_fixe,
    tel_mobile,
    adresse,
    adresse2,
    code_postal,
    profession,
    commentaire,
    type_logement,
    surface_logement,
    taille_logement,
    dept_rech,
    ville_rech,
    dbo.ray_GetNumeric(budget_max) as budget_max,
    ed.ville,
    case when code_programme is null or code_programme='' then '0063__'+programme_prodirect_val else code_programme end code_programme,
    projet_immo,
    utm_source,
    utm_medium,
    utm_capaign as utm_campaign,
    case when canal is null then 'cc006' else canal end as canal,
    case when salutation is null or salutation='' then salutat else salutation end salutation,
    case when situation_logement is null or situation_logement='' then situation_log else situation_logement end situation_logement,
    objectif_achat,
    email2,
    tel_professionnel,
    primo_accedant,
    coalesce((select email from oe_commerciaux where id = ed.id_commercial ), 'call-center@edouarddenis.fr') as commercial,
    utm_act as action,
    nature_bien as nature_logement,
    rgpdin,
	case when budget is null then '' Else budget End  as if_wishbudgetmax
    ,case when destination_achat is null then '' Else destination_achat End as if_mainsearchprofil
    ,case when taille_logement is null then '' Else taille_logement End as taille_logement
    ,case when ed.QUALIF_CODE in (3, 91,99) then 'INEXPLOITABLE' else ed.lib_status end  as cloture_call,
    case when ed.QUALIF_CODE = 91 then 'WRONG NUMBER SYSTEM' when ed.QUALIF_CODE =99 then 'INJOIGNABLE PERMANENT' else upper(ed.lib_detail) end as motif_cloture,
    case when ed.programme_prodirect_VAL is null or ed.programme_prodirect_VAL='' then code_programme else '0063__'+ed.programme_prodirect_VAL end  as programme_call,
    replace(replace(replace(convert(nvarchar(20),getDate(),120),' ',''),':',''),'-','') as attribdate_call,
    commentaires_agent as commentaire_call,
    revente,case when code_programme LIKE '%62934' OR '0063__'+programme_prodirect_val LIKE '%62934' THEN 'VIGED' ELSE CASE WHEN UPPER(ed.lib_status) like 'FAUX NU%' then 'FAUX NUMERO' else upper(ed.lib_status) end END as conclusioncode from [31_EA_EDOUARD_DENIS] ed
    WHERE ed.indice ={}""".format(indice)
    print (query1)
    #sys.exit()
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


def envoiMail(emailto):
    try:
        destiprincipale = emailto
        copie = ""
        template = "VIGED_CONFIRMATION.txt"
        message = TemplateString4Mail(template)
        objet = "EDOUARDDENIS | Confirmation"
        logging.info("message : " + str(message))
        if sendMailEdouardDenis(destiprincipale, message, objet):
            print('LASA')
        else:
            print('TSY LASA')
    except Exception as e:
        print (e)
        logging.info("START EXCEPTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logging.info(e)
        logging.info("END EXCEPTION   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def sendMailEdouardDenis(strTo, message, subject, copie=''):
    strFrom = 'groupe-edouard.denis@groupe-prodirect.com'
    memo = 'Tol90676'
    smtpServer = 'smtp.office365.com'
    port = 587
    copie = "thierry1804@gmail.com"
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot['Bcc'] = copie
    kasekoIto = ""
    # msgRoot['Bcc'] = kasekoIto
    msgRoot.preamble = 'html format mail.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)
    # sys.exit()

    # This example assumes the image is in the current directory
    basename = '//home//user1//programme_python//maquette_VIGED//'
    for filename in glob.iglob(basename + 'image//*', recursive=True):
        fname = '<' + str(os.path.basename(filename)).split('.')[0] + '>'
        fp = open(filename, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', fname)
        msgRoot.attach(msgImage)

    try:
        smtp = smtplib.SMTP(smtpServer, 25)
        smtp.connect(smtpServer, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(strFrom, memo)
        smtp.sendmail(strFrom, strTo.split(',') + copie.split(',') + kasekoIto.split(','), msgRoot.as_string())
        smtp.quit()
        print('mail sent')
        return True
    except Exception as e:
        print (e)
        logging.info("SOUCI D'ENVOI DE MAIL")
        logging.info(e)
        logging.info(strFrom)
        logging.info(strTo.split(','))
        logging.info(copie.split(','))
        logging.info(kasekoIto.split(','))
        return False


# mamaky an le mail sy ny variable
def TemplateString4Mail(fileMail):
    basename ='//home//user1//programme_python//maquette_VIGED//'
    with open(basename + fileMail, 'r') as f:
        message = f.read()
    return message


if connecter_site():
    logging.info("init service web lancement du programme at: " +str(lancementpgr) )
    print ("init service web")
    #trouve =findData('1850')
    #dataretr = json.dumps(trouve)
    #print (dataretr)
    #sys.exit() 
    dede = findDIndiceCalledAt(daty)
    print(dede)
    for el in dede:
        indigo = str(el.get("INDICE"))
        logging.info("indice encours de traitement : " +str(indigo)+ " uniqid: "+ str(uuid.uuid4()))
        #continue
        #sys.exit()
        trouve =findData2crm(indigo)
        if len(trouve) > 0 :        
            idpros =  trouve.get("callcenterprojectid")
            data_retr_code_programme = str(trouve.get("code_programme").replace("0063__", ""))
            data_retr_programme_call = str(trouve.get("programme_call").replace("0063__", ""))
            data_retr_commercial = trouve.get("commercial")
            data_retr_email = trouve.get("email")

            dataretr = json.dumps(trouve)
            logging.info(dataretr)
            print (dataretr)

            # Si on a un code programme et que le mail du commercial est call-center@edouarddenis.fr
            # alors ne pas continuer et mettre un flag dans 31_EA_EDOUARD_DENIS
            print("# -- " + str(lancementpgr) + " -- Début aiguillage...")
            logging.info("# -- " + str(lancementpgr) + " -- Début aiguillage...")

            print("# -- " + str(lancementpgr) + " -- " + data_retr_code_programme + " -- " + data_retr_programme_call + " -- " + data_retr_commercial)
            logging.info("# -- " + str(lancementpgr) + " -- " + data_retr_code_programme + " -- " + data_retr_programme_call + " -- " + data_retr_commercial)

            detail_a_verifier = ['RDV PHYSIQUE', 'RDV TELEPHONIQUE', 'RDV VISIO', 'ENVOI DE DOCUMENT', 'TRANSFERT ABOUTI', 'TRANSFERT NON ABOUTI', 'NOUS RECONTACTE', 'HORS BUDGET', 'PAS INTERESSE', 'PLUS DE DISP DE LOT', 'LIVRAISON TARDIVE', 'NOUVEAUX PROGRAMMES', 'PROGRAMME CLOTURE', 'SURFACE TROP PETITE', 'APPELS ADMIN', 'NE PARLE PAS FRANCAIS', 'INJOIGNABLE PERMANENT']

            if data_retr_commercial == 'call-center@edouarddenis.fr' and (len(data_retr_code_programme.strip()) > 0 or len(data_retr_programme_call.strip()) > 0) and trouve.get("motif_cloture") in detail_a_verifier:
                print("# -- " + str(lancementpgr) + " -- INDICE : " + str(indigo) + " -- MAJ FLAG commercial inapprorié et passer au suivant")
                logging.info("# -- " + str(lancementpgr) + " -- INDICE : " + str(indigo) + " -- MAJ FLAG commercial inapprorié et passer au suivant")

                # Mettre à jour le flag flag_no_com et la date date_no_com
                qryFiche = "UPDATE [31_EA_EDOUARD_DENIS] set flag_no_com = 1, date_no_com = GETDATE() WHERE INDICE = {}".format(indigo)
                edouarddenis.execute_crud(qryFiche)
                
                # Continuer à l'itération suivante
                continue

            logging.info("# -- " + str(lancementpgr) + " -- Fin aiguillage")
            print("# -- " + str(lancementpgr) + " -- Fin aiguillage")
            # Fin de l'aiguillage

            #sys.exit()
            retourta =requests.post(urlprod,data = dataretr, headers=prod).json() 
            logging.info('retour CRM: ' + str(retourta))
            error = retourta.get('error')
            erCode = error.get('erCode')
            erMessage = error.get('erMessage')
            factoryprojectid = retourta.get('factoryprojectid')
            logging.info("crm >>" + str(erCode) + str(erMessage) + str(factoryprojectid))
            print(erCode, erMessage, factoryprojectid)
            #sys.exit()
            if erCode is None and erMessage is None:
                print ('ok')
                logging.info("indice : " + str(indigo) + " with factoryid : " + factoryprojectid )  
                print("indice : " + str(indigo) + " with factoryid : " + factoryprojectid )

                # VIGED
                # if data_retr_code_programme == "62934":
                #     envoiMail(data_retr_email)

                #newFactory = retourta.get('factoryprojectid')
                #sys.exit()
                print ("l'indice : " + str(idpros) ) # +retourta.get('factoryprojectid') + " est update: ok")
                #sys.exit()
                qry = "update [31_EA_EDOUARD_DENIS] set is_sent_crm ='done', factoryprojectid='{}', sent_crm_at = convert(nvarchar, getDate(),120)  where indice = {}".format(factoryprojectid,indigo)
                if  edouarddenis.execute_crud(qry):
                    print('ok')
                    logging.info("update ok")
                    #sys.exit()
                else:
                    print('ko')
                    logging.info("qry ko : " + str(qry))
                    #sys.exit()
            else:
                logging.info(" envoi CRM KO raison: " + str(erCode) +" "+ str(erMessage))
                print(" envoi CRM KO raison: " + str(erCode) +" "+ str(erMessage))
                continue
            logging.info("***************** fin traitement indice " + str(indigo) + "*****************")
        else:
            logging.info('pas de correspondance trouve')
        
        #sys.exit()
        #continue
        #if str(requests.post(theuRl, data = json.dumps(findData(indigo)), headers=headers).json()).startswith('SUCCESS'):
        
        
        
        
        
        
        # else:
            # logging.debug("retour lp crm ed : " +str(indigo) + retourta)
            # print ('indice ' + indigo + ' not sent ')
            # varMessage = "Bonjour\n"
            # varMessage += "Une erreur est survenu lors du transfert du leads portant  l'indice : " + str(indigo)+"\n\n"
            # varMessage += "Voici le leads en question sous format json :\n"
            # varMessage +=  dataretr.replace(',',',\n')
            # varMessage += "Le web service a dit:\n " +json.dumps(retourta) + "\n"
            # varMessage += "\nCordialement !\n"
            # varMessage += "RaymanJune" 

            # SendMaxManMail('noreply@vivetic.com','N0reply2015','mail.vivetic.com','iscc@vivetic.mg',varMessage)
        #sys.exit()
    edouarddenis.closeo()
