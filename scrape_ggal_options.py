from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
from bs4 import BeautifulSoup
import datetime as dt
from logger import log
from store import save

name = 'ggal_options'
today = dt.datetime.today()
ggal_options_url='https://www.invertironline.com/titulo/cotizacion/BCBA/GGAL/GRUPO-FINANCIERO-GALICIA/opciones'

def getHtml(driverPath, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu') 

    driver=webdriver.Chrome(options=chrome_options, executable_path=driverPath)
    driver.get(url)
    html=driver.page_source
    driver.close()
    return html

def getOptionsData(soup):
    callBody=soup.find('tbody',attrs={'id':'tCallsListado'})
    putBody=soup.find('tbody',attrs={'id':'tPutsListado'})
    rows=callBody.find_all('tr')+putBody.find_all('tr')
    dataRows=[]
    for row in rows:
        name=row.find('a').text
        name=name[name.find('\n')+1:name.rfind('\n')]
        cells=row.find_all('td')
        price=float(cells[5].text.replace(',','.'))
        volume=int(cells[-3].text.replace('.',''))
        dataRows.append([name,price,volume])
    return dataRows

def getStockPrice(soup):
    tag=soup.find('span',{'data-field':'UltimoPrecio'})
    return float(tag.text.replace(',','.'))

def writeOptionsCsv(price,optionsData,file_name):
    for row in optionsData:
        save(file_name, f"{row[0]},{row[1]},{row[2]},{price},{today}\n", 'a+')

def scrapeGGALOptions():
    log(name, "SCRAPING GGAL OPTIONS")
    source=getHtml(config.webdriver_path, ggal_options_url)
    soup=BeautifulSoup(source, 'html.parser')
    optionsData=getOptionsData(soup)
    price=getStockPrice(soup)
    writeOptionsCsv(price,optionsData, 'GGALoptions.txt')


scrapeGGALOptions()