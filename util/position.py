def obterPosicao():
    with open('token','rt') as f:
        return f.read()

def atualizarPosicao(posicao):
    with open('token','wt') as f:
        f.write(posicao)
        f.close()
    return posicao