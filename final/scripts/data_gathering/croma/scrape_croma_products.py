#!/usr/bin/env python3

# File name:
	# scrape_croma_products.py
# Description:
	# launches selenium in chrome browser to scrape croma products data
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
    # os, pandas , time, random, json
    # undetected_chromedriver 
    # warnings
# Dependency files
    # data/croma/croma_products_cleaned.csv
    # data/croma/croma_products_raw.csv
# Online resources
    # https://www.croma.com/ (for croma products)


from selenium import webdriver
import pandas as pd
import os
import time
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import warnings
import json


# function to scrape raw data from croma
def scrape_croma_products():
    #croma product brand urls
    croma_brand_urls = {"apple" : "https://www.croma.com/apple-iphones/bc/b-0025-97?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A97%3AmanufacturerAID%3Ab-0025%3AexcludeOOSFlag", 
                "samsung" : "https://www.croma.com/samsung-mobile-phones/bc/b-0328-10?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A10%3AmanufacturerAID%3Ab-0328%3AexcludeOOSFlag",
                "vivo" : "https://www.croma.com/vivo-android-phones/bc/b-0795-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0795%3AexcludeOOSFlag",
                "oneplus" : "https://www.croma.com/one-plus-android-phones/bc/b-0948-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0948%3AexcludeOOSFlag",
                "oppo" : "https://www.croma.com/oppo-android-phones/bc/b-0771-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0771%3AexcludeOOSFlag",
                "realme" : "https://www.croma.com/realme-android-phones/bc/b-1090-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-1090%3AexcludeOOSFlag",
                "nokia" : "https://www.croma.com/nokia-android-phones/bc/b-0267-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0267%3AexcludeOOSFlag"
                }

    options = webdriver.ChromeOptions() 
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    #no browser window is opened
    options.add_argument("--headless")
    #to avoid extra logs
    options.add_argument('log-level=3')
    browser = uc.Chrome(options=options)
    #browser waits only till all html elements are loaded(max 10 seconds)
    browser.implicitly_wait(10)

    croma_product_urls = []
    croma_product_ids = []

    print("Started scraping Croma product data")

    #fetching product urls and ids from each brand
    for brand_url in croma_brand_urls.values():
        browser.get(brand_url)
        #clicking on "View More" button repetitively to get load products of page

        try:
            close_button = browser.find_element_by_css_selector("#close")
            browser.execute_script("arguments[0].click();", close_button)
        except:
            pass
        
            
        while True:
            try:
                load_more_button = browser.find_element_by_css_selector(".view-more-div > button")
                browser.execute_script("arguments[0].click();", load_more_button)
            except NoSuchElementException:
                break

        brand_product_urls = browser.find_elements_by_css_selector('h3[class^="product-title"] > a')
        ids = browser.find_elements_by_css_selector('div[class="cp-product typ-plp"]')

        for id in ids:
            try:
                croma_product_ids.append(id.get_attribute('id'))
            except:
                croma_product_ids.append(None)
            
        for url in brand_product_urls:
            u = url.get_attribute('href')
            croma_product_urls.append(u)
    
    print("Total ",len(croma_product_urls), " Croma products to scrape")

    count = 0
    croma_product_names = []
    croma_product_mrps = []
    croma_product_prices = []
    croma_avg_ratings = []
    croma_total_no_of_ratings = []

    #fetching product info from each product url
    for item_url in croma_product_urls:
        count += 1
        browser.get(item_url)
        
        try:
            croma_product_names.append(browser.find_element_by_css_selector("h1.pd-title").text.strip())
        except NoSuchElementException:
            croma_product_names.append(None)

        try:
            croma_product_mrps.append("₹"+browser.find_element_by_css_selector("#old-price").text.strip())
        except:
            croma_product_mrps.append(None)
            
        try:
            croma_product_prices.append("₹"+browser.find_element_by_css_selector(".main-product-price>.new-price>.amount").text.strip())
        except:
            croma_product_prices.append(None)
            
        try:
            croma_avg_ratings.append(browser.find_element_by_css_selector(".info-item>.cp-rating .MuiRating-root").get_attribute("aria-label").strip().split(" ")[0])
        except:
            croma_avg_ratings.append(None)

        try:
            croma_total_no_of_ratings.append(browser.find_element_by_css_selector(".pr-review").text.split("Reviews")[0].strip())
        except:
            croma_total_no_of_ratings.append(None)  

        if(count % 10 == 0):
            print("Scraped ",count," products from Croma...")

    print("All ",len(croma_product_urls)," products scraped successfully!")

    columns = ['Product ID','Name','MRP','Price','Average Rating(5)','No. of Ratings', 'URL']

    #storing in dataframe
    croma_products = pd.DataFrame({
                                    'Product ID': croma_product_ids,
                                    'Name': croma_product_names,
                                    'MRP' : croma_product_mrps,
                                    'Price': croma_product_prices,
                                    'Average Rating(5)': croma_avg_ratings,
                                    'No. of Ratings': croma_total_no_of_ratings,
                                    'URL': croma_product_urls})[columns]

    #setting productID as index
    croma_products.set_index('Product ID', inplace=True)

    #drop duplicates
    croma_products.drop_duplicates()

    #saving raw data to csv
    croma_products.to_csv('data/croma/croma_products_raw.csv',encoding="utf-8-sig")

    print("Started cleaning scraped data from Croma")

    #data cleaning
    croma_products_cleaned = croma_products.rename(columns={'Average Rating(5)':'Average Rating (5)','Name': 'Product Name', 'MRP': 'Base Price (INR)', 'Price': 'Discounted Price (INR)', 'No. of Ratings': 'Number of Ratings'})
    if 'Product ID' in croma_products_cleaned.columns:
        del croma_products_cleaned['Product ID']
    #separating product variant from product name
    croma_products_variant_info = [v.split('(',1)[1].replace('(','').replace(')','') for v in croma_products_cleaned['Product Name'] if '(' in v]
    croma_products_cleaned['Product Name'] = [v.rsplit('(',1)[0] for v in croma_products_cleaned['Product Name']]
    croma_products_cleaned.insert(1,'Variant', croma_products_variant_info)
    indexes = []

    #swapping base price and discounted price when base price is None
    for product in croma_products_cleaned['Base Price (INR)'].iteritems():
            if type(product[1]) == float or product[1] is None:
                croma_products_cleaned['Base Price (INR)'][product[0]],croma_products_cleaned['Discounted Price (INR)'][product[0]] = croma_products_cleaned['Discounted Price (INR)'][product[0]],croma_products_cleaned['Base Price (INR)'][product[0]]
                indexes.append(product[0])

    croma_products_discount_percentages = []
    croma_products_base_prices = []
    croma_products_discounted_prices = []

    for product in croma_products_cleaned['Base Price (INR)'].iteritems():
        if type(product[1]) == float or product[1] is None:
            croma_products_base_prices.append(None)
        else:
            croma_products_base_prices.append(product[1].replace('₹','').replace(',',''))

    for product in croma_products_cleaned['Discounted Price (INR)'].iteritems():
        if type(product[1]) == float or product[1] is None:
            croma_products_discounted_prices.append(None)
        else:
            croma_products_discounted_prices.append(product[1].replace('₹','').replace(',',''))

    croma_products_cleaned['Base Price (INR)'] = croma_products_base_prices
    croma_products_cleaned['Discounted Price (INR)'] = croma_products_discounted_prices

    for item in croma_products_cleaned['Base Price (INR)'].iteritems():
        if (isinstance(item[1], type(None))) or (isinstance(croma_products_cleaned['Discounted Price (INR)'][item[0]], type(None))):
            croma_products_discount_percentages.append(None)
        else:
            disc_price = croma_products_cleaned['Discounted Price (INR)'][item[0]]
            if item[1].strip() == '' or disc_price.strip() == '':
                croma_products_discount_percentages.append(None)
            else:      
                croma_products_discount_percentages.append(int(((float(item[1]) - float(disc_price))/float(item[1])) * 100))

    croma_products_cleaned.insert(3,'Discount (%)',croma_products_discount_percentages)

    #saving cleaned data to csv
    croma_products_cleaned.to_csv('data/croma/croma_products_cleaned.csv')

    print("Cleaning completed for the scrapped data from Croma")

#run functions if file is run directly
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    scrape_croma_products()
 