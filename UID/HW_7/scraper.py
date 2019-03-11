import requests
import logging
from bs4 import BeautifulSoup
#Constants
HOF_URL = "https://www.baseball-reference.com/awards/hof.shtml"
BBR_PREFIX = "https://www.baseball-reference.com"
# LIST THAT WE WANT TO FILL
PLAYERS = {}
POSITIONS = ["Catcher", "Pitcher", "Designated Hitter", "Centerfielder", "Rightfielder",
             "Leftfielder", "First Baseman", "Second Baseman", "Third Baseman", "Shortstop", "Outfielder" ]

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
    divs = soup.find_all('div')
    for div in divs:
        if div.descendents is None:
            continue
        for desc in div.descendents:
            try:
                if "Wins Above Replacement" in div['data-tip']:
                    print("IM HERE")
                    print(div)
                    return div
            except KeyError as ke:
                continue

def create_data_object_from_link(link):
    '''create the data object from the link'''
    player = {}
    resp = requests.get(BBR_PREFIX + link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    meta = soup.find(id="meta")
    paragraphs = meta.find_all('p')
    elements = paragraphs
    WAR_Element = find_war_element(soup)
    for p in elements:
        parser = pick_parser(p)
        if parser is not None:
            entries = parse_element(parser, p)
            for entry in entries:
                player[entry] = entries[entry]

    print(player)
# parser is a function that returns a tuple of data
def parse_element(parser, element):
    return parser(element)

def pick_parser(element):
    label_el= element.find("strong")
    label = None
    if label_el is not None:
        label = label_el.getText()

    if label is not None:
        if "Full Name" in label:
            return full_name_parser
        elif "Position" in label:
            return positions_parser
        elif "Bats" in label:
            return bats_throws_parser
    else:
        if element.find('a') is not None and element.find('a').getText() == "View Player Bio":
            return bio_parser
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
if __name__ == '__main__':
    #calls the other functions here
    links = start_crawling()
    create_data_object_from_link(links.pop())



def WAR_parser(element):
    return {"WAR" : 0.0}
