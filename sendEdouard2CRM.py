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



daty = str(date.today())
#daty = '2019-11-13'
filenamelog ="//home//user1//programme_python//logs//miseajourcrmedLog_"+ str(daty).replace('-','') + ".log"
logging.basicConfig(filename=filenamelog, level=logging.DEBUG)
logging.info("date lancement programme: " + str(date_p))
def isValidIdCom(code_programme, drapp, idcom):
    Query = " SELECT top 1 id from oe_programme_commerciaux where ('0063__'+ code2 = '{}' or code2 = '{}') and id_commercial = {}".format(code_programme,drapp,idcom)
    retour = edouarddenis.execute_crud(Query, typ='kk')
    return retour

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
theuRl = "https://prd-ed-projet.azurewebsites.net/api/Project/CreateOrUpdateProject4CallCenter" 
headers = {'apikey': "ED-FACTORY-PROJET*2020", 'content-type': 'application/json'}

#flagta = False

def updateFactoryProjectId(indice, factoryid,factoryinit):
    if not factoryinit:
        query = "UPDATE [31_RA_EDOUARD_DENIS] set factoryprojectid = '{}' where indice_debut = {}; UPDATE EDOUARDDENIS set factoryprojectid ='{}' where indice ={}".format(factoryid, indice, factoryid,indice)
        print (query)
        #sys.exit()
        return edouarddenis.execute_crud(query)
    print ("tsy nataony")
    return 0


def findDIndiceCalledAt(daty_anio):
    # THR20200605 : Ajout du filtre supplémentaire pour prendre en compte les flag_no_com qui ne sont pas 1
    QueryLoad = """select ed.indice as INDICE from [31_RA_EDOUARD_DENIS] ed 
    inner join [c1_31_RA_EDOUARD_DENIS] c1 on c1.indice = ed.indice
    where  c1.status in (1,2,3,91,99) and c1.date >='20200619' and COALESCE(c1.lib_detail, '') not in ('DOUBLONS','RACCROCHE') and is_sent_crm is null and flag_no_com is null"""
    # THR20200619 : Sélectionner que les fiches dont la date d'appel est aujourd'hui
    daty_anio = str(daty_anio).replace('-','')
    #QueryLoad = "SELECT ed.indice AS INDICE FROM [31_RA_EDOUARD_DENIS] ed INNER JOIN [c1_31_RA_EDOUARD_DENIS] c1 ON c1.indice = ed.indice WHERE c1.status IN (1,2,3,91,99) AND c1.date >='" + str(daty_anio) + "' AND COALESCE(c1.lib_detail, '') NOT IN ('DOUBLONS','RACCROCHE') AND is_sent_crm IS NULL AND flag_no_com IS NULL"
	#THR20230601 : Modification de la requête : rajout de qualification FAUX NUMERO + Email non vide ni null
    QueryLoad = "SELECT ed.indice AS INDICE FROM [31_RA_EDOUARD_DENIS] ed INNER JOIN [c1_31_RA_EDOUARD_DENIS] c1 ON c1.indice = ed.indice WHERE (c1.status IN (1,2,3,99) AND c1.date >='" + str(daty_anio) + "' AND COALESCE(c1.lib_detail, '') NOT IN ('DOUBLONS','RACCROCHE')  AND is_sent_crm IS NULL  AND flag_no_com IS NULL)  OR (c1.status=91 and email is not null and email<>'' AND is_sent_crm IS NULL  AND flag_no_com IS NULL AND c1.date >='" + str(daty_anio) + "')"
	
    if len(indicesSpecifiques):
        strIndices = ",".join(indicesSpecifiques)
        QueryLoad = "SELECT ed.indice AS INDICE FROM [31_RA_EDOUARD_DENIS] ed INNER JOIN [c1_31_RA_EDOUARD_DENIS] c1 ON c1.indice = ed.indice WHERE c1.status IN (1,2,3,91,99) AND ed.indice in (" + strIndices + ") AND COALESCE(c1.lib_detail, '') NOT IN ('DOUBLONS','RACCROCHE') AND is_sent_crm IS NULL AND flag_no_com IS NULL"
    
    logging.info(QueryLoad)
    print (QueryLoad)
    IndiceFlag = edouarddenis.execute_crud(QueryLoad, typ='kk')
    return IndiceFlag
