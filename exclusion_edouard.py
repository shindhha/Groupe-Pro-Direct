#! /usr/bin/env python
#coding=utf-8
import pymssql
import datetime

conn = pymssql.connect('5.196.127.163','read_write','0wY!3M8cQ#Kw','PROD_EDOUARD')
cursor = conn.cursor()

where_exclu = "WHERE  date=REPLACE(CONVERT(date,getdate(),120),'-','') and status in (1,2,3,8,9,10) and priorite<>'-10'"

exclu_def =""" update C1_31_RA_EDOUARD_DENIS 
set versop=-1,
priorite=-10  %s """ %(where_exclu)

daty = datetime.datetime.now()

log_exclu ="""  insert into EDOUARD_DENIS_EXCLU_LOG (min_indice, max_indice, row_updated, date_update_, date_update) 
select 
  min(indice) min_indice,
  max(indice) max_indice,
  (select count(*) from C1_31_RA_EDOUARD_DENIS %s) row_updated,
(select getdate()) date_update_,
(select getdate()) date_update
  from C1_31_RA_EDOUARD_DENIS %s

""" %(where_exclu, where_exclu)

update_absent ="update C1_31_RA_EDOUARD_DENIS set versop=-1 where priorite=0 and versop=-999"

update_vierge_formulaire ="exec UPDATE_VIERGE_FORMULAIRE"

print ("insert to log")
cursor.execute(log_exclu)
conn.commit()
print(cursor.rowcount, "lignes inserees") 
print ("")

print ("exclusion")
cursor.execute(exclu_def)
conn.commit()
print(cursor.rowcount, "lignes exclues") 
print ("")

print ("update absent")
cursor.execute(update_absent)
conn.commit()
print(cursor.rowcount, "lignes maj") 
print ("")

print ("update vierge formulaire")
cursor.execute(update_vierge_formulaire)
conn.commit()
print(cursor.rowcount, "lignes maj") 
print ("")

conn.close()
cursor.close()
print ("exclusion terminee")


