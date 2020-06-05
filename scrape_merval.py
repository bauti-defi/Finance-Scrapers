
import balanz
from store import save
from logger import log
import json
import datetime

name = "Merval Scraper"
def scrape(url, file, parser, attempts):
    if(attempts > 3):
        log(name, 'Failure, too many attempts')

    response = balanz.session.get(url)
    if(response.status_code == 401 or response.status_code == 403):
        log(name, 'Auth Error!')
        balanz.refreshSession()
        scrape(url, file, parser, attempts+1)
    elif(response.status_code == 200):
        data = json.loads(response.content)['cotizaciones']
        data = [*map(parser, data)]
        dump = '\n'.join(data)
        save(file, dump, 'a+') #change to dump

def parseBit(key, data):
    return data[key] if key in data else ''

#Columns are the same for all... structure:
#'ticker', 'plazo', 'max', 'min', 'open', 'last_op','total_volume','datetime', cc-cc5, cv-cv5, pc-pc5, pv-pv5
#cc = cantidad de compra 
#cv = cantidad de venta
#pc = precio de compra
#pv = precio de venta
#pc and pv are in descending order => pc > pc2 > pc3 > p4 > pc5
def parse(data):
    time = datetime.datetime.utcfromtimestamp(data['t']/1000) #from ms to seconds
    return f"{parseBit('ticker', data)},{parseBit('plazo', data)},{parseBit('max', data)},{parseBit('min', data)},{parseBit('ap', data)},{parseBit('u', data)},{parseBit('v', data)},{time},{parseBit('cc', data)},{parseBit('cc2', data)},{parseBit('cc3', data)},{parseBit('cc4', data)},{parseBit('cc5', data)},{parseBit('cv', data)},{parseBit('cv2', data)},{parseBit('cv3', data)},{parseBit('cv4', data)},{parseBit('cv5', data)},{parseBit('pc', data)},{parseBit('pc2', data)},{parseBit('pc3', data)},{parseBit('pc4', data)},{parseBit('pc5', data)},{parseBit('pv', data)},{parseBit('pv2', data)},{parseBit('pv3', data)},{parseBit('pv4', data)},{parseBit('pv5', data)}"


log(name, 'Scraping Stocks')
scrape('https://clientes.balanz.com/api/v1/cotizaciones/acciones/1?token=0&tokenindice=0', 'ArgStocks.txt', parse, 0)
log(name, 'Stocks Saved.')

log(name, 'Scraping CEDEARS')
scrape('https://clientes.balanz.com/api/v1/cotizaciones/cedears?token=0', 'ArgCEDEARS.txt', parse, 0)
log(name, 'CEDEARS Saved.')

log(name, 'Scraping Bonds')
scrape('https://clientes.balanz.com/api/v1/cotizaciones/panel/23?token=0', 'ArgBonds.txt', parse, 0)
log(name, 'Bonds Saved.')

log(name, 'Scraping Options')
scrape('https://clientes.balanz.com/api/v1/cotizaciones/opciones?token=0', 'ArgOptions.txt', parse, 0)
log(name, 'Options Saved.')

log(name, 'Scraping Futures')
scrape('https://clientes.balanz.com/api/v1/cotizaciones/panel/9?token=0', 'ArgFutures.txt', parse, 0)
log(name, 'Futures Saved.')