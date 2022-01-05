# File name:
	# clean_amazon_reviews.py
# Description:
	# this script picks the scraped amazon reviews csv file and cleans (formats the text) into an appropriate format for the applications' use
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/data_gathering/amazon/scrape_amazon_reviews.py
# Other modules the file import:
	# pandas
    # json
# Dependency files (input and output files)
    # data/amazon/amazon_reviews_raw.csv
    # data/amazon/amazon_reviews_cleaned.csv
    # data/amazon/amazon_reviews_cleaned.json

    

import pandas as pd
import json


# function to clean amazon reviews (load raw reviews file and cleanup into expected format)
def clean_amazon_reviews():
    amazon_reviews = pd.read_excel("data/amazon/amazon_reviews_raw.xlsx")
    amazon_reviews_new = amazon_reviews.rename(
        columns={'Review Rating': 'Review Rating (5)', 'Review Details': 'Review Detail', 'Review Date': 'Date',
                 'ReviewedProduct Name': 'Product Name'})
    del amazon_reviews_new['ReviewedProductID'], amazon_reviews_new['Review URL'], amazon_reviews_new['Unnamed: 0']
    amazon_reviews_new['Product Name'] = [v.split('(')[0].strip().lower().replace("\"", "") if v.find('(') >= 0 else v
                                          for v in amazon_reviews_new['Product Name']]
    review_date = []
    popularity_score = []
    review_ratings = []
    review_helpful = []
    prod = []
    dict_months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                   'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    for element in amazon_reviews_new['Review Rating (5)'].iteritems():
        if type(element[1]) == str:
            review_ratings.append(element[1].strip().split(' ')[0])
        else:
            review_ratings.append('NaN')
    for element in amazon_reviews_new['Product Name'].iteritems():
        if type(element[1]) == str:
            prod.append(element[1].replace('"', '').strip().lower())
        else:
            prod.append('NaN')

    for element in amazon_reviews_new['Review Helpful'].iteritems():
        if type(element[1]) == str:
            review_helpful.append(element[1].strip().split(" ")[0].replace(',', '').replace('One', '1'))
        else:
            review_helpful.append('NaN')
    amazon_reviews_new['Review Rating (5)'] = review_ratings
    amazon_reviews_new['Review Helpful'] = review_helpful
    for index, row in amazon_reviews_new.iterrows():
        if 'on' in row['Date'] and type(row['Date']) == str:
            date_str = row['Date'].split('on')[1].strip()
            date_elements = date_str.split(' ')
            str1 = ''
            str1 += date_elements[2] + '-' + dict_months[date_elements[1]] + '-' + date_elements[0]
            review_date.append(str1)
            if row['Review Helpful']:
                popularity_score.append(str(float(row['Review Rating (5)']) * float(row['Review Helpful'])))
            else:
                popularity_score.append('NaN')

    names = []
    for element in amazon_reviews_new['Reviewer Name'].iteritems():
        if type(element[1]) == str:
            names.append(element[1][:2] + '*' * (len(element[1]) - 2))
        else:
            names.append('NaN')

    amazon_reviews_new['Reviewer Name'] = names
    amazon_reviews_new['Date'] = review_date
    amazon_reviews_new['Popularity Score'] = popularity_score
    amazon_reviews_new['Product Name'] = prod
    amazon_reviews_new.to_csv('data/amazon/amazon_reviews_cleaned.csv')

    ## to csv
    amazon_products_reviews = pd.read_csv('data/amazon/amazon_reviews_cleaned.csv')

    df2dict = {}
    for index, row in amazon_products_reviews.iterrows():
        prodName = str(row['Product Name'])
        df2dict.setdefault(prodName, []).append(
            {'Reviewer_Name': row['Reviewer Name'], 'Rating': row['Review Rating (5)'],
             'Description': row['Review Detail'], 'Date': row['Date']})

    with open('data/amazon/amazon_reviews_cleaned.json', 'w+') as f:
        json.dump(df2dict, f, indent=4)