def checkReturnCrm(callprojectAnous, callprojectCRM):
    logging.info("comparaison de celle qu'on a envoyer (" + str(callprojectAnous) + ") vs retour crm (" + str(callprojectCRM) + ") le : " + str(date_p))
    if callprojectAnous == callprojectCRM:
        return True
    return False

# Ajout de deux paramètres supplémentaires: codePostal et codeStatus
def getCommercial4Injoignable(code_programme, codePostal, codeStatus):
    query = """
    select  top 1 t2.id as ID,t2.email as email from oe_commerciaux t2
            inner join oe_programme_commerciaux a on a.id_commercial = t2.id
    WHERE a.code2 != 0 AND a.code2 = replace('{}','0063__','') and COALESCE(a.commercial_admin, 0) != 1 order by a.fake_compteur, newid()
    """.format(code_programme)
    print (query)
    data = edouarddenis.execute_crud(query,typ='kk')
    print(data)
    if len(data) > 0:
        return data[0]
    else:
        # Si on ne trouve rien, vérifions qu'il s'agit d'INJOIGNABLE PERMANENT (99)
        if str(codeStatus) == "99":
            # Si c'est le cas alors essayer de retrouver un commercial à l'aide du code postal
            # query = "SELECT TOP 1 oc.id AS ID, oc.email FROM oe_commerciaux oc INNER JOIN oe_commercial_region ocr ON ocr.id_commerciale = oc.id INNER JOIN correspondance_departement_ed cde ON cde.id_region = ocr.id_region WHERE cde.departement = CASE WHEN LEN('{}') = 5 THEN LEFT('{}', 2) ELSE CONCAT('0', LEFT('{}', 1)) END ORDER BY ocr.fake_compteur, newid();".format(codePostal, codePostal, codePostal)
            # Modficiation ce 20201106 par Thierry : Ne pas prendre dans les commerciaux ceux qui sont admins
            # query = "SELECT TOP 1 oc.id AS ID, oc.email FROM oe_commerciaux oc INNER JOIN oe_commercial_region ocr ON ocr.id_commerciale = oc.id INNER JOIN correspondance_departement_ed cde ON cde.id_region = ocr.id_region WHERE cde.departement = CASE WHEN LEN('{}') = 5 THEN LEFT('{}', 2) ELSE CONCAT('0', LEFT('{}', 1)) END AND oc.id NOT IN (SELECT DISTINCT orac.id_commercial_admin FROM oe_region_admin_commerciaux orac LEFT JOIN oe_region or2 ON or2.id_region = orac.id_region LEFT JOIN oe_commerciaux oc ON oc.id = orac.id_commercial_admin INNER JOIN oe_programmes op ON CAST(op.code2 AS int) = orac.code2 WHERE orac.id_region = cde.id_region) ORDER BY ocr.fake_compteur, newid();".format(codePostal, codePostal, codePostal)
            # Modification ce 20201117 par Thierry : Exclure carrément les commerciaux admins quelque soit leur région
            # query = "SELECT TOP 1 oc.id AS ID, oc.email FROM oe_commerciaux oc INNER JOIN oe_commercial_region ocr ON ocr.id_commerciale = oc.id INNER JOIN correspondance_departement_ed cde ON cde.id_region = ocr.id_region WHERE cde.departement = CASE WHEN LEN('{}') = 5 THEN LEFT('{}', 2) ELSE CONCAT('0', LEFT('{}', 1)) END AND oc.id NOT IN (SELECT DISTINCT opc.id_commercial FROM oe_programme_commerciaux opc WHERE opc.commercial_admin = 1) ORDER BY ocr.fake_compteur, newid();".format(codePostal, codePostal, codePostal)
            # Modification ce 20210416 par Thierry : Si pas de code programme, mais un code postal fourni, alors rechercher un commercial non admin parmi ceux affectés au programme imprecis correspondant à la région du code postal
            # SELECT TOP 1 t2.id as ID,t2.email as email, op.nom, op.code2, opr.id_region FROM oe_commerciaux t2 INNER JOIN oe_programme_commerciaux a ON a.id_commercial = t2.id INNER JOIN oe_programmes op ON op.code2 = a.code2 INNER JOIN oe_programme_region opr ON opr.code2 = op.code2 INNER JOIN correspondance_departement_ed cde ON cde.id_region = opr.id_region WHERE 1 = 1 AND COALESCE(a.commercial_admin, 0) != 1 AND op.nom LIKE 'IMPRECIS%' AND cde.departement = CASE WHEN LEN('13014') = 5 THEN LEFT('13014', 2) ELSE CONCAT('0', LEFT('13014', 1)) END AND op.code2 != 6025 ORDER BY a.fake_compteur, newid();
			
            query = """ SELECT TOP 1 t2.id as ID,t2.email as email, op.nom, op.code2, opr.id_region 
   FROM oe_commerciaux t2 INNER JOIN oe_programme_commerciaux a ON a.id_commercial = t2.id 
   INNER JOIN oe_programmes op ON op.code2 = a.code2 
   INNER JOIN oe_programme_region opr ON opr.code2 = op.code2 
   INNER JOIN correspondance_departement_ed cde ON cde.id_region = opr.id_region and cde.departement=op.departement
	WHERE 1 = 1 AND COALESCE(a.commercial_admin, 0) != 1 
	AND op.nom LIKE 'IMPRECIS%'
	 AND cde.departement = CASE WHEN LEN('{}') = 5 THEN LEFT('{}', 2) ELSE CONCAT('0', LEFT('{}', 1)) END AND op.code2 != 6025 
	 ORDER BY a.fake_compteur, newid();""".format(codePostal, codePostal, codePostal)
            print (query)
            logging.info("DTHR >>> uniqid : "+str(id_uniq) + " >>>")
            logging.info(query)
            logging.info("FTHR >>> uniqid : "+str(id_uniq) + " >>>")
            data = edouarddenis.execute_crud(query,typ='kk')
            print(data)
            if len(data) > 0:
                return data[0]
            else:
                # Si on n'a rien trouvé à partir du code postal, essayer de trouver un commercial non admin pour le code programme 6025 (IMPRECIS GENERAL SANS CODE POSTAL)
                query = "SELECT TOP 1 t2.id AS ID,t2.email AS email FROM oe_commerciaux t2 INNER JOIN oe_programme_commerciaux a ON a.id_commercial = t2.id WHERE a.code2 = replace('{}','0063__','') AND COALESCE(a.commercial_admin, 0) != 1 ORDER BY a.fake_compteur, newid();".format('6025')
                print (query)
                data = edouarddenis.execute_crud(query,typ='kk')
                print(data)
                if len(data) > 0:
                    return data[0]
                else:
                    return 0
        # Si ce n'est pas le cas, retourner 0
        else:
            return 0
    

