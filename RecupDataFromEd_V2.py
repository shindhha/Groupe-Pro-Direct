
#! /usr/bin/env python
# -*- coding: utf8
import requests
import json
import datetime, sys, os,logging
# Thierry 20200217 : Pour utilisation d'expression reguliere
import re
from datetime import date, timedelta,datetime
from RaycnxDict import Raycnx
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import glob

daty = str(date.today())
date_p= datetime.now()
print(date_p)
#log_name = '//home//user1//programme_python//logs//GetprogrammeCRm_'+ daty.replace('-','') + '.log'
log_name = '//var//log_iscc//GetprogrammeCRm_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("********************************date lancement programme: " + str(date_p) + " ************************")
edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')
theuRl = "https://prd-ed-projet.azurewebsites.net/api/Project/GetProject4CallCenter"
urlAcquit = "https://prd-ed-projet.azurewebsites.net/api/Project/AcquitProject4CallCenter"
headersed = {'apikey': "ED-FACTORY-PROJET*2020",'Content-type': 'application/json'}

headers = {'Content-type': 'application/json'}
mineurl = "https://ws-238.vivetic.com/prod_v1_EdouardDenis/api/EdouardDenis"

# Thierry 20200217 : pattern pour exclusion email se terminant par marketed.fr
regexAExclure = re.compile(r"^.+\@marketed\.fr$")
# Thierry 20210509 : pattern pour exclusion VIGED
regexViged = re.compile(r"62934")

def acquiteproject (factoryid, urlAcquit,headersed,indice = "10x20"):
    acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":indice}
    acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
    error = acquite.get('error')
    codeError = error.get('erCode')
    Message = error.get('erMessage')
    if (Message is None and codeError is None):
        print ("acquitement ok bidon")
        logging.info("acquitement ok bidon pour la  factoryprojectid: " + factoryid)
        logging.info(codeError +': ' + Message)
    else:
        print("acquitement non abouti")
        logging.info("le fake acquitement n'est pas reussi")
        print ('contenu non traitable')
        logging.info(codeError +': ' + Message)
        logging.info("********************contenu non traitable chez nous suivant le cahier de charge*********")
# **********************************************************************************************************a ajouter dans la prod ***********
def transformcle(tel_mobile, tel_fixe, tel_professionnel, email, date_acquisition,code_programme,nom,prenom):
    phone_list = []
    phone_list.append('0'+(''.join([n for n in tel_mobile if n.isdigit()]))[-9:])
    phone_list.append('0'+(''.join([n for n in  tel_fixe if n.isdigit()]))[-9:])
    phone_list.append('0'+(''.join([n for n in tel_professionnel if n.isdigit()]))[-9:])

    tel = '_'.join(list(set(filter(lambda x: len(x) > 5, phone_list))))
    print (tel)
    # THR 20201217 : date YYYY-MM-DD (10) et non YYYY-MM (7)
    date_acquisition = str(date_acquisition).split('T')[0][0:10].replace('-','')
    print (date_acquisition)
    listcl = []
    if email:
        listcl.append(email)
    if nom:
        listcl.append(nom)
    # THR 20201217 : ne pas considerer le prenom
    # if prenom:
       # listcl.append(prenom)
    # THR 20201217 : ne pas considerer le code programme
    # if code_programme:
       # listcl.append(code_programme)
    if tel:
        listcl.append(tel)
    if date_acquisition:
        listcl.append(date_acquisition)
    print (listcl)
    # sys.exit()
    cle="#".join(listcl)
    # Correction clé en supprimant ' et espace - THR20200605
    print(cle)
    logging.info(str(date_p) + " *** " + cle)
    cle = str(cle).lower().replace("'", "").replace(" ", "")
    print(cle)
    logging.info(str(date_p) + " *** CLE POUR DEDOUBLONAGE *** " + cle)
    # Fin correction clé - correction effective apres constat - THR20200605
    return str(cle).lower()
	
