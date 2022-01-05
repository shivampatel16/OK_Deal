#!/usr/bin/env python3

# File name:
	# scrape_flipkart_products.py
# Description:
	# uses lxml to extract flipkart products 
# Scraping tool used:
	# Lxml
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# lxml > html
    # os, pandas , time
    # warnings
    # requests
# Dependency files
    # data/flipkart/flipkart_products_cleaned.xlsx
    # data/flipkart/flipkart_products_raw.csv
# Online resources
    # https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=clp_metro_expandable_5_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q0QIS4SPJNLH_wp3&fm=neo%2Fmerchandising&iid=M_639b63f0-b343-43c4-9ee5-a99063a235cd_3.Q0QIS4SPJNLH&ppt=browse&ppn=browse&ssid=lkc1ezok9c0000001636010321741&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock (for flipkart products)


# imports
import requests
from lxml import html
import pandas as pd
import time
import warnings


def scrape_flipkart_products():
    flipkart_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=clp_metro_expandable_5_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q0QIS4SPJNLH_wp3&fm=neo%2Fmerchandising&iid=M_639b63f0-b343-43c4-9ee5-a99063a235cd_3.Q0QIS4SPJNLH&ppt=browse&ppn=browse&ssid=lkc1ezok9c0000001636010321741&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock"

    #fetching the flipkart url html content
    print("Started scraping Flipkart product data")
    page = requests.get(flipkart_url)
    time.sleep(3)
    html_content = html.fromstring(page.content)

    #fetching page count
    try:
        no_of_pages = int(html_content.cssselect("._2MImiq>span")[0].text.split('of')[1].strip())
    except:
        no_of_pages = 1

    flipkart_product_urls = []


    #fetching product urls
    for i in range(1, no_of_pages + 1):
        page = requests.get(flipkart_url + "&page="+str(i))
        time.sleep(3)
        page_content = html.fromstring(page.content)
        items = page_content.cssselect("a._1fQZEK")
        if len(items) == 0:
            break
        
        for j in items:
            url = j.attrib["href"]
            if(not(url.startswith("/"))):
                url = "/" + url
            flipkart_product_urls.append("https://www.flipkart.com"+url)
        


    print("Total ",len(flipkart_product_urls), " Flipkart products to scrape")

    flipkart_product_names = []
    flipkart_product_mrps = []
    flipkart_product_prices = []
    flipkart_avg_ratings = []
    flipkart_total_no_of_ratings = []
    count = 0

    #fetching product data from each product url
    for item_url in flipkart_product_urls:
        count += 1
        product = requests.get(item_url)
        time.sleep(3)
        product_content = html.fromstring(product.content)
        
        try:
            flipkart_product_names.append(product_content.cssselect(".B_NuCI")[0].text_content().strip())
        except:
            flipkart_product_names.append(None)
        

        try:
            flipkart_product_mrps.append(product_content.cssselect("._3I9_wc._2p6lqe")[0].text_content().strip())
        except:
            flipkart_product_mrps.append(None)

        try:
            flipkart_product_prices.append(product_content.cssselect("._30jeq3._16Jk6d")[0].text_content().strip())
        except:
            flipkart_product_prices.append(None)
        

        try:
            flipkart_avg_ratings.append(product_content.cssselect("._2d4LTz")[0].text_content().strip())
        except:
            flipkart_avg_ratings.append(None)
        
        try:
            flipkart_total_no_of_ratings.append(product_content.cssselect("._16VRIQ ._2_R_DZ")[0].text_content().strip().split("Ratings")[0])
        except:
            flipkart_total_no_of_ratings.append(None)
        
        if(count % 10 == 0):
            print("Scraped ",count," products from Flipkart...")
        
    print("All ",len(flipkart_product_urls)," products scraped successfully!")

    columns = ['Name','MRP','Price','Average Rating(5)','No. of Ratings', 'URL']

    #storing in dataframe
    flipkart_products = pd.DataFrame({
                                        'Name': flipkart_product_names,
                                        'MRP' : flipkart_product_mrps,
                                        'Price': flipkart_product_prices,
                                        'Average Rating(5)': flipkart_avg_ratings,
                                        'No. of Ratings': flipkart_total_no_of_ratings,
                                        'URL': flipkart_product_urls})[columns]

    #drop duplicates
    flipkart_products.drop_duplicates()

    #saving raw data to csv
    flipkart_products.to_csv('data/flipkart/flipkart_products_raw.csv',encoding="utf-8-sig")


    print("Started cleaning scraped data from Flipkart")

    #data cleaning
    flipkart_products_cleaned = flipkart_products.rename(columns = {'Average Rating(5)':'Average Rating (5)','Name': 'Product Name', 'MRP': 'Base Price (INR)', 'Price': 'Discounted Price (INR)', 'No. of Ratings': 'Number of Ratings'}, inplace = False)
    if 'Unnamed: 0' in flipkart_products_cleaned:
        del flipkart_products_cleaned['Unnamed: 0']
    product_names = []
    variants = []
    #separating product variant from product name
    for v in flipkart_products_cleaned['Product Name'].iteritems():
        if type(v[1]) == float or v[1] is None:
            product_names.append(None)
            variants.append(None)
        else:
            product_names.append(v[1].split('(',1)[0])
            variants.append(v[1].split('(',1)[1].replace('(','').replace(')',''))

    flipkart_products_cleaned['Product Name'] = product_names
    flipkart_products_cleaned.insert(1,'Variant', variants)

    indexes = []
    for element in flipkart_products_cleaned['Base Price (INR)'].iteritems():
            if type(element[1]) == float or element[1] is None:
                flipkart_products_cleaned['Base Price (INR)'][element[0]],flipkart_products_cleaned['Discounted Price (INR)'][element[0]] = flipkart_products_cleaned['Discounted Price (INR)'][element[0]],flipkart_products_cleaned['Base Price (INR)'][element[0]]
                indexes.append(element[0])
        
    flipkart_discount_percentages = []
    flipkart_base_prices = []
    flipkart_discounted_prices = []
    for item in flipkart_products_cleaned['Base Price (INR)'].iteritems():
        if type(item[1]) == float or item[1] is None:
            flipkart_base_prices.append(None)
        else:
            flipkart_base_prices.append(item[1].replace('₹','').replace(',',''))

    for item in flipkart_products_cleaned['Discounted Price (INR)'].iteritems():
        if type(item[1]) == float or item[1] is None:
            flipkart_discounted_prices.append(None)
        else:
            flipkart_discounted_prices.append(item[1].replace('₹','').replace(',',''))

    flipkart_products_cleaned['Base Price (INR)'] = flipkart_base_prices
    flipkart_products_cleaned['Discounted Price (INR)'] = flipkart_discounted_prices


    for item in flipkart_products_cleaned['Base Price (INR)'].iteritems():
        if (isinstance(item[1], type(None))) or (isinstance(flipkart_products_cleaned['Discounted Price (INR)'][item[0]], type(None))):
            flipkart_discount_percentages.append(None)
        else:
            disc_price = flipkart_products_cleaned['Discounted Price (INR)'][item[0]]
            if item[1].strip() == '' or disc_price.strip() == '':
                flipkart_discount_percentages.append(None)
            else:
                flipkart_discount_percentages.append(int(((float(item[1]) - float(disc_price))/float(item[1])) * 100))

    #saving cleaned data to xlsx
    flipkart_products_cleaned.insert(3,'Discount (%)',flipkart_discount_percentages)
    flipkart_products_cleaned.to_excel('data/flipkart/flipkart_products_cleaned.xlsx')

    print("Cleaning completed for the scrapped data from Flipkart")

#run method in file if file is run directly
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    scrape_flipkart_products()