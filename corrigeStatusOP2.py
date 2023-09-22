#! /usr/bin/env python
# -*- coding: utf8
import requests
import json
import datetime, sys, os,logging
from datetime import date, timedelta,datetime
from RaycnxDict import Raycnx
daty = str(date.today())
recherche = str(daty).replace('-','')
#recherche ='20200618'
print (recherche)
date_p= datetime.now()
print(date_p)
log_name = '//home//user1//programme_python//logs//GetprogrammeCRm_'+ daty.replace('-','') + '.log'
logging.basicConfig(filename=log_name, level=logging.DEBUG)
logging.info("********************************date lancement programme: " + str(date_p) + " ************************")
edouarddenis = Raycnx(host='5.196.127.163', dbname='PROD_EDOUARD', user='read_write', password='0wY!3M8cQ#Kw')


sql_ = """
select op2.indice as indice,
op1.status op1_status, op1.lib_status op1_lib_status, op1.detail op1_detail, op1.lib_detail op1_lib_detail,op1.priorite priorite,op1.rappel rappel,op1.ID_TV id_tv,
op1.tv tv,op1.versop,
case when op2.status = op1.status then 'ok' else 'problème' end etat
 from c1_edouarddenis op1
inner join [31_RA_EDOUARD_DENIS] tb2 on op1.indice = tb2.indice_debut
inner join [c1_31_RA_EDOUARD_DENIS] op2 on op2.indice = tb2.indice
where op1.date ='{}' and op2.status <> op1.status
 and op1.status in (1,2,3,8,9,10) """.format(recherche)

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
def correctionStatusOP2(sql):
    if edouarddenis.execute_crud(sql):
        print("updated")
    else:
        print ("not updated")
    
    
if connecter_site():
    print(sql_)
    data = edouarddenis.execute_crud(sql_, typ='kk')
    for ele in data:
        indice  = ele.get('indice')
        status = ele.get('op1_status')
        lib_status = ele.get('op1_lib_status')
        if ele.get('op1_detail'):
            detail = ele.get('op1_detail')
        else:
            detail = 0
        if ele.get('op1_lib_detail'):
            lib_detail = ele.get('op1_lib_detail')
        else:
            lib_detail=''
        rappel = ele.get('rappel')
        if ele.get('id_tv'):
            id_tv =ele.get('id_tv')
        else:
            id_tv =0
        tv = ele.get('tv')
        priorite = ele.get('priorite')
        versop = ele.get('versop')
        query = "UPDATE [C1_31_RA_EDOUARD_DENIS] set status = {}, lib_status = '{}', detail = {}, lib_detail ='{}', priorite ={}, rappel='{}',tv='{}',id_tv ='{}', versop='{}' WHERE indice = {}".format(status,lib_status,detail,lib_detail,priorite,rappel,tv,id_tv,versop,indice)
        print (query)
        correctionStatusOP2(query)
        #print ("etat de mise à jour l'indice :" + str(indice) +" requety: "+ str(query) + "etat : "+ str(correctionStatusOP2(query))")
    edouarddenis.closeo()    
    
    
