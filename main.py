from fastapi import FastAPI, HTTPException
import json
import importlib

app = FastAPI()

@app.get('/')
async def root():
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()
    return res

@app.get('/{id}/')
async def source(id):
    source = getSource(id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    else:
        return source

@app.get('/{id}/latests/')
async def latests(id):
    source = getSource(id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.getLatests()


def getSource(id):
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()

    for source in res['sources']:
        if source['id'] == id:
            return source
    return None