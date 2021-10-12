import requests
from bs4 import BeautifulSoup

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
    url = RS['url_manga'] + title
    r = requests.get(url)
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
            "title": title,
            "description": manga.find('div', attrs={"itemprop": "description"}).text,
            "rating": manga.find('div', attrs={"itemprop": "ratingValue"}).text,
        },
        "chapters": chapters

    }

    return res

