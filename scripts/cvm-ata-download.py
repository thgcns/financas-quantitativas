import pandas as pd
import io
import requests
import zipfile
import pandas as pd
import re
from pathlib import Path
import os

#variables for loading
root = os.path.dirname("C:\\Users\\thgcn\\OneDrive\\Academico\\Mestrado - NLP - Finance\\datasets\\")

#Level one B3, CVM code
levelone = ['10456', '24600', '906', '1210', '1325', '21199', '18724', '4820', '2437', '2453', '3069', '3077', '18376', '16632', '5770', '6211', '3980', '8672', '19348', '7617', '8656', '11312', '14109', '14320']



#functions
def busca_ipe(ano):
    url = ('https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_%d.zip' %(ano))
    file = ('ipe_cia_aberta_%d.zip' %(ano))    
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


def search (lista, valor):
    return [(lista[lista.index(x)]) for x in lista if valor in x]


def baixar_arquivo(url, endereco):
    resposta = requests.get(url, allow_redirects=True, verify=False, stream=True)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
        print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()
        

def main(year):
    #pega information
    lines = busca_ipe(year)
    #Searches for Ata
    age = search(lines, "Ata")
    #search for url for download
    year = year
    for a in range(len(age)):
    #for a in range(5):
     if(age[a][2]) in levelone:
       sufix = re.sub(u'[^a-zA-Z0-9]','_',age[a][2]+"_"+age[a][1])
       category = re.sub(u'[^a-zA-Z0-9ãçàá]','_',age[a][4])
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
       url = age[a][12]
       #choose a name for download
       nome = re.sub(u'[^a-zA-Z0-9]', '_', age[a][2]+"_"+age[a][1]+"_"+age[a][7][1:100]+"_"+age[a][8])[1:100]
       #download file 
       baixar_arquivo(url, dircategory+"\\%s.pdf"%(nome))


main(2019)
main(2020)
main(2021)
main(2022)