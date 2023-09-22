#!/usr/bin/env python
# -*- coding: cp1252  -*-

#try: 
#    from BeautifulSoup import BeautifulSoup
#except ImportError:
#    from bs4 import BeautifulSoup
#html = #the HTML code you've written above
#parsed_html = BeautifulSoup(html)
#print(parsed_html.body.find('div', attrs={'class':'container'}).text)


from email import message_from_file
from lxml import etree
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


def file_exists (f):
    """Checks whether extracted file was extracted before."""
    return os.path.exists(os.path.join(path, f))

def save_file (fn, cont):
    """Saves cont to a file fn"""
    file = open(os.path.join(path, fn), "wb")
    file.write(cont)
    file.close()

def construct_name (id, fn):
    """Constructs a file name out of messages ID and packed file name"""
    id = id.split(".")
    id = id[0]+id[1]
    return id+"."+fn

def disqo (s):
    """Removes double or single quotations."""
    s = s.strip()
    if s.startswith("'") and s.endswith("'"): return s[1:-1]
    if s.startswith('"') and s.endswith('"'): return s[1:-1]
    return s

def disgra (s):
    """Removes < and > from HTML-like tag or e-mail address or e-mail ID."""
    s = s.strip()
    if s.startswith("<") and s.endswith(">"): return s[1:-1]
    return s

def pullout (m, key):
    """Extracts content from an e-mail message.
    This works for multipart and nested multipart messages too.
    m   -- email.Message() or mailbox.Message()
    key -- Initial message ID (some string)
    Returns tuple(Text, Html, Files, Parts)
    Text  -- All text from all parts.
    Html  -- All HTMLs from all parts
    Files -- Dictionary mapping extracted file to message ID it belongs to.
    Parts -- Number of parts in original message.
    """
    Html = ""
    Text = ""
    Files = {}
    Parts = 0
    if not m.is_multipart():
        if m.get_filename(): # It's an attachment
            fn = m.get_filename()
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, None)
            if file_exists(cfn): return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
            return Text, Html, Files, 1
        # Not an attachment!
        # See where this belongs. Text, Html or some other data:
        cp = m.get_content_type()
        if cp=="text/plain": Text += m.get_payload(decode=True)
        elif cp=="text/html": Html += m.get_payload(decode=True)
        else:
            # Something else!
            # Extract a message ID and a file name if there is one:
            # This is some packed file and name is contained in content-type header
            # instead of content-disposition header explicitly
            cp = m.get("content-type")
            try: id = disgra(m.get("content-id"))
            except: id = None
            # Find file name:
            o = cp.find("name=")
            if o==-1: return Text, Html, Files, 1
            ox = cp.find(";", o)
            if ox==-1: ox = None
            o += 5; fn = cp[o:ox]
            fn = disqo(fn)
            cfn = construct_name(key, fn)
            Files[fn] = (cfn, id)
            if file_exists(cfn): return Text, Html, Files, 1
            save_file(cfn, m.get_payload(decode=True))
        return Text, Html, Files, 1
    # This IS a multipart message.
    # So, we iterate over it and call pullout() recursively for each part.
    y = 0
    while 1:
        # If we cannot get the payload, it means we hit the end:
        try:
            pl = m.get_payload(y)
        except: break
        # pl is a new Message object which goes back to pullout
        t, h, f, p = pullout(pl, key)
        Text += t; Html += h; Files.update(f); Parts += p
        y += 1
    #print "Text",Text
    #print "Html",Html
    #print "Files",Files
    return Text, Html, Files, Parts

