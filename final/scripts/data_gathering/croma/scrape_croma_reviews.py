#!/usr/bin/env python3

# File name:
	# scrape_croma_reviews.py
# Description:
	# launches selenium in chrome browser to scrape croma reviews data
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
    # requests
# Dependency files
    # data/croma/croma_reviews_raw.csv
    # data/croma/croma_reviews_cleaned.csv
    # data/croma/croma_reviews_cleaned.json
# Online resources
    # https://api.croma.com/productdetail/allchannels/v1/review/ (for croma products)


# imports
import requests
from selenium import webdriver
import pandas as pd
import json
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import time
import warnings
warnings.filterwarnings("ignore")


# Function to scrape croma products
def scrape_croma_reviews():

    croma_url = "https://www.croma.com"

    brand_urls = {
        "apple": "https://www.croma.com/apple-iphones/bc/b-0025-97?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A97%3AmanufacturerAID%3Ab-0025%3AexcludeOOSFlag",
        "samsung": "https://www.croma.com/samsung-mobile-phones/bc/b-0328-10?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A10%3AmanufacturerAID%3Ab-0328%3AexcludeOOSFlag",
        "vivo": "https://www.croma.com/vivo-android-phones/bc/b-0795-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0795%3AexcludeOOSFlag",
        "oneplus": "https://www.croma.com/one-plus-android-phones/bc/b-0948-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0948%3AexcludeOOSFlag",
        "oppo": "https://www.croma.com/oppo-android-phones/bc/b-0771-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0771%3AexcludeOOSFlag",
        "realme": "https://www.croma.com/realme-android-phones/bc/b-1090-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-1090%3AexcludeOOSFlag",
        "nokia": "https://www.croma.com/nokia-android-phones/bc/b-0267-95?q=%3Arelevance%3AZAStatusFlag%3Atrue%3AskuStockFlag%3Atrue%3AallCategories%3A95%3AmanufacturerAID%3Ab-0267%3AexcludeOOSFlag"
        }

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('log-level=3')
    browser = uc.Chrome(options=options)
    browser.implicitly_wait(10)  # seconds

    product_urls = []
    product_id = []

    print("Searching how many products to get reviews from Croma")

    for brand_url in brand_urls.values():
        browser.get(brand_url)

        close_popup_buttons = browser.find_elements_by_id("close")
        for close_popup_button in close_popup_buttons:
            close_popup_button.click()

        time.sleep(3)

        while True:
            try:
                load_more_button = browser.find_element_by_css_selector(".view-more-div > button")
                load_more_button.click()
            except NoSuchElementException:
                break

        ids = browser.find_elements_by_css_selector('div[class="cp-product typ-plp"]')
        for id in ids:
            try:
                product_id.append(id.get_attribute('id'))
            except:
                product_id.append(None)

    print("Total products: ", len(product_id))

    reviewed_product_id = []
    reviewed_product_name = []
    reviewer_name = []
    review_rating = []
    review_title = []
    review_details = []
    review_date = []
    review_helpful = []

    print("Croma reviews scraping starts......")
    count_page = 1
    for id in product_id:

        if (count_page % 10 == 0):
            print("Scraped ", count_page , " product reviews from Croma")
        
        count_page += 1

        browser.get('https://www.croma.com/search?q=' + id + '%3ALatestArrival%3AexcludeOOSFlag&text=' + id)

        try:
            product_name = browser.find_element_by_css_selector('.product-title>a').text.strip()
        except NoSuchElementException:
            product_name = None

        response = requests.get('https://api.croma.com/productdetail/allchannels/v1/review/' + id)
        response_json = response.json()
        reviews = response_json['reviews']
        product_names = [product_name] * len(reviews)
        product_ids = [id] * len(reviews)
        reviewed_product_name.extend(product_names)
        reviewed_product_id.extend(product_ids)

        for review in reviews:
            try:
                reviewer_name.append(review['alias'])
            except:
                reviewer_name.append(None)

            try:
                review_rating.append(review['rating'])
            except:
                review_rating.append(None)

            try:
                review_details.append(review['comment'])
            except:
                review_details.append(None)

            try:
                review_date.append(review['date'])
            except:
                review_date.append(None)


    browser.quit()

    print("All ", len(product_id) , " products' reviews from Croma scraped successfully!")

    columns_reviews = ['ReviewedProduct ID', 'ReviewedProduct Name', 'Reviewer Name', 'Review Rating', 'Review Title',
                    'Review Details', 'Review Date', 'Review Helpful']

    review_title = [None] * len(review_details)
    review_helpful = review_title

    croma_products_review_df = pd.DataFrame({
        'ReviewedProduct ID': reviewed_product_id,
        'ReviewedProduct Name': reviewed_product_name,
        'Reviewer Name': reviewer_name,
        'Review Rating': review_rating,
        'Review Title': review_title,
        'Review Details': review_details,
        'Review Date': review_date,
        'Review Helpful': review_helpful
    })[columns_reviews]

    croma_products_review_df.set_index('ReviewedProduct ID', inplace=True)
    croma_products_review_df.to_csv('data/croma/croma_reviews_raw.csv',encoding='utf-8')

    print("Croma reviews cleaning starts......")

    all_reviews = []

    for index, row in croma_products_review_df.iterrows():
        review = []

        if row['ReviewedProduct Name'] is None:
            continue
        reviewed_product_name_clean = row['ReviewedProduct Name'].split('(',1)[0].strip().lower()

        review_date = (row['Review Date'].split('T')[0] if type(row['Review Date']) == str else 'Invalid date')
        # users = (row['Review Helpful'] if type(row['Review Helpful']) == int  else 0)
        # popularity_score = (row['Review Rating'] * row['Review Helpful'] if row['Review Helpful'] else 'NaN')

        review = [
            # row['ReviewedProduct ID'],
            reviewed_product_name_clean,
            row['Reviewer Name'][:2] + '*' * (len(row['Reviewer Name']) - 2),
            row['Review Rating'],
            row['Review Title'],
            row['Review Details'],
            review_date,
            row['Review Helpful'],
            # popularity_score
        ]

        all_reviews.append(review)

    df = pd.DataFrame(all_reviews, columns = ['Product Name', 'Reviewer Name', 'Review Rating', 'Review Title',
                                            'Review Detail', 'Date', 'Review Helpful', 'Popularity Score'])

    df.to_csv("data/croma/croma_reviews_cleaned.csv")

    df2dict = {}
    for index, row in df.iterrows():
        prodName = str(row['Product Name'])
        df2dict.setdefault(prodName, []).append({'Reviewer_Name' : row['Reviewer Name'], 'Rating' : row['Review Rating'],
                                                'Description': row['Review Detail'], 'Date': row['Date']})

    with open('data/croma/croma_reviews_cleaned.json','w') as f:
        json.dump(df2dict, f, indent=4)

    print("Croma Reviews scraping & cleaning completed")
