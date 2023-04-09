import pandas as pd
import io
import requests
import zipfile
import pandas as pd
import re
from pathlib import Path
import os
import wget
import time

#variables for loading
root = os.path.dirname("C:\\Users\\thgcn\\OneDrive\\Academico\\Mestrado - NLP - Finance\\datasets\\")

#Level one B3, CVM code
levelone = ['024600', '000906', '001210', '001325', '021199', '019348']
#Itau
#levelone = ['019348']



#functions
def busca_fre(ano):
    url = ('https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_%d.zip' %(ano))
    file = ('fre_cia_aberta_%d.zip' %(ano))    
    r = requests.get(url)
    zf = zipfile.ZipFile(io.BytesIO(r.content))   
    file = zf.namelist()  
    zf = zf.open(file[0])
    lines = zf.readlines()
    lines=[i.strip().decode('ISO-8859-1') for i in lines] 
    lines=[i.split(';') for i in lines]
    qtl = len(lines)
    #return pd.DataFrame(lines[1:], columns=lines[0])  
    return lines


def baixar_arquivo(url, endereco):
    headers = {
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
    }
    try: 
        resposta = requests.get(url, headers=headers, allow_redirects=True, verify=False, stream=True)
        #zf = zipfile.ZipFile(io.BytesIO(resposta.content))      
        if resposta.status_code == requests.codes.OK:
            file = zipfile.ZipFile(io.BytesIO(resposta.content))
            file.extractall(endereco)
            print("Download finalizado. Arquivo salvo em: {}".format(endereco))
        else:
            resposta.raise_for_status()
    except:
        time.sleep(30)
        resposta = requests.get(url, headers=headers, allow_redirects=True, verify=False, stream=True)
        #zf = zipfile.ZipFile(io.BytesIO(resposta.content))      
        if resposta.status_code == requests.codes.OK:
            file = zipfile.ZipFile(io.BytesIO(resposta.content))
            file.extractall(endereco)
            print("Download finalizado. Arquivo salvo em: {}".format(endereco))
        else:
            resposta.raise_for_status()

def main(year):
    #pega information
    lines = busca_fre(year)
    #Searches for Ata
    #defi = search(lines,"Dados Econômico-Financeiros")
    #search for url for download
    year = year
    for a in range(len(lines)):
    #for a in range(5):
     if lines[a][4] in levelone:
       sufix = re.sub(u'[^a-zA-Z0-9]','_',lines[a][4]+"_"+lines[a][3])
       category = re.sub(u'[^a-zA-Z0-9çãàáêéíõóú]','_',lines[a][5])
       version = re.sub(u'[^0-9]','',lines[a][2])
       print(sufix)
       company = os.path.join(root + "\\%s"%(sufix))
       print(company)
       if not Path(root + "\\%s"%(sufix)).is_dir():
            print("nao existe")
            os.makedirs(root + "\\%s"%(sufix))
       if not Path(company +"\\%d"%(year)).is_dir():
            print("nao existe")
            os.makedirs(company + "\\%d"%(year))
       diryear = os.path.join(company + "\\%d"%(year))
       if not Path(diryear +"\\%s"%(category)).is_dir():
            print("nao existe")
            os.makedirs(diryear + "\\%s"%(category))
       dircategory = os.path.join(diryear + "\\%s"%(category))
       url = lines[a][8]
       #choose a name for download
       nome = re.sub(u'[^a-zA-Z0-9]', '_', lines[a][3]+"_ID"+lines[a][6]+"_"+lines[a][5]+"_vers."+lines[a][2])[1:150]
       #download file 
       baixar_arquivo(url, dircategory)



main(2017)
main(2018)
main(2019)