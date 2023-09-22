import unittest, time, re
import datetime
import time
import psycopg2
import psycopg2.extras
import glob
import os
import sys
import re
import psutil
from xml.dom import minidom
import pysftp

import zipfile
import shutil
import json
import base64
import pymssql
import requests 
from urllib.request import urlopen

#import urllib2
import ssl
import unidecode
import string

import email
import databases.ProdDb as ProdDb
import databases.EasyDb as EasyDb
import ZipRecord

fichierlog = open("logs/" + os.path.basename(__file__) + ".log", "a")
lockFile = '/var/tmp/' + os.path.basename(__file__) + '.lock'

class Traitement():
    ###############################################################
    def set_error(self, num_err, val_err):
        self.error = num_err
        self.msg_error = val_err
        print("\n\n*********" + val_err + "******************\n")
    ###############################################################
    def process_xml(self):
        sms = "Debut lecture xml"
        print(sms)
        if self.error > 0:
            return
        # try:
        if True:
            print(self.dir_zip + "record.xml")
            xdoc = minidom.parse(self.dir_zip + "record.xml")
            data_list = xdoc.getElementsByTagName("XmlData")
            s_wav_name = []
            print("data liste:", data_list)
            for data in data_list:
                print("data", data)
                for field in data.childNodes:
                    print("fields", field)
                    if field.nodeName == "audioList":
                        aud = field.getElementsByTagName("audio")
                        print("audio", aud)
                        for name in aud:
                            print("nom:", name)
                            s_wav_name.append(name.firstChild.nodeValue)

            sms = "Fin lecture xml"
            print(sms)
            return s_wav_name

    #        except:
    #            self.set_error(9,"Erreur, probleme exploitation du fichier xml record" )
    ###############################################################
    def insertionProd(self, data):
        try:
            db_prod = ProdDb()
            # Insere la ligne si rien n'est trouver pour la campagne : self.campaing et l'indice : seasycode
            sql = """
                INSERT INTO call_recording_edouard_denis
                (indice, indice_debut, campaign, agent, date_call, statut, telephone, tel_mobile,
                tel_fixe, tel_professionnel, id_commercial, nom_commercial, prenom_commercial, date_rdv,
                heure_rdv, type_rdv, nom_client, prenom_client)
            SELECT '%(seasycode)s', '%(indice_debut)s', '%(campaign)s', '%(sagent)s', '%(sdate_of_call)s', '%(stypecall)s',
                '%(stel_appele)s', '%(stel_mobile)s', '%(stel_fixe)s', '%(stel_professionnel)s', '%(sid_commercial)s',
                '%(snom_commercial)s', '%(sprenom_commercial)s', '%(sdate_rdv)s', '%(sheure_rdv)s', '%(stype_rdv)s',
                '%(snom_client)s', '%(sprenom_client)s'
            WHERE NOT EXISTS (
                SELECT indice, indice_debut, campaign, agent, date_call, statut, telephone, tel_mobile, tel_fixe,
                    tel_professionnel, id_commercial, nom_commercial, prenom_commercial, date_rdv, heure_rdv,
                    type_rdv, nom_client, prenom_client
                FROM call_recording_edouard_denis
                WHERE indice = '%(seasycode)s' AND campaign = '%(campaign)s'
            )
            """ % data

            db_prod.runSql(sql)
            #            print "eto"
            db_prod.setNothing()
        #            print "eto2"
        except Exception as e:
            self.set_error(8, "Erreur, probleme pendant l'insertion dans la table prod")
            sms = "Erreur de telechargement \n" + str(e) + "\n"
            fichierlog.write(sms)
            self.erreur = True
    ###############################################################
    def clear_directories(self):
        try:
            folder = self.dir_zip
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            folder = self.dir_save
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except:
            pass

    ###############################################################
    def get_down_file(self, easycode, files):
        # On télécharge
        sms = "Debut telechargement"
        print(sms)
        if self.error > 0:
            return

        time.sleep(10)
        try:
            # On récupère le dossier zip
            stemp_file = ""
            print("Get zip")
            # Associe un repertoire a l'objet
            os.chdir(self.dir_temp)
            # On boucle sur tout les archives dans le dossier
            for ifile in glob.glob("*.zip"):
                # On écrase l'archive temporaire a chaque itération.
                stemp_file = ifile
                # On récupère donc la dernière archive

            if stemp_file != "":
                # Si la valeur de stemp_file n'est pas une chaine vide, alors c'est que l'on a trouver une archive
                # On déplace l'archive du répertoire temporaire vers le répertoire de sauvegarde
                shutil.move(self.dir_temp + stemp_file, self.dir_save + stemp_file)
                print("supression")
                myreal_path = self.dir_save + stemp_file
                # On ouvre le fichier en mode lecture binaire
                fh = open(myreal_path, 'rb')
                # On créer un objet ZipFile qui pointe sur le fichier binaire
                zip = zipfile.ZipFile(fh)
                # On extrait les documents de l'archive
                for fname in zip.namelist():
                    zip.extract(fname, self.dir_zip)

                fh.close()
                self.easycode_now = easycode
                easycd = self.easycode_now

                db_prod = ProdDb()
                
                renamed = self.renamed
                req = """ select 
                            nom_client,prenom_client,date_call::varchar
                          from 
                            call_recording_edouard_denis 
                          where 
                            indice = '%s' and campaign ='%s' 
                          order by date_call desc
                    """ % (easycd, self.campaign)
                    
                print(req)
                # On exécute la requête
                tnamed = db_prod.openrecordset(req)
                # print tnamed
                # print renamed
                # Si la première colonne de la première ligne n'est pas nulle
                if tnamed[0][0] != None and tnamed[0][0] != '':
                    renamed = str(renamed) + str(tnamed[0][0].strip().replace(' ', '-').replace('/', '-')) + "_"
                if tnamed[0][1] != None and tnamed[0][1] != '':
                    renamed = str(renamed) + str(tnamed[0][1].strip().replace(' ', '-').replace('/', '-')) + "_"
                renamed = str(renamed) + str(
                    tnamed[0][2].strip().replace('-', '').replace('/', '-').replace(' ', '_').replace(':', '')) + ".mp3"

                print("nom MP3: ", renamed)
                
                command = "/usr/bin/ffmpeg -y -threads 8 "
                comm = " -filter_complex  '"
                i = 0
                print("Renommage")
                os.chdir(self.dir_zip)
                # for file in s_wav_name:
                files = "Audio/" + files
                print("file : ", files)
                command += " -i " + str(files).replace("\\", "\\\\") + " "
                print("command : ", command)
                comm += "[" + str(i) + ":0]"
                i = i + 1
                print("comm : ", comm)

                com = "concat=n=" + str(i) + ":v=0:a=1[out]' -map '[out]' -b:a 32k '../RECORD/" + str(renamed) + "'"
                print("com : ", com)

                print("translation")
                print("avant translation")

                os.system(command + comm + com)
                print("apres translation ")
                req = " update call_recording_edouard_denis set flag_down='O',nom_fichier_mp3='%s' where indice = '%s' and campaign = '%s'  " % (
                renamed, easycd, self.campaign)
                print("req :", req)
                db_prod.runSql(req)
                print("update")
                self.clear_directories()
                db_prod.setNothing()
                print("traitement termine")
        except Exception as e:
            self.set_error(8, "Erreur, probleme pendant le telechargement du fichier")
            sms = "Erreur de telechargement \n" + str(e) + "\n"
            print("erreur :", sms)
            fichierlog.write(sms)
            self.erreur = True
            db_prod.setNothing()
    ###############################################################
    def connect(self):
        myHostname = "164.132.164.34"
        myUsername = "vivetic"
        myPassword = "cqZ44*r7AZYhK9n^#L%93z"
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sms = "sms"
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, port=22,
                                   cnopts=cnopts) as sftp:
            sms = "connection succesfully"
            sftp = pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, port=22,
                                         cnopts=cnopts)
        print(sms)
        return sftp
    ###############################################################
    def get_file_to_send():
        print('debut envoie ftp')
        db_prod = ProdDb()
        flag_traitement = False
        req_name_file = " select nom_fichier_mp3 from call_recording_edouard_denis where campaign ='%s' and flag_up='N' and flag_down='O' order by date_call asc" % (self.campaign)
        print(req_name_file)
        name_file = db_prod.openrecordset(req_name_file)
        print(name_file)
        db_prod.setNothing()
        return name_file


    def envoi_ftp(self):
        files_to_send = self.get_file_to_send()
        try:
            sftp = self.connect()
        except:
            # TODO tenter une deuxieme fois la connexion
            sms = "Erreur de connexion ftp :\n" + str(e) + "\n"
            print(sms)
            fichierlog.write(sms)
            self.erreur = True
            os.remove(lockFile)
        self.nbr_envoi = 0
        
        return self.send_files(sftp,files_to_send)
    
    def send_files(self,sftp,files_to_send):
        if len(files_to_send) == 0:
            # TODO Traiter l'erreur
            flag_traitement = True
            raise FileNotFoundError("Aucun element a envoye sur ftp")
            
        for file_to_send in files_to_send:
            self.send_file(sftp,file_to_send[0])
            # db_prod.setNothing()
            sms = "Nombre fichier envoyé sur ftp : " + str(self.nbr_envoi) + "\n"
            print(sms)
        return flag_traitement
        
    def send_file(self,sftp,file):
        try:
            print(" *****************  ************")
            db_prod = ProdDb()
            print('nom fichier : ', file)
            os.chdir(self.dir_record)

            file = open(file, 'r')

            sftp.cwd(self.dir_fichier_client)
            sftp.put(self.dir_record + file, self.dir_fichier_client + file)
            file.close()
            print('envoi ftp de ', file, ' avec succes')
            req_updt = " update call_recording_edouard_denis set flag_up = 'O', date_envoie ='%s' where campaign ='%s' and nom_fichier_mp3='%s' " % (
            self.dateEnvoie, self.campaign, file)
            db_prod.runSql(req_updt)
            self.nbr_envoi += 1
            db_prod.setNothing()
        except Exception as e:
            sms = "Erreur d'envoie du fichier :" + str(file) + "\n" + str(e) + "\n"
            print(sms)
            self.erreur = True

    ###############################################################
    def couper_livre(self):
        db_prod = ProdDb()
        req_name_file = " select nom_fichier_mp3 from call_recording_edouard_denis where campaign ='%s' and flag_up='O' and flag_down='O' and date_envoie='%s'" % (
        self.campaign, self.dateEnvoie)
        name_file = db_prod.openrecordset(req_name_file)
        print(name_file)

        for fic in name_file:
            fichier = fic[0]
            try:
                print('deplacement de ' + str(fichier))
                shutil.move(self.dir_record + fichier, self.dir_backup + fichier)
            except:
                print("deplacement echoue de " + str(fichier))
        print("fin deplacement")
        db_prod.setNothing()
    ###############################################################
    def suppression_zip(self):

        print("suppression zip")
        bok = True
        #        os.chdir(self.currentDir)

        tzip = glob.glob(self.currentDir + "/*.zip")
        if len(tzip) > 0:
            for zip in tzip:
                os.remove(zip)
        print("fin suppression zip")

    ###############################################################
    def init_var(self):
        self.campaign = "EDOUARD DENIS"
        self.lastcampaign = "('31_RA_EDOUARD_DENIS','EDOUARD_DENIS','0971','31_FORMULAIRE_ED','31_RA_EDOUARD_DENIS_OLD','PREPROD_EDOUARD','2426','8270')"
        self.table = "[PROD_EDOUARD].[dbo].[vw_edouarddenis]"
        self.table_prod = "[DB_PROGRAMME].[dbo].[ODcallsReto]"
        self.renamed = ""
        self.currentDir = "/home/iam/PROD/BANDE_AUDIO/EDOUARD_DENIS"
        self.dir_temp = self.currentDir + "/TEMP/"
        self.dir_save = self.currentDir + "/SAVE/"
        self.dir_zip = self.currentDir + "/UNZIP/"
        self.dir_record = self.currentDir + "/RECORD/"
        self.dir_backup = self.currentDir + "/FICHIERS LIVRES/"
        self.dir_fichier_client = "/inbox/"

































    def verify_lockfile_doesnot_exist(lockFile):
        if os.path.exists(lockFile):
            print("Fin traitement")
            logTraitement += "************Fin traitement************\n"
            logTraitement = logTraitement.encode("utf8")
            fichierlog.write(str(logTraitement))
            raise FileExistsError("")
        
    def get_current_date():
        if len(sys.argv) > 1:
            dateEnvoie = sys.argv[1]
                # self.dateEnvoie = self.dateEnvoie.replace('-','')
        else:
                    # sinon on créer une date
            dateEnvoie = time.strftime("%Y-%m-%d")
        return dateEnvoie
    
    def get_date(self,tcall):
        # Si une seule ligne a été trouver
        if len(tcall) == 0:
            # Récupère un argument passer dans le cmd a la commande executant se script.
            # Cet argument semble correspondre a une date d'éxecution.
            self.dateEnvoie = self.get_current_date()
            logTraitement += "date : " + str(self.dateEnvoie) + "\n"
            print(logTraitement)
            # dateE = self.dateEnvoie + '%'
            self.unpack_tb()               
        else:
            # pour chaque appel
            for rowcall in tcall:
                print("************BEGIN************\n")
                self.dateEnvoie = rowcall['date_call']
                logTraitement = "date : " + str(self.dateEnvoie) + "\n"
                print(logTraitement)
                dateE = str(self.dateEnvoie)[0:10] + '%'
                self.unpack_tb()
    ###############################################################
    def remove_lock_file():
        if os.path.exists(lockFile) == True:
            print("true")
            os.remove(lockFile)
        else:
            print("false")
    ###############################################################
    def __init__(self):
        try:
            logTraitement = "************BEGIN************\n"
            print(logTraitement)
            self.verify_lockfile_doesnot_exist(lockFile)
            fichierlock = open(lockFile, 'w')
            fichierlock.close()
            self.init_var()
            # Selectionne toutes les dates d'appels unique dans la bd
            tcall = self.select_unique_calls()
            self.get_date(tcall)
            self.remove_lock_file()
            print("Fin traitement")
            logTraitement += "************Fin traitement************\n"
            logTraitement = logTraitement.encode("utf8")
            fichierlog.write(str(logTraitement))
        except Exception as inst:
            logTraitement = '*******************' + time.strftime("%Y-%m-%d") + '*******************' + '\n'
            logTraitement += 'type ERREUR:' + str(type(inst)) + '\n'
            logTraitement += 'CONTENU:' + str(inst) + '\n'
            logTraitement = logTraitement.encode("utf8")
            fichierlog.write(str(logTraitement))
            fichierlog.close()
            if os.path.exists(lockFile) == True:
                os.remove(lockFile)




    ###############################################################
    def unpack_tb(self):
        dateDeb = str(self.dateEnvoie)[0:8] + '01'
        dateFin = str(self.dateEnvoie)
        sQl = select_od(self.table, self.table_prod, dateDeb, dateFin, self.lastcampaign)
        print(sQl)
        logTraitement += sQl + "\n"

        sQli = """SELECT indice from call_recording_edouard_denis where flag_down = 'N' and campaign = '%s'""" % (self.campaign)
        db = ProdDb()
        self.getdown_files(geteasyCode(),filter_all_indice(db.openrecordset(sQli)))



    ###############################################################
    def getdown_files(self,teasycode,tindice):
        c = ZipRecord()
        logTraitement += "Traitement par easycode : \n"
        for roweasycode in teasycode:
            self.error = 0
            print("indice :", roweasycode['indice'])
            if str(roweasycode['indice']) not in tindice:
                return
            dictionnary = transform_to_dictionnary(roweasycode)
            self.insert_dictionnary(dictionnary)
            audio = c.CreateZipRecord(dictionnary['seasycode'],self.lastcampaign,self.campaign,tab_rec,self.dir_temp)
            print("audio :" +  audio)
            logTraitement += "  Fin traitement zip\n"
            print("erreur :" + self.error + " \n Fin traitement zip\n")
            if audio != "":
                logTraitement += "  Debut telechargment\n"
                self.get_down_file(dictionnary['seasycode'], audio)
                logTraitement += "  Fin telechargement\n"
                self.suppression_zip()
            logTraitement += "Fin traitement par easycode\n"
    
    def insert_dictionnary(self,dictionnary):
        print_dictionnary(dictionnary)
        tab_rec = "Record_" + str(dictionnary['sdate_of_call'])[0:4] + "_" + str(dictionnary['sdate_of_call'])[5:7]
        print("table record :", tab_rec + "\n")
        logTraitement += " ** Indice : " + str(dictionnary['seasycode']) + " **\n"
        logTraitement += "  Insertion dans la table prod\n"
        # print ("eto fgsf?")
        self.insertionProd(dictionnary)
        logTraitement += "  Fin insertion dans la table prod\n Traitement zip\n"
    

            
    ###############################################################
    def select_unique_calls(self):
        sQli = """
                    SELECT 
                        distinct date_call 
                    from 
                        call_recording_edouard_denis 
                    where 
                        (flag_down = 'N') and campaign = '%s' order by date_call
                """ % (self.campaign)
        print(sQli)
        db = ProdDb()
        return db.openrecordset(sQli)

