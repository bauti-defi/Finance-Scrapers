#!/usr/bin/env python

import websocket
import json
import datetime
import requests
from main import market_close
from logger import log
import pathlib

##Scrapes live market data directly from Balanz websocket

directory = pathlib.Path(__file__).parent.absolute()
name = 'balanz_scraper'
config = get_config(balanz_scraper)

session = requests.session()
session.headers = {
    "Host":"clientes.balanz.com",
    "origin":"https://clientes.balanz.com/",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0",
    "cookie":"_ga=GA1.2.636383094.1586267490; _fbp=fb.1.1586267490167.578089430; __zlcmid=xbj2iCIJ4e5fED; _gid=GA1.2.1551867514.1587732483; _gat=1"
}

# Log in, get token from response
login_response = session.post('https://clientes.balanz.com/api/v1/login', data={
    "pass":config['pass'],
    "user":config['user']
}).json()
access_token = login_response['AccessToken']
session.close()


log(name, f"Access Token: {access_token}")

arg_dump=open(f"{directory}/data/arg.txt",'a')

def parse_message(message):
    message = json.loads(message)
    ticker = message['ticker']
    last_operated_price = message['u']
    total_volume = message['v']
    gmt_time = message['t']
    top_buy_offer = message['pc']
    top_buy_offer_volume = message['cc']
    top_sell_offer = message['pv']
    top_sell_offer_volume = message['cv']

    return f"{ticker},{last_operated_price},{total_volume},{top_buy_offer},{top_buy_offer_volume},{top_sell_offer},{top_sell_offer_volume},{gmt_time}\n"

def on_message(ws, message):
    #Close at market close
    if datetime.datetime.now() > market_close:
        print('[Balanz]: Market closed, shutting down.')
        arg_dump.close()
        ws.close()
    else:
        out = parse_message(message)
        arg_dump.write(out)


def on_error(ws, error):
    print(error)

def on_close(ws):
    arg_dump.close()
    print("[Balanz]: ### closed balanz stream ###")

def on_open(ws):
    print("[Balanz]: Connection established.")
    ws.send(json.dumps({"panel":0,"token":access_token}))
    ws.send(json.dumps({"idwatchlist":38852,"token":access_token}))

websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://clientes.balanz.com/websocket",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            on_open = on_open)
ws.run_forever()