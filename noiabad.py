# -*-coding:utf-8-*-
from util import baixarArquivo as dwn
from util import api
from util import database
from multiprocessing import Process
import os

def runInThread(lista):
    url = 'https://mobile-api.passeidireto.com/file/download?fileId=' + str(lista[1]) + '&fileGuid=' + str(lista[5]) + '&useCloudFront=true'
    if os.path.isfile(str(lista[14])+'/'+str(lista[2]+'.'+str(lista[4]))) == True:
        print('[] arquivo já foi baixado')
        if database.atualizarDocumento(lista[1]) == True:
            if database.atualizarDocumento(lista[1]) == True:
                print('[+] inserido no banco')

    if baixarDocumento(url, lista[2], lista[14], lista[4], lista[1]) == True:
        if database.atualizarDocumento(lista[1]) == True:
            print(lista[2] + ' baixado com sucesso.')
            print('\n')

def listaDocumentos(url):
    lista = api.InitApi(url=url)
    lista.listaDeDocumentos()

def baixarDocumento(url, nome, subId, ext, id):
    baixar = dwn.baixar(url=url, nome=nome, subId=subId, ext=ext,id=id)
    return baixar.iniciar()[2]

listas = database.selecionarDocumentos()
baixando = []
for lista in listas:
    run = Process(target=runInThread,args=(lista,))
    run.start()
    run.join()
