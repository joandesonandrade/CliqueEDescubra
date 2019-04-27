import requests
import os
from .json import obterHeader
import random
from clint.textui import progress
from util import position
import math
import json
from util import database as db

class baixar(object):
    def __init__(self, url, nome, subId, ext, id=None):
        self.url = url
        self.nome = nome
        self.subId = subId
        self.ext = ext
        self.id = id
        self.headers = obterHeader()
        with open('googleIdToken','rt') as f:
            self.googleIdToken = f.read()
            f.close()
        with open('facebookToken','rt') as f:
            self.facebookToken = f.read()
            f.close()


    def obterNovoToken(self,tipoToken='google'):
        if tipoToken == 'google':
            Jsondata = {
                'googleIdToken': self.googleIdToken
            }
        else:
            Jsondata = {
                'facebookToken':self.facebookToken,
                'email':'null'
            }
        headers = {
            'Content-Type':'application/json; charset=utf-8',
            'accept': self.headers['accept'],
            'app-version': self.headers['app-version'],
            'client': self.headers['client'],
            'authorization': 'undefined',
            'Accept-Encoding': self.headers['Accept-Encoding'],
            'User-Agent': self.headers['User-Agent']
        }
        resposta = requests.post('https://mobile-api.passeidireto.com/account/google-login',headers=headers,json=Jsondata)
        try:
            return json.loads(resposta.text)['sessionKey']
        except KeyError:
            print('Erro:',json.loads(resposta.text)['code'])
            return ''

    def iniciar(self):
        # obtendo informações do link
        print('baixando',self.nome,'...')

        lat = position.obterPosicao()
        if lat == '':
            lat = 0
            position.atualizarPosicao(lat)

        posicao = int(lat)

        tokens = []
        for tokken in self.headers['authorization']:
            tokens.append(tokken)

        if (posicao < len(self.headers['authorization'])):
            token = tokens[posicao]
            posicao += 1
            position.atualizarPosicao(str(posicao))
        else:
            token = tokens[0]
            position.atualizarPosicao(str(1))

        print('Quantidade de tokens:',len(tokens))
        print('token =>', token)

        headers = {
            'accept': self.headers['accept'],
            'app-version': self.headers['app-version'],
            'client': self.headers['client'],
            'authorization': token,
            'Accept-Encoding': self.headers['Accept-Encoding'],
            'User-Agent': self.headers['User-Agent']
        }
        try:
            response = requests.get(self.url, headers=headers)

            if 'blocked' in response.text:
                #print(response.text)
                print(json.loads(response.text)['message'])
                '''novoToken = baixar.obterNovoToken(self)
                if novoToken == '':
                    novoToken = baixar.obterNovoToken(self,tipoToken='facebook')
                    if novoToken == '':
                        return '', '', False
                else:
                    with open('headears.json','rt') as r:
                        rt = r.read()
                        r.close()
                    novottToken = rt.replace('"],','","'+novoToken+'"],')
                    with open('headears.json','wt') as w:
                        w.write(novottToken)
                        w.close()
                    token = novoToken
                #time.sleep(1*60*60)'''
                return  '','',False


        except requests.exceptions.Timeout:
            print('[-] problema no download: Timeout')
            return '', '', False

        if response.status_code == 200:

            try:

                response = requests.get(response.text.replace('"',''),stream=True)
                dir = 'documentos/' + str(self.subId) + '/'
                if not os.path.isdir(dir):
                    os.mkdir(dir)

                if os.path.isfile(dir + self.nome.replace('/', '-').replace('\/', '-') + self.ext):
                    fullpath = dir + self.nome.replace('/', '-').replace('\/', '-') + str(
                        random.randint(0, 99999999)) + self.ext
                else:
                    fullpath = dir + self.nome.replace('/', '-').replace('\/', '-') + self.ext

                tamanho = int(response.headers.get('content-length'))
                if (int(math.ceil(tamanho / 1024 / 1024)) + 1) > 15:
                    if self.id != None:
                        db.atualizarSizeDocumento(self.id,tamanho)
                    print('[-] Tamanho do arquivo ultrapassa 15MB')

                    return '', '', False

                with open(fullpath, 'wb') as f:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(tamanho / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()

                '''with open(fullpath,'wb') as f:
                    f.write(response.content)
                    f.close()'''

                return fullpath, id, True

            except requests.exceptions.Timeout:
                print('[-] problema no download: Timeout')
                return '', '', False

        else:
            problema = json.loads(response.text)
            print(f'[-] {response.status_code} problema no download:',problema['message'])
            if(problema['message'] == 'Not Found'):
                db.atualizarSizeDocumento(self.id, -1)

            return '','',False
