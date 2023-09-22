class ZipRecord(object):
    def __init__(self):

        jPath = "/home/iam/PROD/BANDE_AUDIO/EDOUARD_DENIS/dependance/fields-param-record.json"

        self.jData = None
        with open(jPath) as jHandle:
            self.jData = json.load(jHandle)

    def CreateXmlFile(self, file_path):
        retHandle = open(file_path, "wt")
        return retHandle

    def CloseXmlFile(self, retHandle):
        retHandle.close()

    def WriteXmlFile(self, retHandle, sTexte):
        retHandle.write(sTexte)

    def CreateEasyPath(self, sEasyCode):
        pathret = "./%s" % (sEasyCode)
        try:
            os.mkdir(pathret)
        except:
            pass

        pathret += "/Audio"
        try:
            os.mkdir(pathret)
        except:
            pass

    def CopyXsl(self, sEasyCode):
        shutil.copyfile("/home/iam/PROD/BANDE_AUDIO/EDOUARD_DENIS/dependance/record.xsl",
                        "./%s/record.xsl" % (sEasyCode))

    def GenerateRecordName(self):
        ret = "record"
        datename = str(datetime.datetime.now()).replace(":", "")
        print(datename)

        #        print ("gsdfgsg")
        ret += "-" + str(datename).lower()
        return ret

    def GetDataByEasycode(self, sEasyCode, campaign, tab_rec):
        try:
            sQry = """
              select bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
              FROM Record
              where rec_idlink =""" + sEasyCode + """ and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
            """
            print("requete :", sQry + "\n")

            db_rec = RecordDbNow()
            trow_bande = db_rec.openrecordsetOne(sQry)
            db_rec.setNothing()
            print("trouve: ", trow_bande)
            if trow_bande == None:
                sql = """
                  select  bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                  FROM [VIVETIC_BACKUP].dbo.""" + tab_rec + """
                  where rec_idlink='""" + sEasyCode + """' and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                """
                print(sql)

                db_rec_ = RecordDb()
                trow_bande_ = db_rec_.openrecordsetOne(sql)
                db_rec_.setNothing()
                print("trouve backup: ", trow_bande_)
                if trow_bande_ == None:
                    sqlgetindicedeb = """select indice_debut FROM [PROD_EDOUARD].[dbo].[31_RA_EDOUARD_DENIS] where indice =""" + sEasyCode
                    print("indice debut :", sqlgetindicedeb)

                    db = EasyDb()
                    tindicedeb = db.openrecordsetOne(sqlgetindicedeb)

                    sQry = """
                      select bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                      FROM Record
                      where rec_idlink =""" + tindicedeb["indice_debut"] + """ and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                    """
                    db_rec = RecordDbNow()
                    trow_bande_deb = db_rec.openrecordsetOne(sQry)
                    db_rec.setNothing()

                    print("trouve debut: ", trow_bande_deb)
                    if trow_bande_deb == None:
                        sql = """
                          select  bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                          FROM [VIVETIC_BACKUP].dbo.""" + tab_rec + """
                          where rec_idlink='""" + tindicedeb["indice_debut"] + """' and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                        """
                        print(sql)

                        db_rec_ = RecordDb()
                        trow_bande_deb_ = db_rec_.openrecordsetOne(sql)
                        db_rec_.setNothing()
                        print("trouve debut backup", trow_bande_deb_)
                        if trow_bande_deb_ == None:
                            bande = ''
                        else:
                            bande = trow_bande_deb_['bande']
                    else:
                        bande = trow_bande_deb["bande"]
                else:
                    bande = trow_bande_["bande"]
            else:
                bande = trow_bande["bande"]
            bande = bande.replace("D:/HNETRecords/hermes_p/Files/354663A57736D434/RECORDS", "//51.255.66.238/STORAGE")
            print("Bande :", bande)
            return bande
        except Exception as e:
            try:
                sQry = """
                  select bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                  FROM Record
                  where rec_idlink =""" + sEasyCode + """ and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                """
                print("requete :", sQry + "\n")
                db_rec = RecordDbNow()
                trow_bande = db_rec.openrecordsetOne(sQry)
                db_rec.setNothing()
                print("trouve: ", trow_bande)
                if trow_bande == None:
                    sql = """
                      select  bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                      FROM [VIVETIC_BACKUP].dbo.""" + tab_rec + """
                      where rec_idlink='""" + sEasyCode + """' and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                    """
                    print(sql)

                    db_rec_ = RecordDb()
                    trow_bande_ = db_rec_.openrecordsetOne(sql)
                    db_rec_.setNothing()
                    print("trouve backup: ", trow_bande_)
                    if trow_bande_ == None:
                        sqlgetindicedeb = """select indice_debut FROM [PROD_EDOUARD].[dbo].[31_RA_EDOUARD_DENIS] where indice =""" + sEasyCode
                        db = EasyDb()
                        tindicedeb = db.openrecordsetOne(sqlgetindicedeb)
                        print("indice debut:", tindicedeb)
                        sQry = """
                          select bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                          FROM Record
                          where rec_idlink =""" + tindicedeb["indice_debut"] + """ and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                        """
                        db_rec = RecordDbNow()
                        trow_bande_deb = db_rec.openrecordsetOne(sQry)
                        db_rec.setNothing()

                        print("trouve debut: ", trow_bande_deb)
                        if trow_bande_deb == None:
                            sql = """
                              select  bande from (SELECT replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')  as bande,max(Rec_Time) as temps
                              FROM [VIVETIC_BACKUP].dbo.""" + tab_rec + """
                              where rec_idlink='""" + tindicedeb[
                                "indice_debut"] + """' and rec_campid in """ + campaign + """ group by replace('https:'+replace(replace([Rec_Filename],'192.168.134.8\d$\hermes_p\Files\\354663A57736D434\RECORDS','51.255.66.238\STORAGE'),'\\','/'),'#','%23')) as t
                            """
                            print(sql)

                            db_rec_ = RecordDb()
                            trow_bande_deb_ = db_rec_.openrecordsetOne(sql)
                            db_rec_.setNothing()
                            print("trouve debut backup", trow_bande_deb_)
                            if trow_bande_deb_ == None:
                                bande = ''
                            else:
                                bande = trow_bande_deb_['bande']
                        else:
                            bande = trow_bande_deb["bande"]
                    else:
                        bande = trow_bande_["bande"]
                else:
                    bande = trow_bande["bande"]
                bande = bande.replace("D:/HNETRecords/hermes_p/Files/354663A57736D434/RECORDS",
                                      "//51.255.66.238/STORAGE")
                print("Bande :", bande)
                return bande

            except Exception as e:
                print(str(e))
                #                self.envoi_mail_serveur(str(e))
                return False

    def dowload_file(self, file_url, namefile):
        try:
            # if True:
            print("download start " + file_url)
            r = requests.get(file_url, stream=True, verify=False)

            if int(r.headers["Content-Length"]) == 0:
                return False

            print("download encours " + file_url)
            with open(namefile, "wb") as wav:
                for chunk in r.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        wav.write(chunk)

            wav.close()
            print("download end " + file_url)
            return True
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            return False

    def CreateRecordingByLink(self, myurl, record_filename):
        print("record filename :", record_filename)
        ret = False
        mydatfile = None
        print("URL:", myurl)

        try:
            myContext = ssl._create_unverified_context()
            mydatfile = urlopen(myurl, context=myContext)
        except:
            pass
        print("mydatfile:", mydatfile)

        if mydatfile != None:
            with open(record_filename, 'wb') as output:
                output.write(mydatfile.read())
            ret = True

        return ret

    def ZipAdirectory(self, dir_name):
        ret = ""
        output_filename = self.GenerateRecordName()
        shutil.make_archive(output_filename, 'zip', dir_name)
        if shutil.os.access(output_filename + ".zip", os.F_OK):
            ret = output_filename + ".zip"

        return ret

    def CreateZipRecord(self, sEasyCode, lastcamcampaign, campaign, tab_rec, dir_dossier=""):
        print("debut creation zip")
        self.CreateEasyPath(sEasyCode)
        self.CopyXsl(sEasyCode)
        db_prod = ProdDb()
        NameFile = ""
        Bande = self.GetDataByEasycode(str(sEasyCode), str(lastcamcampaign), tab_rec)
        if Bande != '' and Bande != None and Bande != False:
            tNameFile = Bande.split("/")
            nb = len(tNameFile)
            NameFile = tNameFile[nb - 1]
            print("nom:", NameFile)
            """
            fname_save = ".\\" + str(sEasyCode) + "\\Audio\\" + rsRow["fname"]
            """
            fname_save = r"./" + str(sEasyCode) + "/Audio/" + NameFile

            print("fname : ", fname_save)

            if self.CreateRecordingByLink(Bande, fname_save) == True:
                """
                createdZip = self.ZipAdirectory(".\\%s" % (sEasyCode))
                """

                createdZip = self.ZipAdirectory("./%s" % (sEasyCode))
                print("createdZip : ", createdZip)

                if createdZip != "":
                    """
                    shutil.copyfile(createdZip, dir_dossier + "\\" + str(sEasyCode) + ".zip")
                    """
                    shutil.copyfile(createdZip, dir_dossier + "/" + str(sEasyCode) + ".zip")
                """
                shutil.rmtree(".\\%s" % (sEasyCode))
                """
                shutil.rmtree("./%s" % (sEasyCode))

                print("fin zip")
            else:
                print("Audio introuvable")
                req = " update call_recording_edouard_denis set flag_down = 'R' where indice = '%s' and campaign = '%s'  " % (
                str(sEasyCode), campaign)
                print("req :", req)
                db_prod.runSql(req)
                NameFile = ""


        elif (Bande == False):
            req = " update call_recording_edouard_denis set flag_down = 'R' where indice = '%s' and campaign = '%s'  " % (
            str(sEasyCode), campaign)
            print("req :", req)
            db_prod.runSql(req)
        else:
            req = " update call_recording_edouard_denis set flag_down = 'I' where indice = '%s' and campaign = '%s'  " % (
            str(sEasyCode), campaign)
            print("req :", req)
            db_prod.runSql(req)
        #            self.envoi_mail_introuvable(str(sEasyCode))

        return NameFile

    def envoi_mail_introuvable(self, easycode):
        try:
            print("debut envoie mail")
            mailBody = """
               <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
               <html>
               <head>
                 <title></title>
                 <meta content="fr" http-equiv="Content-Language" />
                 <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
               </head>
               <body style="font-size:12px; color: #333333; font-family: Century Gothic, sans-serif;">
                 <div><img src="cid:logo"></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>Bonjour</div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div> 
                 <div><b>L\'audio avec indice : %s est introuvable</b></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>Cordialement,</div>
                 <div>--&nbsp;</div>
                 <div><b>L\'équipe  %s de VIVETIC</b></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div><img src="cid:logo"></div>
               </body>
               </html>

               """ % (easycode, "CAMBIUM")

            # Define these once; use them twice!
            strFrom = 'doNotReply@vivetic.mg'
            strTo = ["encadrants_as@vivetic.mg"]
            strCC = ["infodev@vivetic.mg"]

            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = 'CAMBIUM : AUDIO INTROUVABLE'
            msgRoot['From'] = strFrom
            msgRoot['To'] = ",".join(strTo)
            msgRoot['CC'] = ",".join(strCC)

            msgRoot['Date'] = formatdate(localtime=True)
            msgText = MIMEText(mailBody, 'html', _charset='utf-8')

            msgRoot.attach(msgText)

            fp = open('logo.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            msgImage.add_header('Content-ID', '<logo>')
            msgRoot.attach(msgImage)

            import smtplib
            smtp = smtplib.SMTP()
            smtp.connect('mx1.vivetic.mg')
            smtp.login('doNotReply@vivetic.mg', 'Admin2013')
            smtp.sendmail(strFrom, strTo + strCC, msgRoot.as_string())
            print("ok maail")
            smtp.quit()
        except Exception as e:
            print(str(e))

    def envoi_mail_serveur(self, error):
        try:
            print("debut envoie mail")
            mailBody = """
               <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
               <html>
               <head>
                 <title></title>
                 <meta content="fr" http-equiv="Content-Language" />
                 <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
               </head>
               <body style="font-size:12px; color: #333333; font-family: Century Gothic, sans-serif;">
                 <div><img src="cid:logo"></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>Bonjour</div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div> 
                 <div><b>Coupure serveur OVH  erreur : %s</b></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div>Cordialement,</div>
                 <div>--&nbsp;</div>
                 <div><b>L\'équipe  %s de VIVETIC</b></div>
                 <div>&nbsp;</div>
                 <div>&nbsp;</div>
                 <div><img src="cid:logo"></div>
               </body>
               </html>

               """ % (error, "CAMBIUM")

            # Define these once; use them twice!
            strFrom = 'doNotReply@vivetic.mg'
            strTo = ["reseaux.systemes@vivetic.mg"]
            strCC = ["infodev@vivetic.mg"]

            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = 'CAMBIUM : AUDIO INTROUVABLE'
            msgRoot['From'] = strFrom
            msgRoot['To'] = ",".join(strTo)
            msgRoot['CC'] = ",".join(strCC)

            msgRoot['Date'] = formatdate(localtime=True)
            msgText = MIMEText(mailBody, 'html', _charset='utf-8')

            msgRoot.attach(msgText)

            fp = open('logo.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            msgImage.add_header('Content-ID', '<logo>')
            msgRoot.attach(msgImage)

            import smtplib
            smtp = smtplib.SMTP()
            smtp.connect('mx1.vivetic.mg')
            smtp.login('doNotReply@vivetic.mg', 'Admin2013')
            smtp.sendmail(strFrom, strTo + strCC, msgRoot.as_string())
            print("ok maail")
            smtp.quit()
        except Exception as e:
            print(str(e))