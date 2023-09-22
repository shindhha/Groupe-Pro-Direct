#! /usr/bin/env python
#coding=utf-8
import os,sys,logging
import requests, json
from datetime import date, timedelta,datetime
import pymssql
import smtplib



daty = date.today()
conn = pymssql.connect('5.196.127.163', 'read_write', '0wY!3M8cQ#Kw', 'PROD_EDOUARD')
cursor = conn.cursor(as_dict=True)

query_prio="""SELECT MAX(daty)as daty from [edouarddenis] tb
INNER JOIN C1_edouarddenis c1 on tb.indice = c1.indice
where  priorite >=1"""

cursor.execute (query_prio)
prio = cursor.fetchall()
max_date = str(prio[0]['daty'])
print(max_date)

update_prio= """ UPDATE C1_edouarddenis set priorite= 1 
FROM C1_edouarddenis c1
INNER JOIN edouarddenis tb on c1.indice = tb.indice
Where daty = '{}' and priorite > 1
""".format(max_date)

cursor.execute (update_prio)
conn.commit()
#test

#Fin test
query_zozio="""SELECT distinct(daty) from [edouarddenis] tb
INNER JOIN C1_edouarddenis c1 on tb.indice = c1.indice
where priorite >= 1 and daty <> '{}'
Order by daty desc""".format(max_date)


cursor.execute (query_zozio)
zozio = cursor.fetchall()
print(zozio)
print(len(prio))
print(len(zozio))

sql = "SELECT indice , replace(substring(date_acquisition,12,5),':','') as heure From edouarddenis where daty ='{}' and date_acquisition is not null order by heure desc".format(max_date)
print(sql)
cursor.execute(sql)
alahatra = cursor.fetchall()
print(alahatra)
sqlmix = "SELECT MAX(mixup) as mixup from C1_edouarddenis"
cursor.execute(sqlmix)
mixup = cursor.fetchone()
index = mixup["mixup"]
index = index + 1
print(index)
print("Traitement 1")
for idaka in alahatra :
	print(idaka)
	indice = idaka["indice"]
	ora = idaka["heure"]
	print(indice , ora)
	updateo = "UPDATE C1_edouarddenis set mixup={} WHERE indice={}".format(index,indice)
	cursor.execute(updateo)
	conn.commit()
	index = index +1 
	print("update ny indice : " , indice)
	
if len(zozio) > 0 :
	index = 2
	print("Traitement 2")
	for fiche in zozio :
		doduo = fiche['daty']
		print (doduo)
		update_prio= """ UPDATE C1_edouarddenis set priorite= '{}' 
						FROM C1_edouarddenis c1
						INNER JOIN edouarddenis tb on c1.indice = tb.indice
						Where daty = '{}' and priorite >= 1""".format(index,doduo)
		cursor.execute(update_prio)
		conn.commit()
		index = index+1	
		print("Update faite pour " , doduo)	