from util import database
#from util import api
from util import web

query = []

lista = database.selecionarDisciplinas()

for disciplina in lista:
    query.append(disciplina[1])

for s in query:
    for i in range(0,10):
        param = {
            'subjectId':s,
            'pageNumber':i,
            'pageSize':10
        }
        url = 'https://api.passeidireto.com/api/Material/BrowseBySubject'
        initApi = web.InitApi(url=url,params=param)
        initApi.listaDeDocumentos()
        database.atualizarDisciplina(s)