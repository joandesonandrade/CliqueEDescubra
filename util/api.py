import requests
import json
from .json import obterHeader
from .database import inserirDocumento, selecionarDocumento
import mysql.connector

class InitApi(object):
    def __init__(self, url):
        self.url = url

    def listaDeDocumentos(self):

        header = obterHeader()
        headers = {
            'accept': header['accept'],
            'app-version': header['app-version'],
            'client': header['client'],
            'authorization': header['authorization'],
            'Accept-Encoding': header['Accept-Encoding'],
            'User-Agent': header['User-Agent']
        }

        response = requests.get(self.url,headers=headers)
        resultado = json.loads(response.text)
        if len(resultado['materials']) == 0:
            print('[-] documentos vázios')
            return False

        total = 0
        for i in range(0,len(resultado['materials'])):
            tags = []
            informacoes = []
            objeto = resultado['materials'][i]
            Id = objeto['Id']
            Name = objeto['Name']
            Type = objeto['Type']
            Extension = objeto['Extension']
            FileUrl = objeto['FileUrl']
            Author = objeto['Author']
            Author_Id = Author['Id']
            Author_Name = Author['Name']
            Author_ImageUrl = Author['ImageUrl']
            Author_UniversityShortName = Author['UniversityShortName']
            FilePreview = objeto['FilePreview']
            FilePreview_Id = FilePreview['Id']
            FilePreview_FileId = FilePreview['FileId']
            FilePreview_FolderUrl = FilePreview['FolderUrl']
            FilePreview_PageCount = FilePreview['PageCount']
            Subject = objeto['Subject']
            Subject_Id = Subject['Id']
            Subject_Name = Subject['Name']
            Subject_Alias = Subject['Alias']
            Tags = objeto['Tags']
            for tag in Tags:
                IdTags = tag['Id']
                NameTags = tag['Name']
                fullTag = [IdTags,NameTags]
                tags.append(fullTag)
            informacoes.append([Id,Name,Type,Extension,FileUrl,Author_Id,Author_Name,Author_ImageUrl,Author_UniversityShortName,FilePreview_Id,FilePreview_FileId,FilePreview_FolderUrl,FilePreview_PageCount,Subject_Id,Subject_Name,Subject_Alias,tags])
            try:
                if selecionarDocumento(Id) == 0:
                    if inserirDocumento(informacoes) == 1:
                        print('[+]',Name,' inserido no banco de dados...')
                        total += 1
            except mysql.connector.errors.DatabaseError:
                print('Erro na codificação do conteúdo')
        print(f'{total} documentos adicionado')