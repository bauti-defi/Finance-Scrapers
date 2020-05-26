
import pathlib
import json

directory = pathlib.Path(__file__).parent.absolute()

def get_config(key):
    with open(f"{directory}/config.json") as private_config:
        config = json.load(private_config)
        return config[key]