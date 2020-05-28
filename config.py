import pathlib
import json

directory = pathlib.Path(__file__).parent.absolute()

webdriver_path = f"{directory}/chromedriver"

optionExpirationDates={
    'MY':'2020-5-15',
    'JU':'2020-6-19',
    'AG':'2020-8-21'
}

def get_config(key):
    with open(f"{directory}/config.json") as private_config:
        config = json.load(private_config)
        return config[key]