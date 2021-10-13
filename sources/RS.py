import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

from utils.utils import formatToUrl, getSource

RS = getSource('RS')

def getLatests():
    r = requests.get(RS['url_latests'])
    html = BeautifulSoup(r.text, 'html.parser')

    mangas = html.find_all('div', class_='bs')
    
    res = []
    for item in mangas:
        res.append({
            "title": item.find('a')['title'],
            "slug": formatToUrl(item.find('a')['title']),
            "url": item.find('a')['href'],
            "img": item.find('img')['src'],
            "rating": item.find('div', class_='numscore').text
        })

    return res

def getManga(title):
    title = formatToUrl(title)
    url = RS['url_manga'].format(title)
    r = requests.get(url)
    if(r.status_code == 404):
        raise HTTPException(status_code=404, detail="Manga not found")

    html = BeautifulSoup(r.text, 'html.parser')

    manga = html.find('div', class_='main-info')
    chapters_html = html.find('div', id='chapterlist').find_all('li')

    chapters = []
    for chapter in chapters_html:
        chapters.append({
            "number": chapter['data-num'],
            "title": chapter.find('span', class_='chapternum').text,
            "url": chapter.find('a')['href'],
            "date": chapter.find('span', class_='chapterdate').text
        })

    res = {
        "metadata": {
            "img": manga.find('div', class_='info-left').find('img')['src'],
            "title": manga.find('h1', attrs={"itemprop": "name"}).text,
            "description": manga.find('div', attrs={"itemprop": "description"}).text,
            "rating": manga.find('div', attrs={"itemprop": "ratingValue"}).text,
        },
        "chapters": chapters

    }

    return res

def getChapter(title, number):
    slug = formatToUrl(title + " " + number)
    url = RS['url_chapter'].format(slug)
    r = requests.get(url)
    if(r.status_code == 404):
        raise HTTPException(status_code=404, detail="Chapter not found")

    html = BeautifulSoup(r.text, 'html.parser')

    pages_html = html.find('div', id='readerarea').find_all('img')

    pages = []
    i = 0
    for page in pages_html:
        i += 1
        pages.append(page['src'])

    return pages

def search(query):
    