#MAJ 20230322 : modification des règles de dédoublonnage 
def transformcle(tel_mobile, tel_fixe, email, date_acquisition) :

	tel_fixe='0'+(''.join([n for n in tel_fixe if n.isdigit()]))[-9:]
	tel_mobile='0'+(''.join([n for n in tel_mobile if n.isdigit()]))[-9:]
	date_acquisition = str(date_acquisition).split('T')[0][0:10].replace('-','')

	rs = {"email" : email,"tel_fixe":tel_fixe,"tel_mobile":tel_mobile,"date_acquisition":date_acquisition}


	if rs["email"]!='':
		cle=rs["email"]+"#"+rs["date_acquisition"][0:10].replace("-","")
		cle2 = cle

	else:
		if rs["tel_mobile"]!='0':
			cle=rs["tel_mobile"]+"#"+rs["date_acquisition"][0:10].replace("-","")
			cle2 = cle

		else:
			if rs["tel_fixe"]!='0':
				cle=rs["tel_fixe"]+"#"+rs["date_acquisition"][0:10].replace("-","")
				cle2 = cle

			else:
				rs["tel_mobile"]='0612345678' 
				cle=rs["tel_mobile"]+"#"+rs["date_acquisition"][0:10].replace("-","")
				cle2 = cle

	cle = str(cle).lower().replace("'", "").replace(" ", "")
	cle2 = str(cle2).lower().replace("'", "").replace(" ", "")
	cle_liste = []
	cle_liste.append(cle)
	cle_liste.append(cle2)
	return cle_liste	
	
    
def stockerRejet(factoryid, motif):
    query = "INSERT INTO rejet_edouarddenis_crm (factoryprojectid, motif) values ('{}', '{}')".format(factoryid,motif)
    edouarddenis.execute_crud(query)
    
# def checkifExist(cle):
    # sql ="SELECT COUNT(*) AS trouve from edouarddenis where cle ='{}'".format(cle)
    # d = edouarddenis.execute_crud(sql, typ='kk')[0]
    # print(d.get('trouve'))
    # if d.get('trouve') > 0:
        # return True
    # return False
#MAJ 20230223 : Dedoublonnage
def checkifExist(cle,cle_):
    sql ="SELECT COUNT(*) AS trouve from edouarddenis where (cle ='{}' or cle='{}')".format(cle,cle_)
    d = edouarddenis.execute_crud(sql, typ='kk')[0]
    print(d.get('trouve'))
    if d.get('trouve') > 0:
        return True
    return False	
#*********************************************************************************************************** fin ajout prod ************************#

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
    # copie = "thierry1804@gmail.com"
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


