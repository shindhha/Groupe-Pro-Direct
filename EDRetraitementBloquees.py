#! /usr/bin/env python
#coding=utf-8

import os,sys,logging, uuid
import requests, json, time
from RaycnxDict import Raycnx
from datetime import date, timedelta,datetime

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
date_p = datetime.now()

indicesSpecifiques = []
if len(sys.argv) > 1:
    indicesSpecifiques = sys.argv[1].split(',')

def connecter_site(): 
    logging.info(str(datetime.now()) + ":> Connexion à la base de données")
    try:
        dict_tomatika = edouarddenis.connecting()
        logging.info(str(datetime.now()) + ":>> Connexion réussie") 
        return True
    except:
        logging.debug(str(datetime.now()) + ":>> Erreur de connexion à la base")
        return False

def logDate():
    daty = str(date.today())
    return str(daty).replace('-','')

def getARetraiter():
    QueryLoad = """
        SELECT
            red.factoryprojectid, 
            red.INDICE,
            red.id_commercial, 
            coalesce((SELECT email FROM oe_commerciaux WHERE id = CASE WHEN red.id_commercial = 'NULL' THEN 0 ELSE red.id_commercial END ), 'call-center@edouarddenis.fr') as commercial,
            REPLACE(CASE WHEN (red.drapp IS NULL OR red.drapp = '') THEN red.code_programme ELSE red.drapp END, '0063__', '') AS code2,
            red.code_programme,
            red.drapp,
            red.programme_prodirect,
            red.programme_prodirect_VAL,
            cred.DATE AS dateappel,
            red.code_postal
        FROM C1_31_RA_EDOUARD_DENIS cred 
        INNER JOIN [31_RA_EDOUARD_DENIS] red ON red.INDICE = cred.INDICE 
        WHERE 1 = 1
        AND red.flag_no_com = 1
        AND cred.DATE > '20200619'
        AND cred.STATUS = 99
    """
    
    logging.info(str(datetime.now()) + ":>>> " + QueryLoad)
    print (QueryLoad)
    indices = edouarddenis.execute_crud(QueryLoad, typ='kk')
    return indices

def getCommercialAAffecter(code_programme, code_postal):
    query = "select  top 1 t2.id as ID,t2.email as email from oe_commerciaux t2 inner join oe_programme_commerciaux a on a.id_commercial = t2.id WHERE a.code2 = replace('{}','0063__','') and COALESCE(a.commercial_admin, 0) != 1 order by a.fake_compteur, newid();".format(code_programme)
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(query))
    print (query)
    data = edouarddenis.execute_crud(query,typ='kk')
    print(data)
    if len(data) > 0:
        return data[0]
    else:
        query = "SELECT TOP 1 oc.id AS ID, oc.email FROM oe_commerciaux oc INNER JOIN oe_commercial_region ocr ON ocr.id_commerciale = oc.id INNER JOIN correspondance_departement_ed cde ON cde.id_region = ocr.id_region WHERE cde.departement = CASE WHEN LEN('{}') = 5 THEN LEFT('{}', 2) ELSE CONCAT('0', LEFT('{}', 1)) END ORDER BY ocr.fake_compteur, newid();".format(code_postal, code_postal, code_postal)
        print (query)
        logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(query))
        data = edouarddenis.execute_crud(query,typ='kk')
        print(data)
        if len(data) > 0:
            return data[0]
        else:
            query = "select  top 1 t2.id as ID,t2.email as email from oe_commerciaux t2 inner join oe_programme_commerciaux a on a.id_commercial = t2.id WHERE a.code2 = replace('{}','0063__','') and COALESCE(a.commercial_admin, 0) != 1 order by a.fake_compteur, newid();".format('6025')
            print (query)
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(query))
            data = edouarddenis.execute_crud(query,typ='kk')
            print(data)
            if len(data) > 0:
                return data[0]
            else:
                return 0

