import datetime

def log(name, message):
    print(f"[{datetime.datetime.now()}][{name}]: {message}")