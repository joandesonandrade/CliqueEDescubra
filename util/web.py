import requests
import json
from .database import inserirDocumento, selecionarDocumento
import mysql.connector

class InitApi(object):
    def __init__(self, url, params):
        self.url = url
        self.params = params

    def listaDeDocumentos(self):

        headers = {
            'Host': 'api.passeidireto.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.passeidireto.com/disciplina/calculo-i?ordem=3',
            'Authorization': 'f562db68b441c2e227ca58675af1431d',
            'Origin': 'https://www.passeidireto.com'
        }

        response = requests.get(self.url,headers=headers,params=self.params)
        resultado = json.loads(response.text)
        if len(resultado['Results']) == 0:
            print('[-] documentos vázios')
            return False

        total = 0
        for i in range(0,len(resultado['Results'])):
            tags = []
            informacoes = []
            objeto = resultado['Results'][i]

            try:
                Id = objeto['Id']
                Name = objeto['Name']
                Type = objeto['Type']
                Extension = objeto['Extension']
                FileUrl = objeto['AmazonId']
                Author_Id = objeto['AuthorId']
                Author_Name = objeto['AuthorName']
                Author_ImageUrl = objeto['AuthorImageUrl']
                Author_UniversityShortName = objeto['UniversityName']
                FilePreview = None#objeto['FilePreview']
                FilePreview_Id = -1#FilePreview['Id']
                FilePreview_FileId = -1#FilePreview['FileId']
                FilePreview_FolderUrl = objeto['AmazonId']#FilePreview['FolderUrl']
                FilePreview_PageCount = -1#FilePreview['PageCount']
                Subject_Id = objeto['SubjectId']
                Subject_Name = objeto['SubjectName']
                Subject_Alias = objeto['SubjectAlias']
                Tags = objeto['Tags']
                for tag in Tags:
                    IdTags = -1#tag['Id']
                    NameTags = tag['Name']
                    fullTag = [IdTags,NameTags]
                    tags.append(fullTag)
            except KeyError:
                print('[-] Informações quebradas')
                return ''


            informacoes.append([Id,Name,Type,Extension,FileUrl,Author_Id,Author_Name,Author_ImageUrl,Author_UniversityShortName,FilePreview_Id,FilePreview_FileId,FilePreview_FolderUrl,FilePreview_PageCount,Subject_Id,Subject_Name,Subject_Alias,tags])
            try:
                if selecionarDocumento(Id) == 0:
                    if inserirDocumento(informacoes) == 1:
                        print('[+]',Name,' inserido no banco de dados...')
                        total += 1
            except mysql.connector.errors.DatabaseError:
                print('Erro na codificação do conteúdo')
        print(f'{total} documentos adicionado')