from fastapi import FastAPI, HTTPException
import json
import importlib

from starlette.responses import FileResponse
from utils import utils

app = FastAPI()

@app.get('/')
async def root():
    return "Babel presentation"

@app.get('/list')
async def list():
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()
    return res

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('./assets/favicon.ico')

@app.get('/{id}/')
async def source(id):
    source = utils.getSource(id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    else:
        return source

@app.get('/{id}/latests/')
async def latests(id):
    source = utils.getSource(id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.getLatests()
