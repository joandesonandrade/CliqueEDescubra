import json

def obterHeader():
    with open('headears.json', 'rt') as f:
        r = f.read()
        f.close()
    header = json.loads(r, encoding='utf-8')
    return header