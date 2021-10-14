import requests
import re
import json

from bs4 import BeautifulSoup
from fastapi import HTTPException
from sources import LSV
from utils.utils import formatToUrl, getSource

LCS = getSource('LCS')

def getLatests():
    r = requests.get(LCS['url_latests'])
    html = BeautifulSoup(r.text, 'html.parser')

    mangas = html.find('div', class_='list').find_all('div', class_='group')
    
    res = []
    for item in mangas:
        res.append({
            "title": item.find('div', class_='title').find('a')['title'],
            "slug": formatToUrl(item.find('div', class_='title').find('a')['title']),
            "url": item.find('div', class_='title').find('a')['href'],
            "img": "" # TODO recuperer sur la page d'apres
        })

    return res

def getManga(title):
    title = formatToUrl(title)
    url = LCS['url_manga'].format(title)
    r = requests.get(url)
    
    if(r.status_code == 404):
        raise HTTPException(status_code=404, detail="Manga not found")

    html = BeautifulSoup(r.text, 'html.parser')

    manga = html.find('div', class_='comic')
    chapters_html = html.find('div', class_='list').find_all('div', class_='element')

    chapters = []
    for chapter in chapters_html:
        chapters.append({
            "number": extractNumberFromText(chapter.find('div', class_='title').find('a').text),
            "title": chapter.find('div', class_='title').find('a').text,
            "url": chapter.find('div', class_='title').find('a')['href'],
            "date": extractDateFromText(chapter.find('div', class_='meta_r').text)
        })

    res = {
        "metadata": {
            "img": manga.find('div', class_='thumbnail').find('img')['src'],
            "title": manga.find('h1', class_='title').text,
            "description": manga.find('div', class_='info').text,
        },
        "chapters": chapters

    }

    return res

def getChapter(title, number):
    url = LCS['url_chapter'].format(formatToUrl(title), number)
    r = requests.get(url)
    if(r.status_code == 404):
        raise HTTPException(status_code=404, detail="Chapter not found")

    html = BeautifulSoup(r.text, 'html.parser')
    pages_html = extractJson(html.text)

    pages = []
    i = 0
    for page in pages_html:
        i += 1
        pages.append(page['url'])

    return pages

def search(query):
    r = requests.post(LCS['url_search'], data={"search": query})
    html = BeautifulSoup(r.text, 'html.parser')

    mangas = html.find('div', class_='list').find_all('div', class_='group')
    
    res = []
    for item in mangas:
        res.append({
            "title": item.find('div', class_='title').find('a')['title'],
            "slug": formatToUrl(item.find('div', class_='title').find('a')['title']),
            "url": item.find('div', class_='title').find('a')['href'],
            "img": "" # TODO recuperer sur la page d'apres
        })

    return res

def extractNumberFromText(text):
    regex = r"Chapitre (\d+)"
    matches = re.findall(regex, text)

    return matches[0]

def extractDateFromText(text):
    regex = r"(\d+\.\d+\.\d+)"
    matches = re.findall(regex, text)

    if(len(matches) == 0):
        return 'Hier'
    return matches[0]

def extractJson(str):
   regex = r"var pages = (.+);"

   matches = re.findall(regex, str)
   res = json.loads(matches[0])

   return res