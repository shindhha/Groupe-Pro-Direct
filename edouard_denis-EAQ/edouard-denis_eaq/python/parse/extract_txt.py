#!/usr/bin/env python
# -*- coding: cp1252  -*-

#try: 
#    from BeautifulSoup import BeautifulSoup
#except ImportError:
#    from bs4 import BeautifulSoup
#html = #the HTML code you've written above
#parsed_html = BeautifulSoup(html)
#print(parsed_html.body.find('div', attrs={'class':'container'}).text)


import sys,os
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("cp1252")
import re
#import glob
import psycopg2
import psycopg2.extras
import datetime
import unicodedata

#print ord("•")
#sys.exit(0)

def InitFields():
    chp_dict={}
    chp_dict["programme"]=""
    chp_dict["nom_client"]=""
    chp_dict["destination"]=""
    chp_dict["projet"]=""
    chp_dict["type_recherche"]=""
    chp_dict["surface"]=""
    chp_dict["code_postal"]=""
    chp_dict["ville"]=""
    chp_dict["adresse"]=""
    chp_dict["code_programme"]=""
    chp_dict["mail"]=""
    chp_dict["telephone"]=""
    chp_dict["budget"]=""
    chp_dict["commentaire"]=""
    chp_dict["taille_logement"]=""
    chp_dict["tel_mobile"]=""
    
    
  
    chp_dict["utm_source"]=""
    chp_dict["optin"]=""
    chp_dict["jour_rappel"]=""
    chp_dict["datee"]=""
    chp_dict["parrainage"]=""
    chp_dict["civilite"]=""
    chp_dict["utm_medium"]=""
    chp_dict["traitement_wcb"]=""
    chp_dict["action"]=""
    chp_dict["rgpd"]=""
    chp_dict["utm_campaign"]=""
    chp_dict["projet_client"]=""
    chp_dict["heure_rappel"]=""
    chp_dict["numero_lot"]=""
    chp_dict["prenom_client"]=""
    

    
    
    return chp_dict


# Load the HTML content
#fichier = open("data.txt", "w")

#tfile = glob.glob("C:/image/edouard_denis/**/*.html")
#entete=""
#print tfile

#for key, value in tchamp.iteritems():
#    entete+=";"+key
#        
#fichier.write(entete[1:].encode("cp1252")+"\n")

fichierlog = open(os.path.basename(__file__).replace(".py","")+datetime.datetime.today().strftime('%Y%m%d')+'.log', 'a')
lock=os.path.basename(__file__)+datetime.datetime.today().strftime('%Y%m%d')+'.lock'

if os.path.exists(lock)==False:
    
    fichierlock=open(lock,'w')
    fichierlock.close() 
else:
    sys.exit(0)    


try:
#if True:
     
    
    prod = psycopg2.connect('dbname=production user=prep1 password=pp1p host=mcserver1.madcom.local')
    prod.set_client_encoding('WIN1252')
    curprod = prod.cursor(cursor_factory=psycopg2.extras.DictCursor)
    prod.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

    sql="select * FROM edouard_denis_source_mail where date_creation::date > '2023-04-17'::date and flag=0 and (from_mail like '%contact@immobilier.lefigaro.fr%' or from_mail like '%nouveau.contact@myselogerpro.nmp1.com%' )  order by edouard_denis_source_mail_id"

    #sql="select * FROM edouard_denis_source_mail where edouard_denis_source_mail_id=2366  and (from_mail like '%contact@immobilier.lefigaro.fr%' or from_mail like '%nouveau.contact@myselogerpro.nmp1.com%' )  order by edouard_denis_source_mail_id"
    #sql="select * FROM edouard_denis_source_mail where from_mail like '%contact@immobilier.lefigaro.fr%' or from_mail like '%nouveau.contact@myselogerpro.nmp1.com%'   order by edouard_denis_source_mail_id"


    curprod.execute(sql)
    tfile=curprod.fetchall()
    print tfile
    
except Exception as inst: 
    if os.path.exists(lock)==True:
        os.remove(lock) 
    
    msgs=datetime.datetime.today().strftime('%Y%m%d %H:%M:%S')+'\n'
    msgs += 'erreur: '+ str(type(inst)) + '\n'
    msgs += 'CONTENU:' + str(inst) + '\n'
    print msgs
    fichierlog.write(msgs + '\n')
    fichierlog.close()    
    prod.rollback()
    sys.exit(0)



