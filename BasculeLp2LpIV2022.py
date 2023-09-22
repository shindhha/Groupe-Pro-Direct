#! /usr/bin/env python
#coding=utf-8
import os,sys,logging
import requests, json
from datetime import date, timedelta,datetime
import pymssql
import smtplib



daty = date.today()
androany=daty.strftime("%w")
print(androany)

#if (androany=='4'):
#    randevotaka = "'"+str((date.today() + timedelta(2)).strftime("%d/%m/%Y"))+"'" +","+"'"+str((date.today() + timedelta(4)).strftime("%d/%m/%Y"))+"'"
#if  (androany=='5'):
#    randevotaka = "'"+str((date.today() + timedelta(4)).strftime("%d/%m/%Y"))+"'"  
#else:
#    randevotaka = "'"+str((date.today() + timedelta(2)).strftime("%d/%m/%Y"))+"'" 
if  (androany=='5'):
    randevotaka = "'"+str((date.today() + timedelta(3)).strftime("%d/%m/%Y"))+"'" +","+"'"+str((date.today() + timedelta(4)).strftime("%d/%m/%Y"))+"'" 
else:	
	randevotaka = "'"+str((date.today() + timedelta(2)).strftime("%d/%m/%Y"))+"'"
print (randevotaka)
logfilename = "//var//log_iscc//log_lp_ConfirmationRdv_"+str(daty).replace('-','') +".log"
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("date lancement programme: " + str(daty))


conn = pymssql.connect('5.196.127.163', 'read_write', '0wY!3M8cQ#Kw', 'VIVETIC_PROD')
cursor = conn.cursor(as_dict=True)

theuRl = "http://ws-238.vivetic.com/LpBascule/api/LpBasculeInject" 
headers = {'Content-Type': "application/json"}

