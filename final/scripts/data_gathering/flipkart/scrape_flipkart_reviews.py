#!/usr/bin/env python3

# File name:
	# scrape_flipkart_reviews.py
# Description:
	# uses selenium to extract flipkart reviews 
# Scraping tool used:
	# Selenium
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# lxml > html
    # os, pandas , time, json
    # selenium.common.exceptions > NoSuchElementException
    # undetected_chromedriver 
    # warnings
# Dependency files
    # data/flipkart/flipkart_reviews_raw.csv
    # data/flipkart/flipkart_reviews_cleaned.csv
    # data/flipkart/flipkart_reviews_cleaned.json
# Online resources
    # https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=clp_metro_expandable_5_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q0QIS4SPJNLH_wp3&fm=neo%2Fmerchandising&iid=M_639b63f0-b343-43c4-9ee5-a99063a235cd_3.Q0QIS4SPJNLH&ppt=browse&ppn=browse&ssid=lkc1ezok9c0000001636010321741&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock (for flipkart reviews)


#imports
from selenium import webdriver
import pandas as pd
import json
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import warnings
warnings.filterwarnings("ignore")

def scrape_flipkart_reviews():

    flipkart_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=clp_metro_expandable_5_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q0QIS4SPJNLH_wp3&fm=neo%2Fmerchandising&iid=M_639b63f0-b343-43c4-9ee5-a99063a235cd_3.Q0QIS4SPJNLH&ppt=browse&ppn=browse&ssid=lkc1ezok9c0000001636010321741&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    browser = uc.Chrome(options=options)
    browser.implicitly_wait(10)  # seconds

    browser.get(flipkart_url)

    print("Searching how many pages of products to get reviews from Flipkart")

    try:
        no_of_pages = int(browser.find_element_by_css_selector("._2MImiq>span").text.split('of')[1].strip())
    except NoSuchElementException:
        no_of_pages = 1

    print('Total product pages to scrape: ', no_of_pages)

    item_urls = []

    for i in range(1, no_of_pages + 1):
        page = browser.get(flipkart_url + "&page=" + str(i))
        # page_content = html.fromstring(page.content)

        items = browser.find_elements_by_css_selector("a._1fQZEK")

        if len(items) == 0:
            break

        for j in items:
            url = j.get_attribute("href")
            item_urls.append(url)

    print("Total products to fetch reviews: ",len(item_urls))

    review_urls = []
    reviewed_product_id = []
    reviewed_product_name = []
    reviewer_name = []
    review_rating = []
    review_title = []
    review_details = []
    review_date = []
    review_helpful = []

    count_page = 1
    for item_url in item_urls:
        page = browser.get(item_url)

        if (count_page % 10 == 0):
            print("Get ", count_page , " product reviews page from Flipkart")
        count_page += 1
        try:
            review_url = browser.find_element_by_css_selector('div[class="col JOpGWq"]>a').get_attribute('href')
            review_urls.append(review_url)
        except NoSuchElementException:
            continue

    # Start review Scraping
    print("Flipkart reviews scraping starts......")
    product_id = 0
    count_page = 1
    for review_url in review_urls:

        if (count_page % 10 == 0):
            print("Scraped ", count_page , " product reviews from Flipkart")
        
        count_page += 1
        page = browser.get(review_url)

        reviews = browser.find_elements_by_css_selector('div[class="col _2wzgFH K0kLPL"]')

        try:
            prod_name = browser.find_element_by_css_selector('a[class="s1Q9rs _2qfgz2"]').get_attribute('title')
        except NoSuchElementException:
            prod_name = None

        product_id += 1
        for review in reviews:
            try:
                review_title.append(review.find_element_by_css_selector('p._2-N8zT').text.strip())
                # print("Title: ",title)
            except NoSuchElementException:
                review_title.append(None)

            try:
                reviewer_name.append(review.find_element_by_css_selector('p[class="_2sc7ZR _2V5EHH"]').text.strip())
            except NoSuchElementException:
                reviewer_name.append(None)

            try:
                review_rating.append(review.find_element_by_css_selector('div._3LWZlK._1BLPMq').text.strip())
            except NoSuchElementException:
                review_rating.append(None)

            try:
                review_details.append(
                    review.find_element_by_css_selector('.t-ZTKy>div>div').text.strip().replace('\n', '  '))
            except NoSuchElementException:
                review_details.append(None)

            try:
                review_helpful.append(review.find_element_by_css_selector('div[class="_1LmwT9"]>span._3c3Px5').text.strip())
            except NoSuchElementException:
                review_helpful.append(None)

            try:
                review_date.append(review.find_element_by_css_selector('p[class="_2sc7ZR"]').text.strip())
            except:
                review_date.append(None)

            reviewed_product_id.append(product_id)
            reviewed_product_name.append(prod_name)


    browser.quit()

    print("All ", len(review_urls) , " products' reviews from Flipkart scraped successfully!")

    columns_reviews = ['ReviewedProduct ID', 'ReviewedProduct Name', 'Reviewer Name', 'Review Rating', 'Review Title',
                    'Review Details', 'Review Date', 'Review Helpful']

    flipkart_products_review_df = pd.DataFrame({
        'ReviewedProduct ID': reviewed_product_id,
        'ReviewedProduct Name': reviewed_product_name,
        'Reviewer Name': reviewer_name,
        'Review Rating': review_rating,
        'Review Title': review_title,
        'Review Details': review_details,
        'Review Date': review_date,
        'Review Helpful': review_helpful
    })[columns_reviews]

    flipkart_products_review_df.set_index('ReviewedProduct ID', inplace=True)
    flipkart_products_review_df.to_csv('data/flipkart/flipkart_reviews_raw.csv',encoding='utf8')

    print("Flipkart reviews cleaning starts......")

    all_reviews = []

    for index, row in flipkart_products_review_df.iterrows():
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
    
    df.to_csv("data/flipkart/flipkart_reviews_cleaned.csv")

    df2dict = {}
    for index, row in df.iterrows():
        prodName = str(row['Product Name'])
        df2dict.setdefault(prodName, []).append({'Reviewer_Name' : row['Reviewer Name'], 'Rating' : row['Review Rating'],
                                                'Description': row['Review Detail'], 'Date': row['Date']})

    with open('data/flipkart/flipkart_reviews_cleaned.json','w') as f:
        json.dump(df2dict, f, indent=4)

    print("Flipkart Reviews scraping & cleaning completed")