for file_ok in tfile:
    try:
        
    #if True:
        tchamp=InitFields()
        edouard_denis_source_mail_id=file_ok["edouard_denis_source_mail_id"]
        if file_ok["flag_type"]==1:
            reload(sys)
            sys.setdefaultencoding("cp1252")
            
        
            
          
            
            html_file = open(file_ok["savedirpath_origine"]+"/"+file_ok["n_ima"], 'r')
            html_content = html_file.read()
            html_file.close() # clean up


            tchamp=InitFields()
            tchamp["rgpd"]="non"
            
            tchamp["utm_source"]="SE LOGER NEUF"
            tchamp["utm_medium"]="LIGNAGE"
            tchamp["utm_campaign"]="NATIONAL LIGNAGE SELOGERNEUF FIL ROUGE 201901"
            
            
            

            # Initialize the BS objectaiza 
            soup  = bs(html_content,'html.parser') 
            # At this point, we can interact with the HTML 
            # elements stored in memory using all helpers offered by BS library
            
            #tag_nom_client=soup.body.find('td', attrs={'style':'font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#3e4649; font-weight: bold; line-height:22px;'})
            tag_nom_client=soup.body.find('td', attrs={'style':'font-family:Arial, Helvetica, sans-serif; font-size:18px; color:#4c545f; font-weight: bold;'})
            if tag_nom_client:
                print tag_nom_client.text
                tchamp["nom_client"]= tag_nom_client.text.replace("vous contacte pour ce programme",""). replace("s'intéresse à ce bien","").replace("a fait une recherche sur des critères similaires à ce bien","").strip().encode("cp1252","ignore")
               

            tag_telephone=soup.body.find('a', attrs={'href':re.compile(r"^tel:")})


            if tag_telephone:
                print "0"+tag_telephone.get('href').replace("tel:","").strip().encode("cp1252","ignore").replace(" ","").replace("+33","0")[-9:]
                tchamp["telephone"]= "0"+tag_telephone.get('href').replace("tel:","").strip().encode("cp1252","ignore").replace(" ","").replace("+33","0")[-9:]
            



            tag_commentaire=soup.body.find('td', attrs={'style':'font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#3e4649;padding:20px'})
            if tag_commentaire:
                tchamp["commentaire"]= tag_commentaire.text.strip().encode("cp1252","ignore")
                motif_piece = re.compile(r"\d+ pièce")
                corresp = motif_piece.search(tag_commentaire.text.strip().encode("cp1252","ignore"))
                if corresp!=None:
                
                    tchamp["taille_logement"]="T "+corresp.group().encode("cp1252","ignore").replace("pièces","").replace("pièce","").strip()
                    print("corresp.group()****** :", corresp.group().encode("cp1252","ignore"))
                
            print "tonga ve"
                

                
            #tag_description=soup.body.find('span', attrs={'style':'font-size:18px;color:#3e4649; font-weight:bold;'})
            tzbalise=soup.findAll('span',attrs={'class': re.compile(r"^txt")})
           
            i=0

            tline=[]
            for tbalise in tzbalise:
                infos_balise=tbalise.text.encode("cp1252","ignore").lstrip("\n").strip()
                
                if infos_balise!="" and infos_balise!="\n":
                    #print "1-",infos_balise
                    
                    i+=1
                    tzline_balise=infos_balise.split("\n")
                   
                      
                    if len(tzline_balise) >1:
                        
                       
                        for tline_balise in tzline_balise:
                            
                            print "info_rc 11 "+tline_balise
                            tligne= tline_balise.split("•")
                            
                           
                            if len(tligne) >1:
                                tchamp["destination"]=tligne[0].strip()
                                tchamp["projet"]=tligne[1].strip()
                                if len(tligne)==3:
                                    tchamp["type_recherche"]=tligne[2].strip()
                                if len(tligne)==4:    
                                    tchamp["surface"]=tligne[3].strip()
                            
                            elif tligne[0].strip().find("(")!=-1 and tligne[0].strip().find(")")!=1:
                                cpville=tligne[0].strip()
                                cp=cpville[cpville.find("(")+1:cpville.find(")")]
                                ville=cpville[0:cpville.find("(")]
                                
                                print "cp", cp
                                print "ville", ville
                                
                                if tligne[0].strip().find(")")!=-1:
                                    
                                    
                                    str1=tligne[0].strip()[tligne[0].strip().find(")")+3:].strip()
                                    print str1
                                    str1=str1.replace("0000","").strip() 
                                    motif_date = re.compile(r"0\d?\d?\d? ")
                                    #while True:
                                    corresp = motif_date.search(str1)
                                    if corresp!=None:
                                        if int(corresp.group())==0:
                                            str1=str1.replace(corresp.group().encode("cp1252","ignore"),"").strip()
                                        else:
                                            str1=str1.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group())))
                                        print("corresp.group() :", str1)
                                    else:
                                        motif_date = re.compile(r"0\d?\d?\d?-")
                                        corresp = motif_date.search(str1)
                                        if corresp!=None:
                                            if int(corresp.group().replace("-",""))==0:
                                                str1=str1.replace(corresp.group().encode("cp1252","ignore"),"").strip()
                                            else:
                                                str1=str1.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group().replace("-","")))+"-")
                                           
                                       
                                    tchamp["adresse"]=str1
                                    
                                  
                                tchamp["code_postal"]=cp
                                tchamp["ville"]=ville
                                #print "adresse", str1
                                
                            elif tligne[0].strip().find("Ref.")!=-1 :
                                tchamp["code_programme"]=tligne[0].strip().split(":")[1].strip()[0:11]
                            elif tligne[0].strip().find("€")!=-1 :
                                tchamp["budget"]=tligne[0].strip().replace("A partir de","").strip()
                            elif tligne[0].isupper():
                                str1=tligne[0].replace("0000","").strip() 
                                #print "adresse: "+str1
                                motif_date = re.compile(r"0\d?\d?\d? ")
                                #while True:
                                corresp = motif_date.search(str1)
                                if corresp!=None:
                                    str1=str1.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group())))
                                    #print("corresp.group() :", str1)
                                else:
                                    motif_date = re.compile(r"0\d?\d?\d?-")
                                    corresp = motif_date.search(str1)
                                    if corresp!=None:
                                        if int(corresp.group().replace("-",""))==0:
                                            str1=str1.replace(corresp.group().encode("cp1252","ignore"),"").strip()
                                        else:
                                            str1=str1.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group().replace("-","")))+"-")
                                    
                                    
                                print "adresse2", str1
                                tchamp["adresse"]=str1
                            else:
                                tchamp["destination"]=tligne[0].strip()       
                                    
                          
                    else:
                       
                        print "xxxx " + tzline_balise[0]
                        if tzline_balise[0].strip().find("€")!=-1 :
                            tchamp["budget"]=tzline_balise[0].strip().replace("A partir de","").strip()
                        elif tzline_balise[0].strip().find("@")!=-1 :
                            tchamp["mail"]=tzline_balise[0].strip()
                            
                        elif tzline_balise[0].strip().find("(")!=-1 and tzline_balise[0].strip().find(")")!=1:
                            cpville=tzline_balise[0].strip()
                            cp=cpville[cpville.find("(")+1:cpville.find(")")]
                            ville=cpville[0:cpville.find("(")]
                            
                            if tzline_balise[0].strip().find(")")!=-1:
                               
                                adresse=tzline_balise[0].strip()[tzline_balise[0].strip().find(")")+3:].strip()
                                print "adresse3: "+adresse
                                adresse=adresse.replace("0000","").strip() 
                                motif_date = re.compile(r"0\d?\d?\d? ")
                                #while True:
                                corresp = motif_date.search(adresse)
                                if corresp!=None:
                                    adresse=adresse.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group())))
                                    print("corresp.group() :", adresse)
                                else:
                                    motif_date = re.compile(r"0\d?\d?\d?-")
                                    corresp = motif_date.search(adresse)
                                    if corresp!=None:
                                        if int(corresp.group().replace("-",""))==0:
                                           adresse=adresse.replace(corresp.group().encode("cp1252","ignore"),"").strip()
                                        else:
                                           adresse=adresse.replace(corresp.group().encode("cp1252","ignore"),str(int(corresp.group().replace("-","")))+"-")

                                    
                                
                                
                                
                                tchamp["adresse"]=adresse
                            tchamp["code_postal"]=cp
                            tchamp["ville"]=ville
                            
                        elif tzline_balise[0].strip().find("Ref.")!=-1 :
                            #tchamp["code_programme"]=tzline_balise[0].replace("Ref. du programme :","").strip()
                            tchamp["code_programme"]=tzline_balise[0].strip().split(":")[1].strip()[0:11]
                            
                        elif tzline_balise[0].isupper():
                            tchamp["programme"]=tzline_balise[0].strip() 
                        else:
                            tchamp["destination"]=tzline_balise[0].strip()
                 

            
             
           
           
        else:
            
           
            reload(sys)
            sys.setdefaultencoding("utf8")
            
            tchamp={}
            print file_ok["savedirpath_origine"]+"/"+file_ok["n_ima"]
            with open(file_ok["savedirpath_origine"]+"/"+file_ok["n_ima"], "r") as file:
                i=0
                for line in file:
                   
                    if line.lstrip("\n") !="":
                        i+=1
                        if line.find(":")!=1:
                            line1=line[0:line.find(":")+1]+line[line.find(":")+1:].replace(":","(2.)")
                            key, value = line1.strip().split(":")
                            print key
                            try:
                                key=unicodedata.normalize('NFKD', u""+key).encode('ascii','ignore')
                            except:
                                pass    
                            #print unicodedata.normalize('NFKD', u""+key).encode('ascii','ignore')
                            #print key,unicodedata.normalize('NFKD', key).encode('ascii','ignore').strip().replace(" ","_").replace("email","mail").replace("date","datee").replace("Commentaires","Commentaire").lower()
                         
                    tchamp[key.strip().lower().replace("\xe9","e").replace(" ","_").replace("nom","nom_client").replace("email","mail").replace("date","datee").replace("commentaires","commentaire")] = str(value).decode('UTF-8',"ignore").encode('cp1252',"ignore").strip().replace("(2.)",":")
            if tchamp["telephone"]!="":        
                tchamp["telephone"]="0"+tchamp["telephone"].replace(" ","").replace("+33","0")[-9:]
            print(tchamp)
            tchamp["surface"]=""
            tchamp["tel_mobile"]=""
            tchamp["taille_logement"]=""
            
        if tchamp["type_recherche"]!="":
            if  tchamp["type_recherche"].find("T")!=-1:
                tchamp["type_recherche"]= tchamp["type_recherche"].replace("T","").strip()+" pièce(s)"
        if tchamp["telephone"][0:2]=='06':
            tchamp["tel_mobile"]=tchamp["telephone"]
            tchamp["telephone"]=""
        
                
                
        motif_piece = re.compile(r"appartement T\d+\.? ")
        corresp = motif_piece.search(tchamp["commentaire"])
        if corresp!=None:
            tchamp["taille_logement"]="T "+corresp.group().encode("cp1252","ignore").replace("appartement T","").replace(".","").strip()
            print("corresp.group()****** :", corresp.group().encode("cp1252","ignore"))
            if tchamp["type_recherche"]=="":
                tchamp["type_recherche"]= corresp.group().encode("cp1252","ignore").replace("appartement T","").replace(".","").strip()+" pièce(s)"
            
        if tchamp["budget"]=="":
            motif_budget = re.compile(r"\d+..?\d+ €")
            #motif_budget = re.compile(r"\d+[\,\d+,..?\d+,\s\s?\d+]? €")
            corresp = motif_budget.search(tchamp["commentaire"])
            if corresp!=None:
                tchamp["budget"]=corresp.group().strip()
                print("corresp.group()****** :", corresp.group())
            else:
                motif_budget = re.compile(r"\d+ €")
                if corresp!=None:
                    corresp = motif_budget.search(tchamp["commentaire"])
                    tchamp["budget"]=corresp.group().strip()
                    print("corresp.group()****** :", corresp.group())
                else:
                    motif_budget = re.compile(r"\d+\s\s?\d+ €")  
                    corresp = motif_budget.search(tchamp["commentaire"])  
                    if corresp!=None:
                        tchamp["budget"]=corresp.group().strip()
                        print("corresp.group()****** :", corresp.group())
                        
        if tchamp["surface"]=="":
            print "miditra"
            motif_surface = re.compile(r"\d+..?\d+ m²")
           
            #motif_budget = re.compile(r"\d+[\,\d+,..?\d+,\s\s?\d+]? €")
            corresp = motif_surface.search(tchamp["commentaire"])
            if corresp!=None:
                tchamp["surface"]=corresp.group().strip()
                print("corresp.group()****** :", corresp.group())
            else:
                motif_surface = re.compile(r"\d+ m²")
                corresp = motif_surface.search(tchamp["commentaire"])
                if corresp!=None:
                    tchamp["surface"]=corresp.group().strip()
                    print("corresp.group()****** :", corresp.group())
               
        
        reload(sys)
        sys.setdefaultencoding("cp1252")                        
        str_sql=""
        for key, value in tchamp.iteritems():
            if value==None:
                value=""
            if key=="budget" and value!="":
                tchiffres=re.findall('\d+', value)
                value="".join(tchiffres)+value[len(value)-1:]
                    
            str_sql+=","+key+"='"+value.replace("'","''")+"'"
        
        sql="update edouard_denis_source_mail SET flag=1"+str_sql+ " WHERE date_extract::date >='2023-14-17' and edouard_denis_source_mail_id="+ str(edouard_denis_source_mail_id)
        #sql="update edouard_denis_source_mail SET "+str_sql[1:]+ " WHERE edouard_denis_source_mail_id="+ str(edouard_denis_source_mail_id)
        print sql
        curprod.execute(sql)
        prod.commit()
        
    except Exception as inst: 
        msgs=datetime.datetime.today().strftime('%Y%m%d %H:%M:%S')+'\n'
        msgs += 'erreur: '+ str(type(inst)) + '\n'
        msgs += 'CONTENU:' + str(inst) + '\n'
        print msgs
        fichierlog.write(msgs + '\n')
        
        prod.rollback() 
          
if os.path.exists(lock)==True:
    os.remove(lock) 
prod.close()  
fichierlog.close() 
                   
                   
                    
                
            
          
         

    



                    
    


