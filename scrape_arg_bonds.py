import requests
from bs4 import BeautifulSoup
from store import save
import datetime as dt
from logger import log

today = dt.datetime.today()
name = 'ARG Bonds'
bonds_url = "https://www.invertironline.com/mercado/cotizaciones/argentina/bonos/todos"

def get_html():
    response = requests.get(bonds_url)
    return response.content

def parse(soup):
    body = soup.find('tbody')
    rows = body.find_all('tr', attrs={"data-cantidad":1})
    bonds = []
    for row in rows:
        cells = row.find_all('td')
        bond = f"{cells[0].text.rstrip().lstrip()},"
        for c in cells[1:2]+cells[7:11]:
            bond += f"{parse_float(c.text.rstrip().lstrip())},"
        bond += f"{today}"
        bonds.append(bond)
    return bonds

def parse_float(text):
    return float(text.replace('.', '').replace(',','.'))

def write_to_dump(bonds,file_name):
    for bond in bonds:
        save(file_name, f"{bond}\n",'a+')

def scrape_bond_data():
    log(name, "SCRAPING ARG BONDS")
    source = get_html()
    soup=BeautifulSoup(source, 'html.parser')
    bonds = parse(soup)
    write_to_dump(bonds, 'argBonds.txt')


scrape_bond_data()