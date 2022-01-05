#!/usr/bin/env python3

# File name:
	# currency_api.py
# Description:
	# extracts currencies and their conversion rates (to be used in application)
# Scraping tool used:
	# API
	# Requests
	# URLLIB
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
    # os, pandas , time, random, json, requests,
    # bs4 > BeautifulSoup
# Dependency files
    # data/currency_api/currency_conversion_api_data_raw.csv
    # data/currency_api/currency_conversion_api_data_cleaned.csv
# Online resources
	# We got the API key from https://exchangeratesapi.io/
    # http://api.exchangeratesapi.io/v1/latest?access_key=6d0fcb7e277f067cf8e00f452f61c5cd&format=1 (currency rates api)
    # https://www.easymarkets.com/int/learn-centre/discover-trading/currency-acronyms-and-abbreviations/ (scape currency abbrev)


# Imports 
import pandas as pd
import json
import urllib.request
import requests
from bs4 import BeautifulSoup

# method to grab currency rates
def currency_api():
    pd.set_option('display.max_rows', 250)

    # fetching data from the api
    print("Getting Currency rates data...")
    with urllib.request.urlopen("http://api.exchangeratesapi.io/v1/latest?access_key=6d0fcb7e277f067cf8e00f452f61c5cd&format=1") as url:
        data = json.loads(url.read().decode())
        
    rates = data.get('rates')
    currency_df = pd.DataFrame(rates.items(), columns=['currency', 'value'])

    print("Saving Currency rates data to a file...")
    currency_df.to_csv("data/currency_api/currency_conversion_api_data_raw.csv")

    # scraping currency-acronyms-and-abbreviations
    url="https://www.easymarkets.com/int/learn-centre/discover-trading/currency-acronyms-and-abbreviations/"

    bsync = requests.get(url).text
    soup = BeautifulSoup(bsync, "lxml")

    country_abbr_table = soup.find("table")

    print("Scraping Currency/Country Abbreviations...")
    country_abbr_df = pd.read_html(str(country_abbr_table))[0]

    print("Merging data...")
    merged_df = country_abbr_df.merge(currency_df, left_on='Acronym/AbbreviationAcr./Abb.', right_on='currency')
    merged_df = merged_df.drop(['Acronym/AbbreviationAcr./Abb.'], axis=1)

    print("Saving merged data to a file...")
    merged_df.to_csv("data/currency_api/currency_conversion_api_data_cleaned.csv")


# currency_api()