def updateCompteurCom(id_com,code_programme):
    query = """
        UPDATE [oe_programme_commerciaux] 
            SET
                compteur = compteur + 1,
                fake_compteur = fake_compteur + 1       
        WHERE id_commercial = '{}' and code2 = replace('{}','0063__','')
    """.format(id_com,code_programme)
    logging.info("MAJ COMPTEUR COMMERCIAL " + str(query))
    return edouarddenis.execute_crud(query)


def findData2crm(indice):
    logging.info("Recherche des donnes pour l'indice : " +str(indice))
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
    nature_bien as nature_logement,
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
	case when budget is null then '' Else budget End  as if_wishbudgetmax
    ,case when destination_achat is null then '' Else destination_achat End as if_mainsearchprofil
    ,case when taille_logement is null then '' Else taille_logement End as taille_logement

    ,replace(replace(replace(convert(nvarchar(20),getDate(),120),' ',''),':',''),'-','') as attribdate_call,
    commentaires_agent as commentaire_call,
    revente,
    case when UPPER(c1.lib_status) like 'FAUX NU%' then 'FAUX NUMERO' when UPPER(c1.lib_status) like '%WRONG%'  then 
    'CONTACT MAIL' when c1.lib_status = 'UnreachableLimit' then 'INJOIGNABLE PERMANENT' else upper(c1.lib_detail) end as conclusioncode from [31_RA_EDOUARD_DENIS] ed
    inner join [c1_31_RA_EDOUARD_DENIS] c1 on c1.indice = ed.indice
    WHERE ed.indice = {}""".format(indice)
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
def updateIdCom4Injoingable(indice,id_com):
    query = "UPDATE [31_RA_EDOUARD_DENIS] set id_commercial = {} WHERE indice = {}".format(id_com, indice)
    return edouarddenis.execute_crud(query)

if connecter_site():
    print ("init service web at : " + str(date_p))
    for el in findDIndiceCalledAt(daty):
        indigo = str(el.get("INDICE"))
        id_uniq = uuid.uuid4() # Definition de l'ID unique pour cette ligne THR20200602
        logging.info("********************************** debut de traitement indice "+ str(indigo) +" uniqid : "+str(id_uniq) + " *********************")


        try:

            trouve =findData2crm(indigo)

        except:
            continue
        if len(trouve) > 0 :
            #isValidIdCom(code_programme, drapp, idcom)            
            idpros =  trouve.get("callcenterprojectid")
            initfactory = trouve.get("factoryprojectid")
            status_ = trouve.get('statuman')
            code_ = trouve.get('code_programme')
            codePostal = trouve.get('code_postal') # reccueillir le code postal
            flagta = False
            id_com = ""
            print (status_, code_)
            if str(status_) == "99":
                print ("nandalo tato iz satria : "  + str(status_))
                infocom = getCommercial4Injoignable(code_, codePostal, status_) # ajout de deux paramètres supplémentaires : code postal, code status
                if infocom != 0:
                    email = infocom.get('email')
                    id_com = infocom.get('ID') 
                    print("99 je supprimer le commercial pardefaut")
                    trouve.pop('commercial')
                    trouve['commercial'] = str(email)  # rechercher un commercial approprie
                    print ("mise à jour injoingable permanent :" + str(updateIdCom4Injoingable(indigo,id_com)))
                    logging.info(str(id_uniq) + " mise à jour injoingable permanent :" + str(updateIdCom4Injoingable(indigo,id_com)))
                    flagta = True
                
            else:
                print ("tsy 99")

            data_retr_code_programme = str(trouve.get("code_programme").replace("0063__", ""))
            data_retr_programme_call = str(trouve.get("programme_call").replace("0063__", ""))
            data_retr_commercial = trouve.get("commercial")

            dataretr = json.dumps(trouve)
            logging.info(str(id_uniq))
            logging.info(dataretr)
            print (dataretr)

            # Si on a un code programme et que le mail du commercial est call-center@edouarddenis.fr
            # alors ne pas continuer et mettre un flag dans 31_RA_EDOUARD_DENIS
            print("# -- " + str(date_p) + " -- Début aiguillage...")
            logging.info("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- Début aiguillage...")

            print("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- " + data_retr_code_programme + " -- " + data_retr_programme_call + " -- " + data_retr_commercial)
            logging.info("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- " + data_retr_code_programme + " -- " + data_retr_programme_call + " -- " + data_retr_commercial)
            detail_a_verifier = ['RDV PHYSIQUE', 'RDV TELEPHONIQUE', 'RDV VISIO', 'ENVOI DE DOCUMENT', 'TRANSFERT ABOUTI', 'TRANSFERT NON ABOUTI', 'NOUS RECONTACTE', 'HORS BUDGET', 'PAS INTERESSE', 'PLUS DE DISP DE LOT', 'LIVRAISON TARDIVE', 'NOUVEAUX PROGRAMMES', 'PROGRAMME CLOTURE', 'SURFACE TROP PETITE', 'APPELS ADMIN', 'NE PARLE PAS FRANCAIS', 'INJOIGNABLE PERMANENT']

            if data_retr_commercial == 'call-center@edouarddenis.fr' and (len(data_retr_code_programme.strip()) > 0 or len(data_retr_programme_call.strip()) > 0) and trouve.get("motif_cloture") in detail_a_verifier:
                print("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- INDICE : " + str(indigo) + " -- MAJ FLAG commercial inapprorié et passer au suivant")
                logging.info("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- INDICE : " + str(indigo) + " -- MAJ FLAG commercial inapprorié et passer au suivant")

                # Mettre à jour le flag flag_no_com et la date date_no_com
                qryFiche = "UPDATE [31_RA_EDOUARD_DENIS] set flag_no_com = 1, date_no_com = GETDATE() WHERE INDICE = {}".format(indigo)
                edouarddenis.execute_crud(qryFiche)
                
                # Continuer à l'itération suivante
                continue

            logging.info("# -- " + str(date_p) + " -- " + str(id_uniq) + " -- Fin aiguillage")
            print("# -- Fin aiguillage")
            # Fin de l'aiguillage

            
            retourta =requests.post(theuRl,data = dataretr, headers=headers).json() 
            time.sleep(2) # attente de 2 s pour le WS
            logging.info(str(id_uniq) + " retour CRM : " + str(retourta))
            print(retourta)

            error = retourta.get('error')
            ecode = error.get('erCode')
            emessage = error.get('erMessage')
            callprojectid_retour = retourta.get('callcenterprojectid')
            
            if ecode is None or emessage is None:
                if not checkReturnCrm(callprojectid_retour, idpros):
                    logging.info(str(id_uniq) + " incompatibilite entre l'entrer(" + str(idpros) + ") et le retour (" + str(callprojectid_retour) +")")
                    continue
                logging.info(str(id_uniq) + " ok entre l'entrer(" + str(idpros) + ") et le retour (" + str(callprojectid_retour) +")")
                print("mise à jour crm ok pour l'indice " +str(idpros))

                factory = retourta.get('factoryprojectid')
                print (factory)
                logging.info(str(id_uniq) + " factory  origine : " + str(initfactory) + " factory retour crm " + str(factory))
                print("factory  origine : " + str(initfactory) + " factory retour crm " + str(factory)) 
                updateFactoryProjectId(idpros, factory,initfactory)
                print ("l'indice : " + str(idpros) ) # +retourta.get('factoryprojectid') + " est update: ok")
                if flagta:
                    updateCompteurCom(id_com,code_)
                    logging.info(str(id_uniq) + " new id_commerciale: " + str(id_com))
                    print('naazo commercial vita update compteur et compteur fake')

                qry = "update [31_RA_EDOUARD_DENIS] set is_sent_crm ='done' , sentCrm_at = convert(varchar, getdate(),120) where indice = {};".format(indigo)
                if  edouarddenis.execute_crud(qry):
                    logging.info(str(id_uniq) + " mise à jour c1: ok ")
                    print('ok')

                else:
                    print('ko')
                    logging.info(str(id_uniq) + " la mise à jour du c1 a échouer")

            else:
                logging.info(str(id_uniq) + " Message "  + str(emessage) + "code erreur : "  + str(ecode))
                print(emessage, ecode)
                continue

        else:
            logging.info(str(id_uniq) + ' pas de correspondance trouve')
        #sys.exit()
    edouarddenis.closeo()