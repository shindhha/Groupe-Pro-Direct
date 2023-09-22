#! /usr/bin/env python3.7
#coding=utf-8
import os,sys, logging
import requests,pymssql,uuid
import json , collections
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta, datetime

conn = pymssql.connect('5.196.127.163','read_write','0wY!3M8cQ#Kw','VIVETIC_PROD')
cursor=conn.cursor(as_dict=True)

daty = str(date.today())
date_p = datetime.now()
print (daty)

#strFrom = 'contact@lppromotion.com'
#memo = 'Lppap0305!'
#smtpServer = 'smtp.office365.com'
#port = 587

def updateFini(indice, flag):
	updateo = "UPDATE [LP_PROMOTION_HUBSPOT] set flagmail_injoignable = '{}' + ' ' + convert(varchar,getdate(),120 ) WHERE INDICE ={}".format(flag,indice)
	cursor.execute(updateo)
	conn.commit()
	return True

query = "SELECT indice,email,telephone from [LP_PROMOTION_HUBSPOT] where flagmail_injoignable='mail' and email is not NULL and email <>''"
cursor.execute(query)
Data = cursor.fetchone()

if Data!=None:
	indice = Data.get("indice")
	email = Data.get("email")
	phone = Data.get("telephone")
	print (indice)
	print (email)

	smtp_server = "smtp.office365.com"
	port = 587  # For starttls
	sender_email = "alix.pujol@lppromotion.com"
	password = 'Lppap0305!'
	#receiver_email = 'nilaina.andrimaheniniaina@vivetic-group.com'
	receiver_email = email
	message = MIMEMultipart("alternative")
	message["Subject"] = "Notification LP PROMOTION"
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Cci"] = "iscc@vivetic.mg"
	text = """
<html>
  <body>
     <p> Bonjour,<p> pour donner suite à votre demande de contact pour un projet immobilier, nous avons tenté de vous joindre sur le numéro : {}
Nous restons à votre disposition au 09 88 29 34 67. »<p>
Cordialement.<p>
L’équipe LP PROMOTION 
  </body>
</html>
""".format(phone)
	#text = "Ce ci est un test"
	s = smtplib.SMTP(host=smtp_server, port=port)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(sender_email, password)
	message.attach(MIMEText(text, 'html'))
	try :
		s.sendmail(sender_email,receiver_email, message.as_string())
		del message
	    # Terminate the SMTP session and close the connection
		s.quit()
		print('lasa')
		updateFini(indice, 'OK')
	except pymssql.StandardError as e: 
		print (e)		
		updateFini(indice, 'KO')
else :
	print("Aucun traitement")	
conn.close()