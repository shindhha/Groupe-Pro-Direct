#!/usr/bin/env python
# -*- coding: cp1252  -*-

from tracerlogvivetic import tracer
import requests
import json
import pymssql
from e_bdd import ProdDb

import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import sys,os
#reload(sys)
#sys.setdefaultencoding("cp1252")



def send_mail(send_from, send_to, subject, message,server="192.168.10.4", port=25, username='DoNotReply@vivetic.mg', password='Admin2013',use_tls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


def Historise(id, response, message):
    
 
	bdd = ProdDb()
	qryHisto = "Insert Into call_center_histo ( call_center_id,message,response ) Values (%s, '%s','%s') " % (id,str(message).replace("'","''"), str(response).replace("'","''"))
	try:
		bdd.runSql(qryHisto)
	except:
		pass
	
	bdd.setNothing()
	

def FormatData():
	qryErr = "Select * From call_center Where flag=3"
	bdd = ProdDb()
	for rs in bdd.openrecordset(qryErr):
		cop = rs["code_programme"]
		sav_cop = cop
		
	bdd.setNothing() 




		


def sendEdRequest(arrJs):
   
	#sUrl = "https://ws-238.vivetic.com/preprod_edouard/api/EdouardDenis"  #TEST
	sUrl = "https://ws-238.vivetic.com/prod_v1_EdouardDenis/api/EdouardDenis"   #PROD
	headers = {'Content-type': 'application/json'}

	err				= False
	responseText 	= ""
	responseError	= ""
	responseMessage	= ""

	resp = requests.post(sUrl, data=arrJs, headers=headers).json()
	try:
		responseText = str(resp)
	except:
		err	= True

	try:
		responseError = str(resp["error"])
	except:
		err	= True

	try:
		responseMessage = str(resp["message"])
	except:
		err	= True

	return (err, responseText, responseError, responseMessage)	

print("Debut")





fichierlog = open(os.path.basename(__file__).replace(".py","")+datetime.datetime.today().strftime('%Y%m%d')+'.log', 'a')
lock=os.path.basename(__file__)+datetime.datetime.today().strftime('%Y%m%d')+'.lock'


pid=str(os.getpid())
name_application=os.path.basename(__file__)
msgapplication=""
prestation='EAQ'
status="KO"





if os.path.exists(lock)==False:
   
    print(tracer.trace(name_application,"start",msgapplication,"OK",pid,prestation))
    
    fichierlock=open(lock,'w')
    fichierlock.close() 
else:
    #pass
    print(tracer.trace(name_application,"wait",msgapplication,"OK",pid,prestation))
    print(tracer.trace(name_application,"end",msgapplication,"OK",pid,prestation))
    sys.exit(0)    

try:    
#if True:   
    db = ProdDb()
    
    
    #try:
    con = pymssql.connect('5.196.127.163','read_write','0wY!3M8cQ#Kw','PROD_EDOUARD')
    curseur=con.cursor(as_dict=True)
    print ("Connection etabli avec succes")
#    except Exception as e: #pymssql.DatabaseError, e:
#        print ("Impossible de se connecter a %s voici les detail: %s"%('5.196.127.163',e))
#        msgs=datetime.datetime.today().strftime('%Y%m%d %H:%M:%S')+'\n'
#        msgs+="Error: Impossible de se connecter a %s voici les detail: %s"%('5.196.127.163',e)
#        fichierlog.write(msgs + '\n')
#        fichierlog.close() 
#        if os.path.exists(lock)==True:
#            os.remove(lock)
#        
#        sys.exit(0)
    
    


    sQry = """
        Select 
            case when flag_type=2 then trim(code_postal) else '' end code_postal
            ,trim(adresse) adresse
            ,''::text adresse2
            ,case when flag_type=2 then  trim(ville) else '' end ville
            ,trim(mail) email
            ,''::text email2
            ,trim(prenom_client) prenom
            ,trim(nom_client) nom
            ,trim(tel_mobile) tel_mobile
            ,trim(telephone) tel_fixe
            ,''::text tel_professionnel
            ,CASE WHEN civilite ='MME' then 'Madame' WHEN civilite ='M' THEN 'Monsieur' WHEN civilite ='MLLE' THEN 'Mademoiselle' ELSE civilite END salutation
            ,'' situation_logement
        
            ,'' objectif_achat
        
            ,REPLACE(TRIM(SUBSTRING(date_envoi_mail FROM POSITION(',' IN date_envoi_mail)+1 FOR  (POSITION('+' IN date_envoi_mail)-1) - (POSITION(',' IN date_envoi_mail)+1)+1))::timestamp without time zone::text,' ','T') date_acquisition
            ,trim(code_programme) code_programme
        
            ,'' projet_client
        
            ,trim(destination) projet_immo		
        
            ,trim(commentaire) commentaire
            ,trim(budget) budget_max
            ,trim(heure_rappel) horaire_rappel
            ,trim(utm_campaign) utm_capaign
            ,'CC006'::text canal
            ,trim(action) utm_act
            ,trim(utm_source) utm_source
            ,trim(utm_medium) utm_medium
            ,''::text factoryprojectid
            ,''::text imposition
            ,''::text date_naissance
            ,''::text profession
            ,''::text nom_formulaire
            ,trim(projet) type_logement
            ,surface::text surface_logement
            ,trim(taille_logement) taille_logement
            ,''::text budget_fourchette
            ,''::text code_lot
            ,''::text dept_rech
            ,''::text ville_rech
            ,''::text primo_accedant
            ,trim(rgpd) rgpdin
            ,trim(rgpd) rgpdout
            ,type_recherche::text type_bienED
            ,''::text nature_bien
            ,''::text commercial
            
        From edouard_denis_source_mail
        Where 1 = 1 
      

    """
     
   
    
    #for rsLivr in db.openrecordset("Select * From edouard_denis_source_mail Where edouard_denis_source_mail_id=36825"): 

    for rsLivr in db.openrecordset("Select * From edouard_denis_source_mail Where  date_extracte::date >='2023-04-17' and  flag=1 or flag=99 or flag=999"):
        try:
        #if True:
               
            sQryFiltered = "%s AND date_extracte::date >='2023-04-17' And edouard_denis_source_mail_id = %s" % (sQry, rsLivr["edouard_denis_source_mail_id"])
            print (sQryFiltered)
            tb = db.openrecordset(sQryFiltered)
            for rs in tb:
                cle=""
                rs1=dict()
               
                
                if rs["email"]!='':
                    cle=rs["email"]+"#"+rs["date_acquisition"][0:10].replace("-","")
                    if rs["tel_fixe"]=='' and rs["tel_mobile"]=='':            
                        rs["tel_mobile"]='0612345678'      
                    
                else:
                    if rs["tel_mobile"]!='':
                        cle=rs["tel_mobile"]+"#"+rs["date_acquisition"][0:10].replace("-","")
                    else:
                        if rs["tel_fixe"]!='':
                            cle=rs["tel_fixe"]+"#"+rs["date_acquisition"][0:10].replace("-","")
                        else:
                            rs["tel_mobile"]='0612345678' 
                            cle=rs["tel_mobile"]+"#"+rs["date_acquisition"][0:10].replace("-","")
                           
                      
               
                sql="SELECT count(*) as nb FROM edouarddenis WHERE cle='%s'"%(cle.lower())
                
                

                print (sql)
                curseur.execute(sql)
                tnb=curseur.fetchone()
                print ("doublon: ", tnb["nb"])
                if tnb["nb"]>0:
                    print ("OK test doublons")
                    db.runSql("Update edouard_denis_source_mail Set flag=9 Where date_extracte::date >='2023-04-17' and edouard_denis_source_mail_id=%s" % (rsLivr["edouard_denis_source_mail_id"]))
   
                    continue

                #print("KO test doublons")
               

                #for key, value in rs.iteritems():
                for key, value in rs.items():
                    #rs1[key]=value.decode("cp1252","ignore").encode("utf8","ignore").lower()
                    #rs1[key]=value.encode("utf8","ignore").lower()
                    rs1[key]=value.lower()
        #       reload(sys)
        ##       sys.setdefaultencoding("utf8")
        #        #print(str(rs).decode('UTF-8',"ignore") 
        #       
#                rs1["cle"]=cle.decode("cp1252","ignore").encode("utf8","ignore").lower()
#                print (cle.decode("cp1252","ignore").encode("utf8","ignore").lower())
                rs1["cle"]=cle.encode("utf8","ignore").lower()
                rs1["cle"]=cle.lower()
                print (cle.lower())
                
                #sys.exit(0)
                
                (bKO, msg_resp, err_msg, msg) = sendEdRequest(json.dumps(rs1))

                Historise(rsLivr["edouard_denis_source_mail_id"], msg_resp, msg)

        #        with open(str(rsLivr["edouard_denis_source_mail_id"]) + '.json', 'w') as json_file:
        #            json.dump(json.dumps(rs1), json_file)
    #            send_from = "DoNotReply@vivetic.mg"
    #            send_to = ["hasina.andriambolanavalona@vivetic.mg","tantely.rakotoalisoa@vivetic.mg" ]
    #            subject = "AutomatEdouardDenis"
                message = "Traitement du mail formulaire %s " % (rsLivr["edouard_denis_source_mail_id"])
                if (bKO or msg=="injection error"):
    #                subject = "AutomatEdouardDenis-Warning"
    #                message += "<br>Une erreur s'est produite"
    #                message += "<br>Type :%s" % (msg_resp)
    #                message += "<br>Valeur :%s" % (err_msg)
                    if msg=="" and msg_resp.strip()!='PhoneNumberError':
                        db.runSql("Update edouard_denis_source_mail Set flag=999 Where date_extracte::date >='2023-04-17' and edouard_denis_source_mail_id=%s" % (rsLivr["edouard_denis_source_mail_id"]))
                    else:
                        
                        db.runSql("Update edouard_denis_source_mail Set flag=3 Where date_extracte::date >='2023-04-17' and edouard_denis_source_mail_id=%s" % (rsLivr["edouard_denis_source_mail_id"]))
                    #send_mail(send_from, send_to, subject, message)
                else:
                    #message += "<br>Message :%s" % (msg)
                    db.runSql("Update edouard_denis_source_mail Set flag=2 Where date_extracte::date >='2023-04-17' and edouard_denis_source_mail_id=%s" % (rsLivr["edouard_denis_source_mail_id"]))
                    #send_mail(send_from, send_to, subject, message)
        except Exception as inst: 
            
            db.runSql("Update edouard_denis_source_mail Set flag=99 Where date_extracte::date >='2023-04-17' and edouard_denis_source_mail_id=%s" % (rsLivr["edouard_denis_source_mail_id"]))
            msgs=datetime.datetime.today().strftime('%Y%m%d %H:%M:%S')+'\n'
            msgs += 'erreur: '+ str(type(inst)) + '\n'
            msgs += 'CONTENU:' + str(inst) + '\n'
            #print msgs
            fichierlog.write(msgs + '\n')
            
          
        
    if os.path.exists(lock)==True:
        os.remove(lock)
        
    

    print ("Fin.")
    
    
except Exception as inst: 
    
    if os.path.exists(lock)==True:
        os.remove(lock)
    
    msgs=datetime.datetime.today().strftime('%Y%m%d %H:%M:%S')+'\n'
    msgs += 'erreur: '+ str(type(inst)) + '\n'
    msgs += 'CONTENU:' + str(inst) + '\n'
    msgapplication=msgs
    print (msgs)
    fichierlog.write(msgs + '\n')
   
    

if msgapplication!="":
    status="KO"
    


print(tracer.trace(name_application,"end",msgapplication,status,pid,prestation))
fichierlog.close() 
db.setNothing()


