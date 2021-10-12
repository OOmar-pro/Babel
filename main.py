from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

@app.get('/')
async def root():
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()
    return res

@app.get('/{id}/')
async def source(id):
    f = open('./sources.json',)
    res =  json.load(f)
    f.close()

    for source in res['sources']:
        if source['id'] == id:
            return source

    raise HTTPException(status_code=404, detail="Source not found.")
