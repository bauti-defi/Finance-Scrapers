###PIP INSTALL REMINDER
Remember to `sudo -H pip install <package-name>` for crontab capability on Ubuntu Server 18.04

###REMEMBER TO HANDLE ASSEMBLE THE CONFIG
The config should be stored in the root directory as `config.json`.
It's contents are a JSON Object like the following:

```{
  "alpha_scraper": {
    "api_key": "your key",
    "scrape_symbols": ["GGAL", "BBAR", "GOLD"]
  }
}
```

##ALPHA SCRAPER
packages to pip install: requests

##BALANZ SCRAPER
packages to pip install: requests, websockets
