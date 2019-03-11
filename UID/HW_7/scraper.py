import requests
import logging
from bs4 import BeautifulSoup
#Constants
HOF_URL = "https://www.baseball-reference.com/awards/hof.shtml"
BBR_PREFIX = "https://www.baseball-reference.com"
# LIST THAT WE WANT TO FILL
PLAYERS = {}

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

def create_data_object_from_link(link):
    '''create the data object from the link'''
    player = {}
    resp = requests.get(BBR_PREFIX + link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    meta = soup.find(id="meta")
    paragraphs = meta.find_all('p')
    for p in paragraphs:
        parser = pick_parser(p)
        if parser is not None:
            prop, value = parse_element(parser, p)
            player[prop] = value

# parser is a function that returns a tuple of data
def parse_element(parser, element):
    return parser(element)

def pick_parser(element):
    label = element.find("strong")
    if label == None:
        return None
    if "Full Name" in label.getText():
        return full_name_parser


def full_name_parser(element):
    text = element.getText()
    return "full_name", text.split(":")[1].strip()




if __name__ == '__main__':
    #calls the other functions here
    links = start_crawling()
    create_data_object_from_link(links.pop())