def findData2crm(indice):
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Recherche des données pour l'indice : " +str(indice))
    query1 = """
    select ed.indice_debut as callcenterprojectid,
    case when factoryprojectid='None' then null else factoryprojectid end factoryprojectid,
    date_acquisition,
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
    code_programme,
    projet_immo,
    utm_source,
    utm_medium,
    utm_capaign as utm_campaign,
    canal,
    case when salutation is null or salutation='' then salutat else salutation end salutation,
    situation_logement,
    objectif_achat,
    email2,
    tel_professionnel,
    primo_accedant,
    coalesce((SELECT email from oe_commerciaux where id = ISNULL(case when ed.id_commercial ='NULL' then NULL else ed.id_commercial end,0) ),'call-center@edouarddenis.fr') as commercial,
    utm_act as action,
    replace(type_bienEd,' ','') as type_logementED,
    nature_bien as nature_logement,
    rgpdout,
    rgpdin,
    c1.status as statuman,
    case when c1.status in (3, 91,99) then 'INEXPLOITABLE' else c1.lib_status end  as cloture_call,
    case when c1.status = 91 then 'WRONG NUMBER SYSTEM' when c1.status =99 then 'INJOIGNABLE PERMANENT' else upper(c1.lib_detail) end as motif_cloture,
    CASE WHEN 
        LEN(case when drapp is null or drapp='NULL' or drapp=''  then (case when code_programme like '0063__%' then code_programme else '0063__'+code_programme end) else
    (case when cast(drapp as varchar) like '0063__%' then drapp else '0063__'+cast(drapp as varchar) end) end ) = 6 then ''
    ELSE 
    case when drapp is null or drapp='NULL' or drapp=''  then (case when code_programme like '0063__%' then code_programme else '0063__'+code_programme end) else
    (case when cast(drapp as varchar) like '0063__%' then drapp else '0063__'+cast(drapp as varchar) end) end end
    programme_call,
    replace(replace(replace(convert(nvarchar(20),getDate(),120),' ',''),':',''),'-','') as attribdate_call,
    commentaires_agent as commentaire_call,
    revente,
    case when UPPER(c1.lib_status) like 'FAUX NU%' then 'FAUX NUMERO' when UPPER(c1.lib_status) like '%WRONG%'  then 
    'WRONG NUMBER SYSTEM' when c1.lib_status = 'UnreachableLimit' then 'INJOIGNABLE PERMANENT' else upper(c1.lib_detail) end as conclusioncode from [31_RA_EDOUARD_DENIS] ed
    inner join [c1_31_RA_EDOUARD_DENIS] c1 on c1.indice = ed.indice
    WHERE ed.indice = {}""".format(indice)

    print (query1)

    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Requette lancée:\n: " + query1)
    data = edouarddenis.execute_crud(query1, typ='kk')
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Contenu retourné : " + str(data[0]))
    return data[0]

def updateIdCom4Injoingable(indice, id_com):
    query = "UPDATE [31_RA_EDOUARD_DENIS] set id_commercial = {}, flag_no_com = NULL, date_no_com = NULL WHERE indice = {}".format(id_com, indice)
    # query = "UPDATE [31_RA_EDOUARD_DENIS] set id_commercial = {} WHERE indice = {}".format(id_com, indice)
    return edouarddenis.execute_crud(query)

def checkReturnCrm(callprojectAnous, callprojectCRM):
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Comparaison de celui qu'on a envoyé (" + str(callprojectAnous) + ") vs retour crm (" + str(callprojectCRM) + ") le : " + str(date_p))
    if callprojectAnous == callprojectCRM:
        return True
    return False

def updateCompteurCom(id_com, code_programme):
    query = """
        UPDATE [oe_programme_commerciaux] 
            SET
                compteur = compteur + 1,
                fake_compteur = fake_compteur + 1       
        WHERE id_commercial = '{}' and code2 = replace('{}','0063__','')
    """.format(id_com,code_programme)
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> MAJ COMPTEUR COMMERCIAL " + str(query))
    return edouarddenis.execute_crud(query)

def updateFactoryProjectId(indice, factoryid, factoryinit):
    if not factoryinit:
        query = "UPDATE [31_RA_EDOUARD_DENIS] set factoryprojectid = '{}' where indice_debut = {}; UPDATE EDOUARDDENIS set factoryprojectid ='{}' where indice ={}".format(factoryid, indice, factoryid,indice)
        logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> MAJ factoryprojectid : " + str(query))
        print (query)
        #sys.exit()
        return edouarddenis.execute_crud(query)
    print ("tsy nataony")
    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> MAJ bon faite")
    return 0

