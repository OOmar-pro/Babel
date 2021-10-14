import json

def getSource(id):
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()

    for source in res['sources']:
        if source['id'] == id:
            return source
    return None

def formatToUrl(str):
    s = "-".join(str.split(' '))
    s = s.lower()
    s = s.replace('.', '')

    return s