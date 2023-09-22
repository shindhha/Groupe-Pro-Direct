
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
from email.mime.image import MIMEImage
from  string import Template


import glob
date_p = datetime.now()

daty = str(date.today())
#daty = '2019-11-13'
filenamelog ="//var//log_iscc//sendmailEdouarDenis_entrant_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("****************************date lancement programme: " + str(date_p)+" ******************************")

edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')

def flageroGlasaRamamy(text,indice):
    query ="UPDATE [31_EA_EDOUARD_DENIS] set ok_mail ='{}', mailSent_at= convert(nvarchar, getDate(),120) WHERE indice ={}".format(text, indice)
    return edouarddenis.execute_crud(query)

def findIndice2Send():
    Query = """
    select indice as INDICE from [31_EA_EDOUARD_DENIS]
       
        where (ok_mail is null or ok_mail = '') and date >= '20200605' and 
        (
            (QUALIF_CODE = 1 and (QUALIF_DETAIL between 1 and 7) and id_commercial is not null) or
            (QUALIF_CODE = 3 and QUALIF_DETAIL in(2,3) and id_commercial is not null) 
        ) ORDER BY indice, newID()
    """
    data =  edouarddenis.execute_crud(Query,typ='kk')
    try:
        return data
    except Exception as e:
        print("une erreur est survenue: " + str(e))
        sys.exit()
    
def recupDataUtil(indice):
    print('RE')
    logging.info(" recuperation des donnes utile pour l'indice : "  + str(indice))
    Query = """
    SELECT  format (cast (date as date) , 'dd/MM/yyyy ') as  date_hermes,
            convert(varchar(5),heure,8) as heure_hermes,
            tb.factoryprojectid,
            tb.utm_medium,
            case when tb.salutation='' or tb.salutation is null then 'Monsieur/Madame' else tb.salutation end as salutation,
            tb.nom as nom,
            tb.prenom as prenom,
            tb.adresse,
            tb.adresse2,
            tb.code_postal,
            tb.ville,
            tb.tel_mobile,
            tb.tel_fixe,
            tb.email,
            tb.programme_prodirect as programme_pds,
            tb.type_bienED as type_bien,
            tb.nature_bien,
            tb.budget_max,
            tb.objectif_achat,
            tb.revente,
            tb.date_rdv,
            convert(nvarchar(5), tb.heure_rdv,8) heure_rdv,
            CONCAT(lieu.ville ,' ', lieu.cp , ' ' , lieu.adresse , ' ', lieu.complement) lieu_rdv,
            tb.commentaires_agent,
            lib_detail as detail_statut_hermes,
            com.civilite as civcom,
            com.nom as nomcom,
            com.prenom as prenomcom,
            com.telephone2 as telcom,
            case when tb.type_logement is null or tb.type_logement='NULL' or tb.type_logement ='None' then '' else tb.type_logement end type_logement,
            case when tb.nature_logement is null or tb.nature_logement='NULL' or tb.nature_logement='None' then  '' else tb.nature_logement end nature_logement
            from [PROD_EDOUARD].[dbo].[31_EA_EDOUARD_DENIS] tb            
            left join [PROD_EDOUARD].[dbo].[oe_commerciaux] com on com.id = ISNULL(case when tb.id_commercial ='NULL' then NULL else tb.id_commercial end ,0)
            left join [PROD_EDOUARD].[dbo].[oe_lieu_rdv] lieu on lieu.id_lieu = ISNULL(case when tb.id_lieu_rdv ='NULL' then NULL else tb.id_lieu_rdv end ,0)
            left join [PROD_EDOUARD].[dbo].[oe_programmes] pg on pg.code2 = ISNULL(  case when tb.drapp ='NULL' or tb.drapp is null then replace(tb.code_programme,'0063__','') else tb.drapp end,0)
            where indice = {}""".format(indice)
    data = edouarddenis.execute_crud(Query, typ='kk')
    print('**********************************')
    print(Query)
    logging.info("requety lance : "  +str(Query))
    print('-------------------------------------')
    try:
        return data[0]
    except Exception as e:
        print (e)
        
def connecter_site(): 
  print('connection à la base')
  logging.info("connexion à la base de donnée")
  try:
    dict_tomatika = edouarddenis.connecting()
    logging.info("connexion réussi") 
    return True
  except:
    id_erreur="connection a la base"
    logging.debug("Erreur de connexion à la base")
    return False

def updateMailSented(indice):
    query = "UPDATE [31_RA_EDOUARD_DENIS] set mail_sent ='done' WHERE INDICE = {}".format(indice)
    sys.exit()
    if edouarddenis.execute_crud(query):
        return 1
    return 0
    
