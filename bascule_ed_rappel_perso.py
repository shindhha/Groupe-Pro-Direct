#! /usr/bin/env python
#coding=utf-8
import logging
import pymssql
import datetime 
from datetime import timedelta



conn = pymssql.connect('5.196.127.163','read_write','0wY!3M8cQ#Kw','PROD_EDOUARD')
cursor = conn.cursor()

date_today = datetime.datetime.now() 
format_today = date_today.strftime("%Y%m%d")
logging.basicConfig(filename='/home/user1/programme_python/logs/ed_bascule_rappel_perso_%s.log' %(format_today),level=logging.DEBUG)

t_form = 'EDOUARDDENIS'
t_ed = '31_RA_EDOUARD_DENIS'
c1_form = 'C1_EDOUARDDENIS'
c1_ed = 'C1_31_RA_EDOUARD_DENIS' 

fiche_a_updater_form ="""select tb.indice from %s tb inner join %s c1 on tb.indice=c1.indice where 
tb.indice not in('2217420','2217122','2217415') and c1.date='%s' and status in (94,95) and flag_update_fiche is null
"""%(t_form,c1_form,format_today)

logging.debug(date_today)
logging.debug('requete à exécuter')
logging.debug('%s',fiche_a_updater_form)

cursor.execute(fiche_a_updater_form)
list_indice_debut = cursor.fetchall()

final_result = [list(i) for i in list_indice_debut]
logging.debug('liste des indices à updater dans ED: ')
logging.debug('%s',final_result)
print (final_result)
if (final_result==[]):
    print ("pas de rappel perso /relance à updater dans ED")
    logging.info('pas de rappel perso à updater dans ED')
else:
    for l in final_result:
        indice_debut = ','.join(map(str,l))
        logging.info('vérification  indice dans ED dont l indice_debut = %s',indice_debut)
        
        verif_fiche_in_ed="select indice from [%s] where indice_debut='%s' and flag_update_fiche is null"%(t_ed,indice_debut) 
        logging.info('%s',verif_fiche_in_ed)
        cursor.execute(verif_fiche_in_ed)
        res = cursor.fetchall()
        
        list_indice= [list(j) for j in res]
        logging.debug('requête de vérification de l indice dans ED dont l indice_debut=%s',indice_debut)
        
        if (list_indice==[]):
            logging.debug('cette fiche n est pas encore basculée dans ED')
            print('fiche non existante dans ED')
        else:
            for ind in list_indice:
                indc = ','.join(map(str,ind))
                logging.debug('fiche existante dans ED, indice=%s, indice_debut=%s',indc,indice_debut)
                logging.info('')
                logging.info('récupération des infos dans C1 formulaire pour l indice %s',indice_debut)
                logging.info('')
                print("fiche existante dans ED, indice=%s, indice_debut=%s" %(indc,indice_debut))
                
                list_info_form=""" select priorite,
 versop,
rappel,
tv,
id_tv,
status,
lib_status,
detail,
lib_detail from %s tb inner join %s c1 on tb.indice=c1.indice where c1.date='%s' and status in(94,95) and tb.indice=%s and flag_update_fiche is null
""" %(t_form,c1_form,format_today,indice_debut)
                
                logging.info('%s', list_info_form)
                cursor.execute(list_info_form)
                infos_ed=cursor.fetchall()
                for x in infos_ed:
                    logging.info('')
                    logging.info('%s',x)
                logging.info('')
                logging.info('maj fiche dans ED')
                
                query_update_form_to_ed="""
                update c1_ed
                  set
                  c1_ed.priorite=0,
                  c1_ed.versop=c1_f.versop,
                  c1_ed.rappel=c1_f.rappel,
                  c1_ed.tv=c1_f.tv,
                  c1_ed.id_tv=c1_f.id_tv,
                  c1_ed.status=c1_f.status,
                  c1_ed.lib_status=c1_f.lib_status,
                  c1_ed.detail=c1_f.detail,
                  c1_ed.lib_detail=c1_f.lib_detail
                  from %s c1_ed
                  inner join %s c1_f
                  on c1_ed.mixup=c1_f.indice 
                 where c1_ed.mixup='%s' 
""" %(c1_ed,c1_form,indice_debut)
                logging.info('%s', query_update_form_to_ed)
                
                cursor.execute(query_update_form_to_ed)
                conn.commit()
                print('')
                print("maj effectuee des colonnes basculees dans ED, indice: %s" %(indc))
                logging.debug('maj effectuee des colonnes basculees dans ED, indice: %s',indc)
                print ('')
                logging.debug('')
                
                query_update_form ="update [%s] set flag_update_fiche='done' where indice=%s and flag_update_fiche is null" %(t_form,indice_debut)
                logging.info('%s', query_update_form)
                cursor.execute(query_update_form)
                conn.commit()
                print("maj effectuee dans formulaire, indice: %s" %(indice_debut))
                logging.debug('maj effectuee dans formulaire, indice: %s',indice_debut)
                print ('')
                logging.debug('')
                
                query_update_ed ="update [%s] set flag_update_fiche='done' where indice=%s and flag_update_fiche is null" %(t_ed,indc)
                logging.info('%s', query_update_ed)
                cursor.execute(query_update_ed)
                conn.commit()
                print("maj effectuee dans ED, indice: %s" %(indc)) 
                logging.debug('maj effectuee dans ED, indice: %s',indc)
                print ('')
                logging.debug('')
                logging.debug('---------DONE---------')
                logging.debug('')
                
conn.close()
cursor.close()
print("VITAAA")
logging.debug('---------VITA---------')
logging.debug('')
                
                
                
                
                
                
                    
                     
                    
                
        
        
                    
 
        
        
        
        
       
        
  

