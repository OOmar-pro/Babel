import json

def getSource(id):
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()

    for source in res:
        if source['id'] == id:
            return source
    return None

def formatToUrl(str):
    s = "-".join(str.split(' '))
    s = s.lower()
    s = s.replace('.', '')

    return s

def encodeUrl(url):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return url.replace(' ', '+')

def sanitize(text):
    return text.replace('\n', '').strip()