def extract (msgfile, key):
    """Extracts all data from e-mail, including From, To, etc., and returns it as a dictionary.
    msgfile -- A file-like readable object
    key     -- Some ID string for that particular Message. Can be a file name or anything.
    Returns dict()
    Keys: from, to, subject, date, text, html, parts[, files]
    Key files will be present only when message contained binary files.
    For more see __doc__ for pullout() and caption() functions.
    """
    m = message_from_file(msgfile)
    From, To, Subject, Date = caption(m)
    Text, Html, Files, Parts = pullout(m, key)
    Text = Text.strip(); Html = Html.strip()
    
    
    #msg_html = {"html": Html}
    
    #Subject = base64.b64decode(Subject)
    
    print "From",From
    print "To",To
    print "Subject",Subject.encode("windows-1252").decode("utf-8")
    print "Date",Date
    
#    msg = {"subject": Subject, "from": From, "to": To, "date": Date,
#        "text": Text, "html": Html, "parts": Parts}
#        
#    if Files: msg["files"] = Files
    return Html

def caption (origin):
    """Extracts: To, From, Subject and Date from email.Message() or mailbox.Message()
    origin -- Message() object
    Returns tuple(From, To, Subject, Date)
    If message doesn't contain one/more of them, the empty strings will be returned.
    """
    Date = ""
    if origin.has_key("date"): Date = origin["date"].strip()
    From = ""
    if origin.has_key("from"): From = origin["from"].strip()
    To = ""
    if origin.has_key("to"): To = origin["to"].strip()
    Subject = ""
    if origin.has_key("subject"): Subject = origin["subject"].strip()
    return From, To, Subject, Date


def InitFields():
    chp_dict={}
    chp_dict["objet_mail"]=""
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

    sql="select * FROM edouard_denis_source_mail where date_creation::date >= '2022-07-27'::date and flag=0 and from_mail like '%myslpro@s.myselogerpro.com%'  order by edouard_denis_source_mail_id"
    #sql="select * FROM edouard_denis_source_mail where edouard_denis_source_mail_id='31134'"


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
        
        reload(sys)
        sys.setdefaultencoding("cp1252")
            
        
        f = open(file_ok["savedirpath_origine"]+"/"+file_ok["n_ima"], "rb")
        h = open(f.name.replace(".eml",".html"),'w')
        html_template = extract(f, f.name)
        h.write(html_template)
        f.close()
        h.close()
            
        
        #html_file=open("//mcserver2/recus$/2022-08-04/EDOUARD_DENIS/000000033067/"+file_ok["n_ima"].replace(".eml",".html"), 'r')  
            
        html_file = open(file_ok["savedirpath_origine"]+"/"+file_ok["n_ima"].replace(".eml",".html"), 'r')
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
        
        tchamp["objet_mail"]=soup.find("title").text.encode("cp1252","ignore").strip()
    

        #Check modele

      

#        tag_modele=soup.body.find('span', attrs={'style':'color:#3e4649;font-size:18px;font-family:Arial,Helvetica,sans-serif;line-height:22px;'})
#        print tag_modele
#        if tag_modele!=None:
#            type_modele=1
#        else:
#            type_modele=2
#        
#        if type_modele==1:

