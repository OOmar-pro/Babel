import requests
from bs4 import BeautifulSoup

from utils.utils import getSource

RS = getSource('RS')

def getLatests():
    r = requests.get(RS['url_latests'])
    html = BeautifulSoup(r.text, 'html.parser')

    mangas = html.find_all('div', class_='bs')
    
    res = []
    for item in mangas:
        res.append({
            "title": item.find('a')['title'],
            "url": item.find('a')['href'],
            "img": item.find('img')['src'],
            "rating": item.find('div', class_='numscore').text
        })

    return res
