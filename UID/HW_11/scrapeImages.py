''' Scrapes images off a website '''
import requests
import requests
import logging
from bs4 import BeautifulSoup
import json

LOGOS_URL = 'http://www.sportslogos.net/teams/list_by_year/42019/2019_MLB_Logos/'

def start_crawling():
    resp =  requests.get(LOGOS_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return get_image_urls(soup)

def get_image_urls(soup):
    res = []
    logo_walls = soup.find_all('ul', {'class':'logoWall'})
    for logo_wall in logo_walls:
        img_tags = logo_wall.find_all('img')
        for img in img_tags:
            res.append(img['src'])
    return res


if __name__ == '__main__':
    urls = start_crawling()
    with open('/tmp/image_urls.txt', 'w') as out:
        for url in urls:
            out.write(url+'\n')