###############################################################
def transform_to_dictionnary(tab):
    return {
        'seasycode': tab['indice'],
        'indice_debut': tab['indice_debut'],
        'sagent': tab['LastAgent'],
        'sdate_of_call': tab['CallLocalTime'],
        'stypecall': tab['lib_status'],
        'stel_appele': tab['ANI'],
        'stel_mobile': tab['tel_mobile'],
        'stel_fixe': tab['tel_fixe'],
        'stel_professionnel': tab['tel_professionnel'],
        'sdate_rdv': tab['date_rdv'],
        'sheure_rdv': tab['heure_rdv'],
        'stype_rdv': tab['type_rdv'],
        'snom_client': tab['nom_client'],
        'sprenom_client': tab['prenom_client'],
        'snom_commercial': tab['nom_commercial'],
        'sprenom_commercial': tab['prenom_commercial'],
        'sid_commercial': tab['id_commercial']
    }
###############################################################
def geteasyCode():
    db = EasyDb()
    teasycode = db.openrecordset(sQl)
    print("nombre : ", len(teasycode))
    if len(teasycode) == 0:
        logTraitement += "Pas d'enregistrement"
        logTraitement = logTraitement.encode("utf8")
        fichierlog.write(logTraitement + "\n")
        if os.path.exists(lockFile) == True:
            os.remove(lockFile)
        sys.exit(0)
    print("eto")
    return teasycode






