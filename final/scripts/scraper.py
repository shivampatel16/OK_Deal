# File name:
	# scraper.py
# Description:
	# creates functions for all products, review, tweets and currency scraping actions (to be used in main application)
# Names of group members:  
       # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# main.py
# Other modules the file import:
    # .data_gathering.amazon > scrape_amazon_products as sap
    # .data_gathering.amazon > scrape_amazon_reviews as sar
    # Flipkart
    # .data_gathering.flipkart > scrape_flipkart_products as sfp
    # .data_gathering.flipkart > scrape_flipkart_reviews as sfr
    # Croma
    # .data_gathering.croma > scrape_croma_products as scp
    # .data_gathering.croma > scrape_croma_reviews as scr
    # PhoneArena
    # .data_gathering.phonearena > scrape_phonearena as spa
    # Tweets
    # .data_gathering.twitter > scrape_tweets as stw
    # .data_gathering.twitter > clean_tweets as ctw
    # Currency API
    # .data_gathering.currency > currency_api as ca
# Dependency files
    # none
# Online resources
    # none


# Amazon
from .data_gathering.amazon import scrape_amazon_products as sap
from .data_gathering.amazon import scrape_amazon_reviews as sar
# Flipkart
from .data_gathering.flipkart import scrape_flipkart_products as sfp
from .data_gathering.flipkart import scrape_flipkart_reviews as sfr
# Croma
from .data_gathering.croma import scrape_croma_products as scp
from .data_gathering.croma import scrape_croma_reviews as scr
# PhoneArena
from .data_gathering.phonearena import scrape_phonearena as spa
# Tweets
from .data_gathering.twitter import scrape_tweets as stw
from .data_gathering.twitter import clean_tweets as ctw
# Currency API
from .data_gathering.currency import currency_api as ca

# UI 1.1.1
def scrape_amazon_products():
	sap.scrape_amazon_products()

# UI 1.1.2
def scrape_flipkart_products():
    sfp.scrape_flipkart_products()

# UI 1.1.3
def scrape_croma_products():
    scp.scrape_croma_products()

# UI 1.2.1
def scrape_amazon_reviews():
    sar.scrape_amazon_reviews()

# UI 1.2.2
def scrape_flipkart_reviews():
    sfr.scrape_flipkart_reviews()

# UI 1.2.3
def scrape_croma_reviews():
    scr.scrape_croma_reviews()

# UI 1.3
def scrape_phonearena_specifications():
    spa.scrape_phonearena()

# UI 1.4
def scrape_twitter_tweets():
    stw.scrape_tweets()
    ctw.clean_tweets()

# UI 1.5
def scrape_currency_conversion_rates():
    ca.currency_api()
