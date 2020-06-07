import pathlib
import json

directory = pathlib.Path(__file__).parent.absolute()

webdriver_path = f"{directory}/chromedriver"

optionExpirationDates={
    'MY':'2020-5-15',
    'JU':'2020-6-19',
    'AG':'2020-8-21'
}

def read_config():
    with open(f"{directory}/config.json") as config:
        return json.load(config)

def write_config(newConfig):
    with open(f"{directory}/config.json", 'w+') as config:
        json.dump(newConfig, config)

def get_config(key):
    return read_config()[key]

def update_config(key, data):
    config = read_config()
    config[key] = data
    write_config(config)
