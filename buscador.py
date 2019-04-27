import requests
import json as js
from util import json
from util import database
from util import position

while True:
    query = input('Nome da disciplina: ').lower()

    url = 'https://mobile-api.passeidireto.com/subject/search'

    header = json.obterHeader()
    posicao = int(position.obterPosicao())

    payload = {
        'q':query,
        'page': '0',
        'count': '16',
        'suggestQuery': 'true',
        'order': '1',
        'populateFollowers': 'true',
        'populateUniversityCount': 'true',
        'highlightPreTag': '<highlight>',
        'highlightPostTag': '</highlight>'
    }

    if(posicao < len(header['authorization'])):
        token = header['authorization'][posicao]
        posicao+=1
        position.atualizarPosicao(str(posicao))
    else:
        token = header['authorization'][0]
        position.atualizarPosicao(str(1))

    print('token =>',token)

    headers = {
        'accept': header['accept'],
        'app-version': header['app-version'],
        'client': header['client'],
        'authorization': token,
        'Accept-Encoding': header['Accept-Encoding'],
        'User-Agent': header['User-Agent']
    }

    response = requests.get(url=url,params=payload,headers=headers)


    if response.status_code == 200:
        resultados = js.loads(response.text, encoding='utf-8')

        if 'Results' in resultados:
            informacao = []
            for resultado in resultados['Results']:
                Id = resultado['Id']
                Name = str(resultado['Name']).replace('<highlight>', '').replace('</highlight>', '')
                Alias = resultado['Alias']
                Score = int(resultado['Score'])
                informacao = [Id,Name,Alias,Score]
                continuar = input(informacao[1]+' deseja continuar? sim> ').lower()
                if continuar != 'sim':
                    exit()
                break
            if database.selecionarDisciplina(Id) == 0:
                if database.inserirDisciplina(informacao=informacao) == 1:
                    print(informacao[1],'disciplina inserida...')
            else:
                print('disciplina já foi registrada')