#injectIt ={}
if True:
    #fichierlock = open('pro.lock','w')
    #fichierlock.close()

    retourta =requests.post(theuRl,headers=headersed).json()
    #print ('retour: ' + retourta)
    try:

        data = json.loads(retourta)
        injectIt = data.get('Operation').get('Set').get('Data')
        #print(injectIt)
    except : # envoi data 2 hermes
        #os.remove('pro.lock')
        print('impossible de continue le traitement parce que le retour est vide')
        sys.exit()
    injectIt['utm_capaign'] = injectIt.pop('utm_campaign')
    data = json.dumps(injectIt)
    logging.info("contenu du fichier recuperer dans le crm : " + data)
    file_name ="//var//log_iscc//edouardJsonfile//"+ injectIt.get('factoryprojectid') + ".txt"

    try:
        print ('sauvegarde du fichier json : ' + file_name)
        with open (file_name,'w') as f:
            json.dump(injectIt,f)
    except e :
        print (e)

    print (injectIt['utm_capaign'])
    #sys.exit()
    factoryid =injectIt.get('factoryprojectid') 
    date_acqui = str(injectIt.get('date_acquisition','T')).split('T')[0].replace('-','').replace(' ','')
    #******************************************************************************************************** goto: new ajout ************************#
    tel_mobile = str(injectIt.get('tel_mobile'))
    tel_fixe = str(injectIt.get('tel_fixe'))
    tel_professionnel = str(injectIt.get('tel_professionnel'))
    email = str(injectIt.get('email'))
    
    date_acquisition = str(injectIt.get('date_acquisition'))
    code_programme = str(injectIt.get('code_programme'))
    nom = str(injectIt.get('nom'))
    prenom = str(injectIt.get('prenom'))
    #cletaka = transformcle(tel_mobile, tel_fixe, tel_professionnel, email, date_acquisition,code_programme,nom,prenom)
    cle = transformcle(tel_mobile,tel_fixe,email,date_acquisition)[0]
    cle2 = transformcle(tel_mobile,tel_fixe,email,date_acquisition)[1]
    logging.info("cle de dedoublonnage : " + cle +"&"+ cle2 )
    
    print(factoryid, date_acqui)
    
    #if checkifExist(cletaka):
        #stockerRejet(factoryid, 'REJET DOUBLONS')
        #sys.exit()
        
    #************************************************************************************************** goto:fin ajout *********************************#
    if injectIt.get('commercial') == 'call-center@edouarddenis.fr' and date_acqui >='20200429' :
        if connecter_site():
            # Thierry 20210509 : Si le code programme contient 62934
            
            # if regexViged.search(str(injectIt.get('code_programme'))):
            #     # Clôturer VIGED
            #     print ("VIGED !")
            #     logging.info("REJET VIGED : " + factoryid)
            #     stockerRejet(factoryid, 'REJET VIGED')
            #     acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid": "10x21", "Conclusioncode": "VIGED"}
            #     acquite = requests.post(urlAcquit, data=json.dumps(acquiteb), headers=headersed).json()
            #     error = acquite.get('error')
            #     codeError = error.get('erCode')
            #     Message = error.get('erMessage')
            #     if (Message is None and codeError is None):
            #         print ("acquitement ok VIGED pour la factoryprojectid: " + factoryid)
            #         logging.info("acquitement ok VIGED pour la factoryprojectid: " + factoryid)
            #     else:
            #         print("le fake acquitement VIGED n'est pas reussi pour " + factoryid)
            #         print(error)
            #         print(codeError)
            #         print(Message)
            #         logging.info("le fake acquitement VIGED n'est pas reussi pour " + factoryid)
            #         logging.info(error)
            #         logging.info(codeError)
            #         logging.info(Message)
            #         sys.exit()

            #     # Envoyer le mail
            #     envoiMail(email)
            #     # Terminer et ne pas continuer
            #     sys.exit()

            # Thierry 20200217 : Si l'email se termine par marketed.fr
            if regexAExclure.search(email):
                print ("REJET MARKETED.FR: " + factoryid)
                logging.info("REJET MARKETED.FR: " + factoryid)
                stockerRejet(factoryid, 'REJET MAIL MARKETED.FR')
                acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
                acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok marketed.fr pour la factoryprojectid: " + factoryid)
                    logging.info("acquitement ok marketed.fr pour la factoryprojectid: " + factoryid)
                else:
                    print("le fake acquitement marketed.fr n'est pas reussi pour " + factoryid)
                    logging.info("le fake acquitement marketed.fr n'est pas reussi pour " + factoryid)
                sys.exit() # Thierry 20210331 : oubli

            # Thierry 20210331 : Email Marine du 30/03/2021 : exclure les fiches comportant les numéros de téléphones suivants : 06 36 20 29 84 et 06 20 98 93 56
            # Thierry 20210401 : Email Emilie du 01/04/2021 : exlure 0652235627
            # Thierry 20210602 : Email Mélina du 01/06/2021 : exclure 06.30.74.61.35
            # Thierry 20210331 : obtenir tous les téléphones, et les nettoyer
            telephones = tel_mobile + "," + tel_fixe + "," + tel_professionnel
            regexNettoyage = r"[^\+\d\,]"
            telephonesNettoyes = re.sub(regexNettoyage, "", telephones, 0, re.MULTILINE)
            # Thierry 20210331 : vérifie si à exclure ou pas
            regexTelAExclure = re.compile(r"636202984|620989356|652235627|630746135")
            if regexTelAExclure.search(telephonesNettoyes):
                print ("REJET 0636202984 ou 0620989356 ou 0652235627: " + factoryid)
                logging.info("REJET 0636202984 ou 0620989356 ou 0652235627: " + factoryid)
                stockerRejet(factoryid, 'REJET 0636202984 ou 0620989356 ou 0652235627')
                acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
                acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok 0636202984 ou 0620989356 ou 0652235627 pour la factoryprojectid: " + factoryid)
                    logging.info("acquitement ok 0636202984 ou 0620989356 ou 0652235627 pour la factoryprojectid: " + factoryid)
                else:
                    print("le fake acquitement 0636202984 ou 0620989356 ou 0652235627 n'est pas reussi pour " + factoryid)
                    logging.info("le fake acquitement 0636202984 ou 0620989356 ou 0652235627 n'est pas reussi pour " + factoryid)
                sys.exit()

            if checkifExist(cle,cle2):
                stockerRejet(factoryid, 'REJET DOUBLONS')

                # acquitement doublons
                acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
                acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok bidon doublons")
                    logging.info("acquitement ok bidon pour la  factoryprojectid: " + factoryid)
                else:
                    print("tsy poinsa ny acquitement")
                    logging.info("le fake acquitement n'est pas reussi")
        
                sys.exit()
            # ajout vérification cle
            injectIt['cle'] = cle
            data = json.dumps(injectIt)
            #sys.exit()
            print (data)
            #sys.exit()
            retour = requests.post(mineurl, data=data, headers = headers).json()
            print(retour)
            print(type(retour))
            #sys.exit()
            if str(retour) == "PhoneNumberError ":
                #********************************************************* une nouvelle ligne *********************************************************#
                stockerRejet(factoryid, 'REJET ERROR TELEPHONE')
                #********************************************************* Fin nouvell ligne **********************************************************#
                print('phone ko')
                #sys.exit()
                acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
                acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok bidon")
                    logging.info("acquitement ok bidon pour la  factoryprojectid: " + factoryid)
                else:
                    print("tsy poinsa ny acquitement")
                    logging.info("le fake acquitement n'est pas reussi")
                    print ('contenu non traitable')
                    logging.info("********************contenu non traitable chez nous suivant le cahier de charge*********")

                sys.exit()






            if retour.get('message') == 'injection success':
 
                RecupIndice = "SELECT max(indice) as indice from [edouarddenis]"
                data = edouarddenis.execute_crud(RecupIndice, typ='kk')
                indis = data[0].get('indice')
                logging.info('indice trouve:' + str(indis))
               
                acquidata = {}
                acquidata["factoryprojectid"] = str(injectIt.get('factoryprojectid'))
                acquidata["callcenterprojectid"] = str(indis)
                #acquidata["conclusioncode"] ="PDS"
                #acquiteproject (factoryid, urlAcquit,headersed
                acquite = requests.post(urlAcquit,data=json.dumps(acquidata), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok production")
                    logging.info("acquitement ok production pour la factoryprojectid : " + str(factoryid) + "portant l'indice :" + str(indis) + " dans hermes")
                else:
                    print("tsy poinsa ny acquitement")
                    logging.info("probleme dans l'acquitement du projet le fichier reus est stocker dans " + str(factoryid) +".txt")
            else:
                print('injection dans edouarddenis ko')
                logging.info("erreur dans notre ws: verifier si un cle est modifier dans ce lui recuper dans le crm")



                acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
                acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
                error = acquite.get('error')
                codeError = error.get('erCode')
                Message = error.get('erMessage')
                if (Message is None and codeError is None):
                    print ("acquitement ok bidon")
                    #************************************************************** here too *****************************************************#
                    stockerRejet(factoryid,'REJET ERROR VOCALCOM')
                    #****************************************** end ***************************#
                    logging.info("acquitement ok bidon pour la  factoryprojectid: " + factoryid)
                else:
                    print("tsy poinsa ny acquitement")
                    logging.info("le fake acquitement n'est pas reussi")
                print ('contenu non traitable')
                logging.info("********************contenu non traitable chez nous suivant le cahier de charge*********")
            edouarddenis.closeo()
        else:
            print("impossible de se connecter a la base PROD_EDOUARD")
            logging.info("impossible de se connecter à la base PROD_EDOUARD")
        
    else:

        acquiteb = {"factoryprojectid": factoryid, "callcenterprojectid":"10x20"}
        acquite = requests.post(urlAcquit,data=json.dumps(acquiteb), headers=headersed).json()
        error = acquite.get('error')
        codeError = error.get('erCode')
        Message = error.get('erMessage')
        if (Message is None and codeError is None):
            print ("acquitement ok bidon")
            logging.info("acquitement ok bidon pour la  factoryprojectid: " + factoryid)
        else:
            print("tsy poinsa ny acquitement")
            logging.info("le fake acquitement n'est pas reussi")
        print ('contenu non traitable')
        #**************************************** filter ko ****************************************#
        stockerRejet(factoryid, 'REJET NON TRAITABLE')
        #*************************************** end of filter *************************************#
        logging.info("********************contenu non traitable chez nous suivant le cahier de charge*********")


    # dans tout les cas il faut acquiter le projet
    
#if os.path.exists('pro.lock') ==True:
    #os.remove('pro.lock')