###############################################################
def filter_all_indice(tid):
    tindice = []
    for rowid in tid:
        tindice.append(rowid['indice'])
    print(tindice)
    return tindice




###############################################################
def print_dictionnary(dictionnary):
    for key in dictionnary.keys():
        print(key + " : " + dictionnary[key])



###############################################################
def select_od(*args):
    """
    SELECT 
        od.indice,tb.indice_debut,od.LastAgent, od.CallLocalTime, 
        od.CallStatusNum, od.ANI,tb.tel_mobile,tb.tel_fixe,
        tb.tel_professionnel, tb.date_rdv,tb.heure_rdv,tb.lib_status,
        tb.lib_detail as type_rdv,tb.nom as nom_client,tb.prenom as prenom_client,
        vw.nom as nom_commercial,vw.prenom as prenom_commercial,tb.id_commercial 
    from 
        %s tb 
    INNER JOIN 
        [PROD_EDOUARD].[dbo].[oe_commerciaux] vw    
    ON 
        convert(varchar,tb.id_commercial) = convert(varchar,vw.id)
    INNER JOIN 
        %s od 
    ON 
        tb.indice = od.indice 
    where 
        convert(varchar,CallLocalTime, 23)>='%s' 
        and od.LastAgent != 0
        and convert(varchar,CallLocalTime, 23) <= '%s'  
        and ((tb.lib_status = 'ACCORD' and tb.lib_detail not in ('ENVOI DE DOCUMENT','HORS CIBLE')) or tb.lib_status = 'REFUS')
        and od.LastCampaign in %s
    """ % (args)