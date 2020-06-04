#!/usr/bin/env python

import json
import datetime
import requests
from logger import log
from config import get_config, update_config


config = get_config('balanz_scraper')

session = requests.session()
session.headers = {
    "Host":"clientes.balanz.com",
    "origin":"https://clientes.balanz.com/",
    "Connection":"keep-alive",
    'Accept-Enconding': 'gzip, deflate, br',
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Authorization": config['session-token']
}

def refreshSession():
    config['session-token'] = getToken()
    update_config('balanz_scraper',config)
    session.headers['Authorization'] = config['session-token']

def getToken():
    login_response = session.post('https://clientes.balanz.com/api/v1/login', data={ "pass":config['pass'], "user": config['user']}).json()
    if('idError' in login_response and 'Descripcion' in login_response):
        log('Balanz', login_response['Descripcion']) # Login limit exceded
        raise SystemExit
    return login_response['AccessToken']
