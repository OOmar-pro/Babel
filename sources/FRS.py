import requests
import re
import json

from bs4 import BeautifulSoup
from fastapi import HTTPException
from utils.utils import formatToUrl, getSource

FRS = getSource('FRS')

def getLatests():
    r = requests.get(FRS['url_latests'])
    html = BeautifulSoup(r.text, 'html.parser')

    mangas = html.find('ul', class_='hot-thumbnails').find_all('li')
    
    res = []
    for item in mangas:
        res.append({
            "title": item.find('div', class_='manga-name').find('a').text,
            "slug": formatToUrl(item.find('div', class_='manga-name').find('a').text),
            "url": item.find('div', class_='manga-name').find('a')['href'],
            "img": "https:" + item.find('a', class_='thumbnail').find('img')['src']
        })

    return res

def getManga(title):
    title = formatToUrl(title)
    url = FRS['url_manga'].format(title)
    r = requests.get(url)
    
    if(r.status_code == 404):
        raise HTTPException(status_code=404, detail="Manga not found")

    html = BeautifulSoup(r.text, 'html.parser')

    manga = html.find('div', class_='wrapper')
    chapters_html = html.find('ul', class_='chapters').find_all('li')

    chapters = []
    for chapter in chapters_html:
        if not 'btn' in chapter['class']:
            chapters.append({
                "number": extractNumberFromText(chapter.find('a')['href']),
                "title": chapter.find('em').text,
                "url": chapter.find('a')['href'],
                "date": chapter.find('div', class_='date-chapter-title-rtl').text
            })

    res = {
        "metadata": {
            "img": manga.find('div', class_='boxed').find('img')['src'] ,
            "title": manga.find('h2', class_='widget-title').text,
            "description": manga.find('div', class_='well').find('p').text,
        },
        "chapters": chapters

    }

    return res

def getChapter(title, number):
    return "NOT DONE"

def search(query):
    return "NOT DONE"

def extractNumberFromText(text):
    return text.split('/')[-1]