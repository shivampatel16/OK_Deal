#!/usr/bin/env python3

# File name:
	# clean_amazon_reviews.py
# Description:
	# launches selenium in chrome browser to scrape amazon reviews data
# Scraping tool used:
	# Selenium
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# selenium > webdriver
    # webdriver_manager.chrome > ChromeDriverManager
    # selenium.common.exceptions > NoSuchElementException
    # selectorlib > Extractor
    # pandas , datetime, random, datetime,time 
    # clean_amazon_reviews > clean_amazon_reviews
    # warnings
# Dependency files
    # scripts/data_gathering/amazon/resources/search_results_reviews.yml
    # data/amazon/amazon_products_raw.csv
    # scripts/data_gathering/amazon/resources/search_results.yml
# Online resources
    # https://www.amazon.in/s?rh=n%3A1389432031&fs=true&ref=lp_1389432031_sar (for amazon products)

# Selenium algorithm learnt from (courtey): 
    # https://github.com/brenfrrs/selenium_and_pagination/blob/master/amazon_scraper.py

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import pandas as pd
from datetime import date
from random import randint
from time import sleep
from .clean_amazon_reviews import clean_amazon_reviews
import sys
import warnings

warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('log-level=3')
options.add_argument('--headless')


#method to scrape each page using an Extractor yml file
def scrape(url, driver, e):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    url = 'https://www.amazon.in' + url
    driver.get(url)
    driver.implicitly_wait(2)
    r = driver.page_source
    return e.extract(r)


# Method to scrape raw reviews (scrape raw reviews)
def step1_scrape_amazon_reviews():
    review_urls = []
    reviewed_product_id = []
    reviewed_product_name = []
    reviewer_name = []
    review_rating = []
    review_title = []
    review_details = []
    review_date = []
    review_helpful = []
   
    # Create an Extractor by reading from the YAML file
    e = Extractor.from_yaml_file('scripts/data_gathering/amazon/resources/search_results_reviews.yml')
    
    product_id = 0
    line_count = sum(1 for line in open('data/amazon/amazon_products_raw.csv', encoding="utf8"))
    print("\n\nTotal " + str(line_count) + " mobile specifications to scrape")
    
    scrape_counter = 0
    
    #open reviews file and scrape each url for reviews
    with open("data/amazon/amazon_products_raw.csv", 'r', encoding="utf8") as urllist:
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        
        for line in urllist.readlines()[1:]:
            scrape_counter += 1
            if (scrape_counter % 10 == 0):
                print("Scraped specifications of  " + str(scrape_counter) + "  mobiles from Amazon")

            # test few scrapes
            # if scrape_counter == 22:
            #    break

            line_split = line.split(',')
            url = line_split[-1]
            sleep(randint(0, 1))
            data = scrape(url, driver, e)

            if data and data['products'] != None:
                for product in data['products']:
                    try:
                        reviewed_product_name.append(line_split[1])
                    except:
                        print("name error")
                        reviewed_product_name.append(None)
                    try:
                        review_title.append(product['review_title'])
                    except:
                        print("title error")
                        review_title.append(None)
                    try:
                        review_rating.append(product['review_rating'])
                    except:
                        print("rating error")
                        review_rating.append(None)
                    try:
                        review_details.append(product['review_details'])
                    except:
                        review_details.append(None)
                    try:
                        reviewer_name.append(product['reviewer_name'])
                    except:
                        reviewer_name.append(None)

                    try:
                        review_date.append(product['review_date'])
                    except:
                        review_date.append(None)
                    try:
                        review_helpful.append(product['review_helpful'])
                    except:
                        print("review_helpful error")
                        review_helpful.append(None)

                    try:
                        review_urls.append('https://amazon.in' + url)
                    except:
                        print("review error")
                        review_urls.append(None)

                    try:
                        reviewed_product_id.append(str(product_id))
                    except:
                        print("Product ID error")
                        reviewed_product_id.append()
            else:
                print("data object is empty")
                pass
            product_id += 1

    a = {'ReviewedProductID': reviewed_product_id, 'ReviewedProduct Name': reviewed_product_name,
         'Reviewer Name': reviewer_name, 'Review Rating': review_rating, 'Review Title': review_title,
         'Review Details': review_details, 'Review Date': review_date, 'Review Helpful': review_helpful,
         'Review URL': review_urls}
    amazon_products_reviews = pd.DataFrame.from_dict(a, orient='index')
    amazon_products_reviews = amazon_products_reviews.transpose()

    amazon_products_reviews.to_excel('data/amazon/amazon_reviews_raw.xlsx', encoding="utf-8-sig")
    print("All " + str(
        scrape_counter) + " mobile specifications scraped successfully! \nAmazon data scrapping completed\n\n")

    driver.quit()

#scrapes reviews and cleans the reviews into csv file
def scrape_amazon_reviews():
    step1_scrape_amazon_reviews()
    clean_amazon_reviews()


######################## RUN CODE ##################

# scrape_amazon_reviews()
