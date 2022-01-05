#!/usr/bin/env python3

# File name:
	# clean_amazon_products.py
# Description:
	# launches selenium in chrome browser to scrape amazon products data
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
    # os, pandas , time, random
    # clean_amazon_products > step3_product_cleaning
    # warnings
# Dependency files
    # scripts/data_gathering/amazon/resources/search_results_urls.txt
    # data/amazon/amazon_products_raw.csv
    # scripts/data_gathering/amazon/resources/search_results.yml
# Online resources
    # https://www.amazon.in/s?rh=n%3A1389432031&fs=true&ref=lp_1389432031_sar (for amazon products)

# Selenium algorithm learnt from (courtey): 
    # https://github.com/brenfrrs/selenium_and_pagination/blob/master/amazon_scraper.py


# Imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import os
from random import randint
from time import sleep
import pandas as pd
from .clean_amazon_products import step3_product_cleaning
import warnings

# suppress warnings
warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('log-level=3')
options.add_argument('--headless')


####################################################
### Step 1 GETTING ALL (COUNT OF) PHONES TO BE SCRAPED
#####################################################


def step1_grab_phones_list():
    url_list = []

    # launch selenium to amazon.in Smartphones & Basic Mobiles
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get('https://www.amazon.in/s?rh=n%3A1389432031&fs=true&ref=lp_1389432031_sar')
    driver.implicitly_wait(5)

    # get first page_number
    try:
        num_page = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
    except NoSuchElementException:
        pass
        # num_page = driver.find_element_by_class_name('a-last').click()
    driver.implicitly_wait(3)

    for i in range(int(num_page.text)):  # To test few lines replace with "for i in range(int(num_page.text)-4,int(num_page.text)):"
        url_list.append(driver.current_url)
        driver.implicitly_wait(4)

    driver.quit()

    with open('scripts/data_gathering/amazon/resources/search_results_urls.txt', 'w+') as filehandle:
        for result_page in url_list:
            filehandle.write('%s\n' % result_page)

    line_count = sum(1 for line in open('scripts/data_gathering/amazon/resources/search_results_urls.txt'))
    print("\n\nTotal " + str(line_count) + " mobile specifications to scrape")


####################################################
###Step 2 SCRAPING ALL PHONES FROM AMAZON
#####################################################

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
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    driver.get(url)
    driver.implicitly_wait(3)
    r = driver.page_source
    return e.extract(r)


def step2_extract_amazon_products():
    name = []
    mrp = []
    price = []
    avg_rating = []
    total_no_of_ratings = []
    urls = []

    # Create an Extractor by reading from the YAML file
    e = Extractor.from_yaml_file('scripts/data_gathering/amazon/resources/search_results.yml')

    scrape_counter = 0
    with open("scripts/data_gathering/amazon/resources/search_results_urls.txt", 'r') as urllist:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print("\n\n")
        for url in urllist.read().splitlines():
            scrape_counter += 1

            # test few scrapes
            # if scrape_counter == 22:
            #    break

            if (scrape_counter % 10 == 0):
                print("Scraped specifications of  " + str(scrape_counter) + "  mobiles from Amazon")
            sleep(randint(0, 2))
            data = scrape(url, driver, e)
            if data and data['products'] != None:
                for product in data['products']:
                    try:
                        name.append(product['title'])
                    except:
                        print("name error")
                        name.append(None)
                    try:
                        price.append(product['price'])
                    except:
                        print("price error")
                        price.append(None)
                    try:
                        mrp.append(product['mrp'])
                    except:
                        print("mrp error")
                        mrp.append(None)
                    try:
                        urls.append(product['url'])
                    except:
                        urls.append(None)

                    try:
                        avg_rating.append(product['rating'])
                    except:
                        print("rating error")
                        avg_rating.append(None)

                    try:
                        total_no_of_ratings.append(product['reviews'])
                    except:
                        print("review error")
                        total_no_of_ratings.append(None)
            else:
                print("data object is empty")
                pass

    a = {'Name': name, 'MRP': mrp, 'Price': price, 'Average Rating(5)': avg_rating,
         'No. of Ratings': total_no_of_ratings,
         'URL': urls}
    amazon_products = pd.DataFrame.from_dict(a, orient='index')
    amazon_products = amazon_products.transpose()

    amazon_products.to_csv('data/amazon/amazon_products_raw.csv', encoding="utf-8-sig")
    print("All " + str(
        scrape_counter) + " mobile specifications scraped successfully! \nAmazon data scrapping completed\n\n")


# public method used to scrape and clean amazon products data.
def scrape_amazon_products():
    step1_grab_phones_list()
    step2_extract_amazon_products()
    step3_product_cleaning()  # clean extracted data


# scrape_amazon_products()
