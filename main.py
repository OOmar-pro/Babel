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

@app.get('/{source_id}/')
async def source(source_id):
    source = utils.getSource(source_id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    else:
        return source

@app.get('/{source_id}/latests/')
async def latests(source_id):
    source = utils.getSource(source_id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.getLatests()

@app.get('/{source_id}/search/')
async def latests(source_id):
    source = utils.getSource(source_id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.search()

@app.get('/{source_id}/{manga_title}')
async def manga(source_id,manga_title):
    source = utils.getSource(source_id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.getManga(manga_title)

@app.get('/{source_id}/{manga_title}/{chapter_number}')
async def chapter(source_id, manga_title, chapter_number):
    source = utils.getSource(source_id)
    if(source is None):
        raise HTTPException(status_code=404, detail="Source not found.")
    
    parser = importlib.import_module("sources.{}".format(source['id']))

    return parser.getChapter(manga_title, chapter_number)