def GetTemplateObjectDestinator(indice):
    Qry = """  

        SELECT tb.indice,

        CASE
        WHEN
        QUALIF_CODE = 1 and QUALIF_DETAIL = 1 then 'RDV_PHYSIQUE_PROSPECT.txt_separateurtraitement_RDV_PHYSIQUE_COMMERCIAL.txt'
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (6) then 'RDV_TELEPHONIQUE_PROSPECT_V2.txt_separateurtraitement_RDV_TELEPHONIQUE_COMMERCIAL.txt'
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (3) then 'RDV_TELEPHONIQUE_PROSPECT_V1.txt_separateurtraitement_RDV_TELEPHONIQUE_COMMERCIAL.txt'
            WHEN
            QUALIF_CODE = 2 and QUALIF_DETAIL < 10 then 'REFUS_COMMERCIAL.txt'
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 3 then 'INEXPLOITABLE_COMMERCIAL.txt'
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 2 then 'APPEL_ADMINISTRATIF.txt'
            WHEN
            QUALIF_CODE =91 then 'DEMANDE_INFO_PROSPECT.txt'
            WHEN
            QUALIF_CODE =99 then 'DEMANDE_INFO_PROSPECT.txt_separateurtraitement_INEXPLOITABLE_INJOIGNABLE.txt'
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (2,4,5) then 'AUTRE_COMMERCIAL.txt'
            ELSE
            ''
            END Template,

            CASE
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL = 1 then case when tb.email is null or tb.email='' then tb.email2 else tb.email end + '_separateurtraitement_' + com.email +'--'+ com.mail_copie
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (3,6) then CONCAT(case when tb.email is null or tb.email='' then tb.email2 else tb.email end , '_separateurtraitement_' , com.email ,'--', com.mail_copie)
            WHEN
            QUALIF_CODE = 2 and QUALIF_DETAIL < 10 then CONCAT(com.email ,'--', com.mail_copie)
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 3 then CONCAT(com.email ,'--', com.mail_copie)
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 2 then CONCAT(com.email ,'--', com.mail_copie)
            WHEN
            QUALIF_CODE = 91 then case when tb.email is null or tb.email='' then tb.email2 else tb.email end
            WHEN
            QUALIF_CODE = 99 then CONCAT(case when tb.email is null or tb.email='' then tb.email2 else tb.email end , '_separateurtraitement_' , com.email ,'--', com.mail_copie)
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (2,4,5) then CONCAT(com.email ,'--', com.mail_copie)
            ELSE
            ''
            END destinataire,

            CASE
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL = 1 then CONCAT('Votre Rendez-vous EDOUARD DENIS' , '_separateurtraitement_' , 'RDV pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom,  '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL in (3,6) then CONCAT('Votre Rendez-vous EDOUARD DENIS' , '_separateurtraitement_' , 'RDV pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 2 and QUALIF_DETAIL < 10 then CONCAT('REFUS pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 3 then CONCAT('INEXPLOITABLE pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 3 and QUALIF_DETAIL = 2 then 'Appel Administratif'
            WHEN
            QUALIF_CODE = 91 then 'Votre demande d''information Edouard Denis'
            WHEN
            QUALIF_CODE=99 then CONCAT('Votre demande d''information Edouard Denis','_separateurtraitement_','INJOIGNABLE pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL = 2 then CONCAT('TRANSFERT ABOUTI pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL = 4 then CONCAT('TRANSFERT NON ABOUTI pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            WHEN
            QUALIF_CODE = 1 and QUALIF_DETAIL = 5 then CONCAT('DEMANDE DE DOC pour "' , tb.salutat ,' ' , tb.nom , ' ' , tb.prenom , '" avec ' , com.civilite , ' ' , com.nom , ' ' , com.prenom)
            ELSE
            ''
            END objet


            from [PROD_EDOUARD].[dbo].[31_ea_EDOUARD_DENIS] tb           
            left join [PROD_EDOUARD].[dbo].[oe_commerciaux] com on com.id = ISNULL(case when tb.id_commercial ='NULL' then NULL else tb.id_commercial end ,0)
            left join [PROD_EDOUARD].[dbo].[oe_lieu_rdv] lieu on lieu.id = ISNULL(case when tb.id_lieu_rdv ='NULL' then NULL else tb.id_commercial end ,0)
            left join [PROD_EDOUARD].[dbo].[oe_programmes] pg on pg.code2 = ISNULL(case when tb.code_programme ='NULL' or tb.code_programme is null then tb.drapp else replace(tb.code_programme,'0063__','') end,0)

    where indice = {}""".format(indice)
    retour = edouarddenis.execute_crud(Qry, typ='kk')
    data = retour[0]
    return data

