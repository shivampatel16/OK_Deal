#!/usr/bin/env python3

# File name:
	# clean_amazon_products.py
# Description:
	# this script picks the scraped amazon products csv file and cleans (formats the text) into an appropriate format for the applications' use
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/data_gathering/amazon/scrape_amazon_products.py
# Other modules the file import:
	# pandas
# Dependency files
    # data/amazon/amazon_products_raw.csv
    # data/amazon/amazon_products_cleaned.csv

import pandas as pd


def step3_product_cleaning():
    amazon_products = pd.read_csv("data/amazon/amazon_products_raw.csv")
    amazon_products_new = amazon_products.rename(
        columns={'Average Rating(5)': 'Average Rating (5)', 'Name': 'Product Name', 'MRP': 'Base Price (INR)',
                 'Price': 'Discounted Price (INR)', 'No. of Ratings': 'Number of Ratings'}, inplace=False)
    amazon_products_variant_info = [v.split('(')[1].lower().replace("\"", "") if v.find('(') >= 0 else v for v in
                                    amazon_products_new['Product Name']]
    amazon_products_new['Product Name'] = [v.split('(')[0].replace("\"", "").strip().lower() if v.find('(') >= 0 else v
                                           for v in amazon_products_new['Product Name']]
    amazon_products_new.insert(1, 'Variant', amazon_products_variant_info)
    indexes = []
    for element in amazon_products_new['Base Price (INR)'].iteritems():
        if type(element[1]) == float:
            amazon_products_new['Base Price (INR)'][element[0]], amazon_products_new['Discounted Price (INR)'][
                element[0]] = amazon_products_new['Discounted Price (INR)'][element[0]], \
                              amazon_products_new['Base Price (INR)'][element[0]]
            indexes.append(element[0])
    discounts = []
    base = []
    disc = []
    rating = []
    no_rating = []
    url = []

    for item in amazon_products_new['Base Price (INR)'].iteritems():
        if type(item[1]) == float:
            base.append(None)
        else:
            base.append(item[1].replace('₹', '').replace(',', ''))

    for item in amazon_products_new['Discounted Price (INR)'].iteritems():
        if type(item[1]) == float:
            disc.append(None)
        else:
            disc.append(item[1].replace('₹', '').replace(',', ''))

    for item in amazon_products_new['Average Rating (5)'].iteritems():
        if type(item[1]) == float:
            rating.append(None)
        else:
            rating.append(item[1].split()[0])

    for item in amazon_products_new['Number of Ratings'].iteritems():
        if type(item[1]) == float:
            no_rating.append(None)
        else:
            no_rating.append(item[1].replace(',', ''))

    for item in amazon_products_new['URL'].iteritems():
        if type(item[1]) == float:
            url.append(None)
        else:
            url.append('https://amazon.in' + str(item[1]))

    amazon_products_new['Base Price (INR)'] = base
    amazon_products_new['Discounted Price (INR)'] = disc
    amazon_products_new['Average Rating (5)'] = rating
    amazon_products_new['Number of Ratings'] = no_rating
    amazon_products_new['URL'] = url

    for item in amazon_products_new['Base Price (INR)'].iteritems():
        if (isinstance(item[1], type(None))) or (
                isinstance(amazon_products_new['Discounted Price (INR)'][item[0]], type(None))):
            discounts.append(None)
        else:
            disc_price = amazon_products_new['Discounted Price (INR)'][item[0]]
            discounts.append(int(((float(item[1]) - float(disc_price)) / float(item[1])) * 100))

    amazon_products_new.insert(3, 'Discount (%)', discounts)
    amazon_products_new.to_csv('data/amazon/amazon_products_cleaned.csv')