query="""SELECT  indice as indice_origine , ISNULL( adresse,'')adresse , ISNULL( budget, '') budget, ISNULL( civilite, '') civilite, ISNULL( cle, '')cle , ISNULL(  codePostal, '')codePostal , ISNULL( codePostalRecherche1, '')codePostalRecherche1 , ISNULL( codePostalRecherche2, '')codePostalRecherche2 , ISNULL( codePostalRecherche3, '')codePostalRecherche3 , ISNULL( commentConnu, '')commentConnu , ISNULL( complementAdresse, '')complementAdresse , ISNULL(  conversionRecente, '')conversionRecente , ISNULL(  dateCreation, '')dateCreation , ISNULL( email, '')email , ISNULL(  hubspotId, '')hubspotId , ISNULL(  informationSource1, '')informationSource1 , ISNULL( message, '')message , ISNULL(  nom, '')nom , ISNULL(  nombrePiece, '')nombrePiece , ISNULL(  nomProgramme, '')nomProgramme , ISNULL( prenom, '')prenom , ISNULL( telephone, '')telephone , ISNULL(  typeAchat, '')typeAchat , ISNULL(  typeBien, '')typeBien , ISNULL( ville, '')ville , ISNULL(  villeRecherche1, '')villeRecherche1 , ISNULL(  villeRecherche2, '')villeRecherche2 , ISNULL(  villeRecherche3, '')villeRecherche3 , ISNULL(  optin, '')optin , ISNULL(  daty, '')daty , ISNULL( Calltype, '')Calltype , ISNULL( flagmail_injoignable, '')flagmail_injoignable , ISNULL( details_source_hors_ligne, '')details_source_hors_ligne , ISNULL(  budget_VAL, '')budget_VAL , ISNULL( civilite_VAL, '')civilite_VAL , ISNULL( commentConnu_VAL, '')commentConnu_VAL , ISNULL( nombrePiece_VAL, '')nombrePiece_VAL , ISNULL(  optin_VAL, '')optin_VAL , ISNULL(  typeAchat_VAL, '')typeAchat_VAL , ISNULL(  typeBien_VAL, '')typeBien_VAL , ISNULL( COMMENTAIRES, '')COMMENTAIRES , ISNULL( date_deal_change, '')date_deal_change , ISNULL( proprietaireContact, '')proprietaireContact , ISNULL(  flag_mail_change, '')flag_mail_change , ISNULL( flag_resultat_appel_change, '') flag_resultat_appel_change, ISNULL( flag_proprietairecontact_change, '')flag_proprietairecontact_change , ISNULL(  flag_deal_change, '')flag_deal_change , ISNULL( flag_contact_change, '')flag_contact_change , ISNULL(  Flag_fin_appel_deal, '')Flag_fin_appel_deal , ISNULL(  createdate_hubspot, '')createdate_hubspot , ISNULL( proprietaireContact_VAL, '')proprietaireContact_VAL , ISNULL(  ANI, '')ANI , ISNULL( DATE_RDV, '')DATE_RDV , ISNULL( HEURE_RDV, '')HEURE_RDV , ISNULL( TYPE_RDV, '')TYPE_RDV , ISNULL( COMMERCIAL,'' )COMMERCIAL, ISNULL( NOM_COMMERCIAL,'' )NOM_COMMERCIAL  FROM [VIVETIC_PROD].[dbo].[LP_PROMOTION_HUBSPOT] 
Where DATE_RDV in ({}) and (status = 1 or TYPE_RDV like '%RDV%' or TYPE_RDV='Rendez-vous programmé') and indice not in (SELECT indice_origine FROM LP_PROMOTION_CONFIRMATION_RDV where indice_origine is not null)
UNION ALL
SELECT  indice as indice_origine , ISNULL( adresse,'')adresse , ISNULL( budget, '') budget, ISNULL( civilite, '') civilite, ISNULL( cle, '')cle , ISNULL(  codePostal, '')codePostal , ISNULL( codePostalRecherche1, '')codePostalRecherche1 , ISNULL( codePostalRecherche2, '')codePostalRecherche2 , ISNULL( codePostalRecherche3, '')codePostalRecherche3 , ISNULL( commentConnu, '')commentConnu , ISNULL( complementAdresse, '')complementAdresse , ISNULL(  conversionRecente, '')conversionRecente , ISNULL(  dateCreation, '')dateCreation , ISNULL( email, '')email , ISNULL(  hubspotId, '')hubspotId , ISNULL(  informationSource1, '')informationSource1 , ISNULL( message, '')message , ISNULL(  nom, '')nom , ISNULL(  nombrePiece, '')nombrePiece , ISNULL(  nomProgramme, '')nomProgramme , ISNULL( prenom, '')prenom , ISNULL( telephone, '')telephone , ISNULL(  typeAchat, '')typeAchat , ISNULL(  typeBien, '')typeBien , ISNULL( ville, '')ville , ISNULL(  villeRecherche1, '')villeRecherche1 , ISNULL(  villeRecherche2, '')villeRecherche2 , ISNULL(  villeRecherche3, '')villeRecherche3 , ISNULL(  optin, '')optin , ISNULL(  daty, '')daty , ISNULL( Calltype, '')Calltype , ISNULL( flagmail_injoignable, '')flagmail_injoignable , ISNULL( details_source_hors_ligne, '')details_source_hors_ligne , ISNULL(  budget_VAL, '')budget_VAL , ISNULL( civilite_VAL, '')civilite_VAL , ISNULL( commentConnu_VAL, '')commentConnu_VAL , ISNULL( nombrePiece_VAL, '')nombrePiece_VAL , ISNULL(  optin_VAL, '')optin_VAL , ISNULL(  typeAchat_VAL, '')typeAchat_VAL , ISNULL(  typeBien_VAL, '')typeBien_VAL , ISNULL( COMMENTAIRES, '')COMMENTAIRES , ISNULL( date_deal_change, '')date_deal_change , ISNULL( proprietaireContact, '')proprietaireContact , ISNULL(  flag_mail_change, '')flag_mail_change , ISNULL( flag_resultat_appel_change, '') flag_resultat_appel_change, ISNULL( flag_proprietairecontact_change, '')flag_proprietairecontact_change , ISNULL(  flag_deal_change, '')flag_deal_change , ISNULL( flag_contact_change, '')flag_contact_change , ISNULL(  Flag_fin_appel_deal, '')Flag_fin_appel_deal , ISNULL(  createdate_hubspot, '')createdate_hubspot , ISNULL( proprietaireContact_VAL, '')proprietaireContact_VAL , ISNULL(  ANI, '')ANI , ISNULL( DATE_RDV, '')DATE_RDV , ISNULL( HEURE_RDV, '')HEURE_RDV , ISNULL( TYPE_RDV, '')TYPE_RDV , ISNULL( COMMERCIAL,'' )COMMERCIAL, ISNULL( NOM_COMMERCIAL,'' )NOM_COMMERCIAL  FROM [VIVETIC_PROD].[dbo].[LP_PROMOTION_HUBSPOT_AE] 
Where DATE_RDV in ({}) and (status = 1 or TYPE_RDV like '%RDV%' or TYPE_RDV='Rendez-vous programmé') and indice not in (SELECT indice_origine FROM LP_PROMOTION_CONFIRMATION_RDV where indice_origine is not null)""".format(randevotaka,randevotaka)


cursor.execute (query)
data = cursor.fetchall()

if len(data) > 0 :
    print (data[0])
    data2Send = json.dumps(data[0])
    indigo = data[0]["indice_origine"]
    print(indigo)
    retourta =requests.post(theuRl,data = data2Send, headers=headers)
    print(retourta.json())
else : 
    print("Aucun Rdv à basculer")
    logging.info("Aucun RDV à basculer")

conn.close()