#objet distinataire copie
def Mainparam(indice):
    datapart = GetTemplateObjectDestinator(indice)
    try:
        logging.info("******************** debut de traitement *****************************")
        listTemplate = datapart.get('Template').split('_separateurtraitement_')
        print('eatttt')
        listDestinataire = datapart.get('destinataire').split('_separateurtraitement_')
        print('splite manaraka')
        if datapart.get('objet'):
            Listobjet = datapart.get('objet').split('_separateurtraitement_')
        else:
            Listobjet = ['']
        mlahatra = zip(listTemplate,listDestinataire,Listobjet)
        print (mlahatra)
        
        print('mandalo ato v')
        destiprincipale=""
        copie=""
        destinataire=""
        if len(listTemplate) > 1:            
            for ele in mlahatra:
                template = ele[0]
                destinataire = ele[1].split('--')
                logging.info(template)
                logging.info(destinataire)
                print('mandalo aty')
                #sys.exit()
                if len(destinataire) > 1:
                    destiprincipale = destinataire[0]
                    copie = destinataire[1]
                else:
                    destiprincipale = ele[1]
                    copie=""
                print(ele)  
                objet = ele[2]
                logging.info(destiprincipale)
                #sys.exit()
                message = TemplateString4Mail(template, recupDataUtil(indice))
                logging.info("message : " + str(message))
                if sendMailEdouardDenis(destiprincipale,message,objet,copie):
                    flageroGlasaRamamy('OUI',indice)
                else:
                    flageroGlasaRamamy('PROBLEME',indice) 
                # recupere data
                
                
            #
        else:
            print('template ray')
            logging.info(" 1 template trouve")
            if len(listDestinataire) > 1:
                print('niditra teto')
                destiprincipale = listDestinataire[0]
                copie = listDestinataire[1]
                print('nakato')
            else:
                print('tafiditra tato')
                print(listDestinataire)
                destiprincipale = listDestinataire[0].split('--')[0]
                try:
                    copie=listDestinataire[0].split('--')[1] 
                except Exception as e:
                    copie=""
                print('tsy tatko')
            message = TemplateString4Mail(listTemplate[0], recupDataUtil(indice))
            print(destiprincipale, copie)
            logging.info(" destinateur et copie trouve : " + str(destiprincipale) + str(copie) )
            #sys.exit()
            if sendMailEdouardDenis(destiprincipale,message, Listobjet[0],copie):
                flageroGlasaRamamy('OUI',indice)
                updateMailSented(indice)
            else:
                flageroGlasaRamamy('PROBLEME',indice)  
            #Listobjet
        #sys.exit()
    except Exception as e:
        print (e)
        logging.info("probleme au niveau du resultat du query")
        logging.info(e)

def sendMailEdouardDenis(strTo,message,subject,copie=''):

    strFrom = 'groupe-edouard.denis@groupe-prodirect.com'
    #memo = 'Tol90676'
    memo = 'Nob74133'
    smtpServer = 'smtp.office365.com'
    port = 587
    #strTo = "jp.grima@edouarddenis.fr,f.decker@edouarddenis.fr,f.derothiacob@edouarddenis.fr" #"iscc@vivetic.mg"
    #copie= "hgomez@groupe-prodirect.com"
# Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot['Cc'] = copie
  #  kasekoIto = "iscc@vivetic.mg"
    #msgRoot['Bcc'] = kasekoIto
    msgRoot.preamble = 'html format mail.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    
    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)
    #sys.exit()

    # This example assumes the image is in the current directory
    # extraire les sary
    basename ='//home//user1//programme_python//maquette//'
    for filename in glob.iglob(basename+'images//*', recursive=True):
        fname ='<'+ str(os.path.basename(filename)).split('.')[0]+'>'
        
        fp = open(filename, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        # Define the image's ID as referenced above
        
        msgImage.add_header('Content-ID', fname)
        msgRoot.attach(msgImage)

   
    try:

        smtp = smtplib.SMTP(smtpServer,25)
        smtp.connect(smtpServer,587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(strFrom, memo)
        #smtp.sendmail(strFrom, strTo.split(',')+copie.split(',')+kasekoIto.split(','), msgRoot.as_string())
        smtp.sendmail(strFrom, strTo.split(',')+copie.split(','), msgRoot.as_string())
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
        #logging.info(kasekoIto.split(','))
        return False
    
# mamaky an le mail sy ny variable
def TemplateString4Mail(fileMail, dicta):
    basename ='//home//user1//programme_python//maquette//'
    with open(basename + fileMail, 'r') as f:
        message = f.read()
    data = Template(message)
    return data.substitute(dicta)

  
#sendMailEdouardDenis('iscc@vivetic.mg','fabrice.razanajatovo@vivetic.mg','RDV_PHYSIQUE_PROSPECT.txt','RDV TELEPHONIQUE PROSPECT')

if connecter_site():
    #Mainparam(1260762)
    listINdice = findIndice2Send()
    #print(listINdice)
    for ele in  listINdice :
        indice = ele.get('INDICE')
        print(indice)
        Mainparam(indice)
        #sys.exit()
    edouarddenis.closeo()

