

import yfinance as yf
import pandas as pd

aapl= yf.Ticker("AAPL")

aapl.info["marketCap"]






from ast import operator
from operator import index
import pandas as pd
from datetime import datetime, timedelta
import requests


# nejriv stahnu nova data za vcerejsek (uzaviraci hodnota)
source_website = "https://8marketcap.com/companies/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}
# Make a GET request to fetch the raw HTML content
html_content = requests.get(source_website, headers=headers).text
source = pd.read_html(html_content); source = source[0]

print(source)
scraped = pd.DataFrame(source)

import pandas as pd

# Představuji si, že jste data načetl(a) pomocí pandas. Pokud ne, můžete to udělat takto:
# scraped = pd.read_csv('path_to_your_file.csv')

# 1. Odstranění nepotřebných sloupců
scraped = scraped.drop(columns=['Unnamed: 0'])

# 2. Čištění sloupce `Market Cap`
def convert_market_cap(value):
    if 'T' in value:
        return float(value.replace('$', '').replace('T', '')) * 1e12
    elif 'B' in value:
        return float(value.replace('$', '').replace('B', '')) * 1e9
    else:
        return float(value.replace('$', ''))

scraped['Market Cap'] = scraped['Market Cap'].apply(convert_market_cap)

# 3. Čištění ostatních sloupců

scraped['Price'] = scraped['Price'].str.replace(',', '').str.replace('$', '').astype(float)

# 4. Manipulace s indexem
scraped.set_index('#', inplace=True)

scraped = scraped.drop(columns=['Price (30 days)','Symbol','24h','7d'])

scraped['Market Cap'] = scraped['Market Cap']/1000000000


def format_market_cap(value):
    if value % 1 == 0:  # Pokud je číslo celé (za tečkou je 0)
        return "{:,.0f}".format(value).replace(",", " ")
    else:
        return "{:,.2f}".format(value).replace(",", " ")  # Zde předpokládám, že chcete 2 desetinná místa

# Aplikujte na sloupec DataFrame
scraped['Market Cap'] = scraped['Market Cap'].apply(format_market_cap)

scraped.to_csv("final.csv",index=False)










