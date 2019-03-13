import requests
import logging
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
#Constants
HOF_URL = "https://www.baseball-reference.com/awards/hof.shtml"
BBR_PREFIX = "https://www.baseball-reference.com"
# LIST THAT WE WANT TO FILL
PLAYERS = []
POSITIONS = ["Catcher", "Pitcher", "Designated Hitter", "Centerfielder", "Rightfielder",
             "Leftfielder", "First Baseman", "Second Baseman", "Third Baseman", "Shortstop", "Outfielder" ]

OUTPUT_FILE = './players2.json'

def start_crawling():
    res = set()
    resp =  requests.get(HOF_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    hof_table = soup.find_all('tbody')[0]
    links = hof_table.find_all('a')
    for link in links:
        if '/players' in link['href']:
            res.add(link['href'])
    return res

def find_war_element(soup):
    element = soup.find('div', {'class' : 'stats_pullout'})
    return element

def find_image_element(soup):
    get_img = lambda x: x.find('img')
    return get_img(soup.find(id='meta'))


def create_data_object_from_link(link):
    '''create the data object from the link'''
    player = {}
    resp = requests.get(BBR_PREFIX + link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    meta = soup.find(id="meta")
    paragraphs = meta.find_all('p')
    elements = paragraphs
    WAR_Element = find_war_element(soup)
    img_element = find_image_element(soup)
    elements.append(WAR_Element)
    elements.append(img_element)
    for p in elements:
        parser = pick_parser(p)
        if parser is not None:
            entries = parse_element(parser, p)
            for entry in entries:
                player[entry] = entries[entry]
    return player
# parser is a function that returns a tuple of data
def parse_element(parser, element):
    return parser(element)

def pick_parser(element):
    label_el= element.find("strong")
    label = None
    if label_el is not None:
        label = label_el.getText()
    if label == "Career":
        label = element.getText()

    if label is not None:
        if "Full Name" in label:
            return full_name_parser
        elif "Position" in label:
            return positions_parser
        elif "Bats" in label:
            return bats_throws_parser
        elif "SUMMARY" in label:
            return stats_parser
        elif "Born" in label:
            return born_parser
        elif "Last Game" in label:
            return lg_parser
        elif "Rookie Status" in label:
            return rookie_parser
    else:
        if element.find('a') is not None and element.find('a').getText() == "View Player Bio":
            return bio_parser
        elif element.name == 'img':
            return image_parser

    return None

def full_name_parser(element):
    text = element.getText()
    return {"full_name": text.split(":")[1].strip()}

def positions_parser(element):
    text = element.getText()
    # print(text)
    # print([pos for pos in POSITIONS if pos in text])
    return {"positions": [pos for pos in POSITIONS if pos in text]}

def bats_throws_parser(element):
    text = element.getText()
    text = text.encode('ascii', errors='ignore').decode()
    text = ''.join(text.split())
    splt = text.split(':')
    throws = splt[2]
    bats = splt[1].replace("Throws", '')
    return {'bats' : bats, 'throws':throws}

def get_bio(bio_url):
    print(bio_url)
    resp = requests.get(bio_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    pars = soup.find_all('p')
    for p in pars:
        text = p.getText()
        if text is not None and len(text) > 100:
            if len(text) > 500:
                return text[:500]
            return text

def bio_parser(element):
    bio = get_bio(element.find('a')['href'])
    return {"bio" : bio}

def stats_parser(element):
    text = element.getText()
    splt = text.split()
    return {"WAR" : splt[3]}

def born_parser(element):
    text = element.getText()
    born_text = text.split(':')[1]
    born_text = ' '.join(born_text.split())

    return {'born' : born_text}

def lg_parser(element):
    text = element.getText()
    lg_text = text.split(':')[1]
    lg_text = ' '.join(lg_text.split())
    return {'last_game' : lg_text}

def rookie_parser(element):
    text = element.getText()
    rook_text = text.split(':')[1]
    rook_text = ' '.join(rook_text.split())
    return {'rookie_status' : rook_text}

def image_parser(element):
    return {'image_url' : element['src']}

def populate_players(links, n):
    for x in range(n):
        player = create_data_object_from_link(links.pop())
        if 'bio' in player:
            PLAYERS.append(player)

def dump_players():
    with open(OUTPUT_FILE, 'w') as out:
        json.dump(PLAYERS, out)

def add_player_ids():
    for ind, player in enumerate(PLAYERS):
        player['id'] = ind

def multiprocess_scrape(links, n):
    with Pool(5) as p:
        p.map(create_data_object_from_link, links[:4])

if __name__ == '__main__':
    #calls the other functions here
    links = start_crawling()
    # multiprocess_scrape(list(links), 3)
    populate_players(links, 45)

    add_player_ids()
    # print(PLAYERS)
    dump_players()