filenamelog ="//home//user1//programme_python//logs//bloquees//traitement_"+ logDate() + ".log"
edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
theuRl = "https://prd-ed-projet.azurewebsites.net/api/Project/CreateOrUpdateProject4CallCenter" 
headers = {'apikey': "ED-FACTORY-PROJET*2020", 'content-type': 'application/json'}

logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info(str(datetime.now()) + ":## Retraitement lancé ########################")

if connecter_site():
    print ("init service web at : " + str(datetime.now()))
    for fiche in getARetraiter():
        idUniq = uuid.uuid4()
        
        logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>> " + str(fiche.get('INDICE')) + " - " + str(fiche.get('code2')) + " - " + str(fiche.get('code_postal')))

        indice = fiche.get('INDICE')
        codeProgramme = fiche.get('code2')
        codePostal = fiche.get('code_postal')

        infocom = getCommercialAAffecter(codeProgramme, codePostal)
        if infocom != 0:
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(fiche.get('INDICE')) + " - " + str(infocom.get('email')) + " - " + str(infocom.get('ID')))
            email = infocom.get('email')
            id_com = infocom.get('ID')

            # MISE A JOUR DU COMMERCIAL
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Mise à jour du commercial" + str(updateIdCom4Injoingable(indice, id_com)))

            try:
                trouve = findData2crm(indice)
            except:
                continue
            
            idpros =  trouve.get("callcenterprojectid")
            initfactory = trouve.get("factoryprojectid")
            code_ = trouve.get('code_programme')

            dataretr = json.dumps(trouve)
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(dataretr))
            print (dataretr)

            # Envoi des données vers le CRM client
            retourta =requests.post(theuRl, data = dataretr, headers=headers).json() 
            time.sleep(2) # attente de 2 s pour le WS
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Retour CRM : " + str(retourta))
            print(retourta)
            
            error = retourta.get('error')
            ecode = error.get('erCode')
            emessage = error.get('erMessage')
            callprojectid_retour = retourta.get('callcenterprojectid')
            
            if ecode is None or emessage is None:
                if not checkReturnCrm(callprojectid_retour, idpros):
                    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Incompatibilité entre l'entrée (" + str(idpros) + ") et le retour (" + str(callprojectid_retour) +")")
                    continue
                logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Ok entre l'entrée (" + str(idpros) + ") et le retour (" + str(callprojectid_retour) +")")
                print("mise à jour crm ok pour l'indice " +str(idpros))
                
                factory = retourta.get('factoryprojectid')
                print (factory)
                logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Factory  origine : " + str(initfactory) + " vs factory retour crm " + str(factory))
                print("factory  origine : " + str(initfactory) + " factory retour crm " + str(factory)) 
                updateFactoryProjectId(idpros, factory,initfactory)
                print ("l'indice : " + str(idpros) ) # +retourta.get('factoryprojectid') + " est update: ok")
                
                updateCompteurCom(id_com, code_)
                logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Nouvel id_commercial : " + str(id_com))
                print('naazo commercial vita update compteur et compteur fake')
                
                qry = "update [31_RA_EDOUARD_DENIS] set is_sent_crm ='done' , sentCrm_at = convert(varchar, getdate(),120) where indice = {};".format(indice)
                if  edouarddenis.execute_crud(qry):
                    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Mise à jour c1: ok ")
                    print('ok')
                else:
                    print('ko')
                    logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> La mise à jour du c1 a échouée")
            else:
                logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> Message "  + str(emessage) + "code erreur : "  + str(ecode))
                print(emessage, ecode)
                continue
        else:
            logging.info(str(idUniq) + ":" + str(datetime.now()) + ":>>>>> " + str(fiche.get('INDICE')) + " - RAS")
    edouarddenis.closeo()
else:
    print ("Impossible de se connecter")

logging.info(str(datetime.now()) + ":## Fin du retraitement #######################")