#            tag_infos_clients=soup.body.find_all('span', attrs={'style':'font-family:Arial, Helvetica, sans-serif;font-size:16px;color:#4c545f;'})
#            if len(tag_infos_clients)==2:
#               
#                telts_infos_client= tag_infos_clients[1].text.replace("Email","|Email").replace("Tél","|Tél").split("|")
#                tchamp["nom_client"]=telts_infos_client[0].split(":")[1].strip()
#                tchamp["mail"]=telts_infos_client[1].split(":")[1].strip()
#                tchamp["telephone"]=telts_infos_client[2].split(":")[1].replace("Indice d’activité","").strip()
#                if tchamp["telephone"][0:2]=='06':
#                    tchamp["tel_mobile"]=tchamp["telephone"]
#                    tchamp["telephone"]=""
#
#            if tchamp["tel_mobile"]=="" and tchamp["telephone"]=="":
#                tags_telephones=soup.body.find_all('a', attrs={'style':'background-color:#6a6eaa;border:1px solid #6a6eaa;border-radius:23px;color:#ffffff;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:175px;-webkit-text-size-adjust:none;mso-hide:all;'})
#                if len(tags_telephones)==2:
#                    tchamp["telephone"]=tags_telephones[1].text.strip()
#                    if tchamp["telephone"][0:2]=='06':
#                        tchamp["tel_mobile"]=tchamp["telephone"]
#                        tchamp["telephone"]=""
#                
#
#                
#            tag_budget=soup.body.find('span', attrs={'style':'color:#3e4649;font-size:18px;font-family:Arial;'})
#            print tag_budget
#            if tag_budget:
#                tchamp["budget"]=tag_budget.text
#                
#            tag_cpville=soup.body.find('span', attrs={'style':'color:#3e4649;font-size:14px;font-family:Arial, Helvetica, sans-serif;'})
#            if tag_cpville:
#                tchamp["ville"]=tag_cpville.text.split(",")[0].strip()
#                if len(tag_cpville.text.split(","))==2:
#                    tchamp["code_postal"]=tag_cpville.text.split(",")[1].strip()
#
#      
#            tag_bien=soup.body.find('span', attrs={'style':'font-family:Tahoma;font-size:12px;color:#000000;font-weight:normal;word-wrap:break-word;word-break:normal;text-align:left'})
#         
#            motif_piece = re.compile(r"\d+ pièce")
#            
#            if tag_bien:
#                ttag_bien=tag_bien.text.encode("cp1252","ignore").split("•")
#                tchamp["projet"]=ttag_bien[0].strip()
#                if len(tag_bien)==2:
#                        corresp=motif_piece.search(ttag_bien[1].strip().encode("cp1252","ignore"))
#                        if corresp!=None:
#                            tchamp["taille_logement"]="T "+re.sub("[^0-9]", "",corresp.group().encode("cp1252","ignore")).strip()
#                        else:
#                            tchamp["surface"]= ttag_bien[1].strip()
#            
#                elif len(tag_bien)==3:
#                    tchamp["taille_logement"]="T "+re.sub("[^0-9]", "",ttag_bien[1].encode("cp1252","ignore")).strip()
#                    tchamp["surface"]=ttag_bien[2].strip()
#                    
#            tag_commentaire=soup.body.find('span', attrs={'style':'font-family:Arial, Helvetica, sans-serif;font-size:16px;color:#4c545f;'})
#            if tag_commentaire:
#                tchamp["commentaire"]=tag_commentaire.text.strip()
#           
#
#
#        else:
  
        documentObjectModel = etree.HTML(str(soup))
        tag_nom_client=documentObjectModel.xpath('//span[@style="color:#3e4649;font-size:14px;font-family:Arial,Helvetica,sans-serif;line-height:22px;"]/strong')
        if tag_nom_client:
            tchamp["nom_client"]=tag_nom_client[0].text.strip()
            print tag_nom_client[0].text
     




        tag_mail_client=documentObjectModel.xpath('//span[@style="font-size:14px;font-weight:normal;"]')

        if tag_mail_client:
            tchamp["mail"]=tag_mail_client[0].text
        print tchamp["mail"]
      
        tags_telephones=documentObjectModel.xpath('//a[@style="text-decoration:none;color:#6a6eaa;"]')
        #tags_telephones=soup.body.find_all('a', attrs={'style':'text-decoration:none;color:#6a6eaa;'})
        if len(tags_telephones)==2:
            tchamp["telephone"]=tags_telephones[1].text.strip()
            if tchamp["telephone"]!="":        
                tchamp["telephone"]="0"+tchamp["telephone"].replace(" ","").replace("+33","0")[-9:]
            
            if tchamp["telephone"][0:2]=='06':
                tchamp["tel_mobile"]=tchamp["telephone"]
                tchamp["telephone"]=""
        print tchamp["tel_mobile"]
        print tchamp["telephone"]
      

        tag_programme=documentObjectModel.xpath('//span[@style="color:#4c545f;font-family:Arial, Helvetica, sans-serif;font-size:12px;"]')
        if tag_programme:
            
            print tag_programme[0].text.replace("Ref. du programme :","").strip()
            tchamp["code_programme"]=tag_programme[0].text.replace("Ref. du programme :","").strip()

        tag_budget=documentObjectModel.xpath('//span[@style="color:#4c545f;font-family:Arial, Helvetica, sans-serif;font-size:12px;"]/strong')
        
        if tag_budget:
            if tag_budget[0].text!=None:
                print tag_budget[0].text.encode("cp1252","ignore").strip()
                tchamp["budget"]=tag_budget[0].text.encode("cp1252","ignore").strip()

        

  
        tag_cpville_adresse=documentObjectModel.xpath('//td[@style="font-family:Tahoma;font-size:12px;color:#000000;font-weight:normal;word-wrap:break-word;word-break:normal;text-align:left"]')
        if tag_cpville_adresse:
            print tag_cpville_adresse[4].text
            if tag_cpville_adresse[4].text.find("(")!=-1:
                tchamp["code_postal"]=tag_cpville_adresse[4].text[tag_cpville_adresse[4].text.find("(")+1:tag_cpville_adresse[4].text.find(")")].strip()
                tchamp["ville"]=tag_cpville_adresse[4].text[0:tag_cpville_adresse[4].text.find("(")]
                tchamp["adresse"]=tag_cpville_adresse[4].text[tag_cpville_adresse[4].text.find(")")+1:].replace("-","").strip()
                print tchamp["code_postal"]
                print tchamp["ville"]
                print tchamp["adresse"]
            else:
               tchamp["ville"]=tag_cpville_adresse[4].text.strip()

                
        tag_programme=documentObjectModel.xpath('//td[@style="font-family:Tahoma;font-size:12px;color:#000000;font-weight:normal;word-wrap:break-word;word-break:normal;text-align:left"]/strong/span')
        if tag_programme:
           tchamp["programme"]=tag_programme[0].text
           print tchamp["programme"]
        
        tag_bien=documentObjectModel.xpath('//td[@style="font-family:Tahoma;font-size:12px;color:#000000;font-weight:normal;word-wrap:break-word;word-break:normal;text-align:left"]/strong')
 
        for c in tag_bien[0].getparent().iter():
            if c.tail!=None:
                print str(c.tail)
                for b in str(c.tail).split("•"):
                    b=b.strip(" ").encode("cp1252","ignore")
                    if b.strip().strip() in ["Appartement","Maison"]:
                        print "999"
                        tchamp["projet"]=b.strip()
                    elif b.strip().find("pièces")!=-1:
                        tchamp["taille_logement"]="T "+re.sub("[^0-9]", "",b.strip().encode("cp1252","ignore")).strip()
                    elif b.strip().find("m²")!=-1:
                        tchamp["surface"]=b.strip().encode("cp1252","ignore")
                    else:
                        print "888"
 
                        tchamp["destination"]=(tchamp["destination"]+"-"+b.strip().encode("cp1252","ignore"))
                        print tchamp["destination"]
                if tchamp["destination"]!="":
                    tchamp["destination"]=tchamp["destination"][1:]    

        print tchamp["destination"] , tchamp["projet"],  tchamp["taille_logement"], tchamp["surface"]
       
       
      
        tag_commentaire=soup.body.find('span', attrs={'style':'font-family:Arial, Helvetica, sans-serif;font-size:14px;color:#3e4649;'})
        if tag_commentaire:
            tchamp["commentaire"]=tag_commentaire.text.strip()
        
     
               
        
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
        
        sql="update edouard_denis_source_mail SET flag=1"+str_sql+ " WHERE edouard_denis_source_mail_id="+ str(edouard_denis_source_mail_id)
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
                   
                   
                    
                
            
          
         

    



                    
    


