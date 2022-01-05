# file name:
	# merge_files.py
# description:
	# merges raw and cleaned product details and reviews details into merged files
# names of group members:  
       # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# files that import this module:
	# scripts/scraper.py
# other modules the file import:
	# pandas
       # os
# dependency files
       # data/flipkart/flipkart_products_cleaned.xlsx
       # data/flipkart/flipkart_reviews_cleaned.csv
       # data/croma/croma_reviews_cleaned.csv
       # data/croma/croma_products_cleaned.csv
       # data/amazon/amazon_reviews_cleaned.csv
       # data/amazon/amazon_products_cleaned.csv
# online resources
       # none

#import
import pandas as pd
import os

#read all clean and raw data files for products and reveiws
flipkart_products_cleaned = pd.read_excel("data/flipkart/flipkart_products_cleaned.xlsx")
flipkart_reviews_cleaned = pd.read_csv("data/flipkart/flipkart_reviews_cleaned.csv")

croma_products_cleaned = pd.read_csv("data/croma/croma_products_cleaned.csv")
croma_reviews_cleaned = pd.read_csv("data/croma/croma_reviews_cleaned.csv")

amazon_products_cleaned = pd.read_csv("data/amazon/amazon_products_cleaned.csv")
amazon_reviews_cleaned = pd.read_csv("data/amazon/amazon_reviews_cleaned.csv")

croma_reviews_cleaned['Product Name'] = [v.rsplit('(',1)[0] for v in croma_reviews_cleaned['Product Name']]
flipkart_reviews_cleaned['Product Name'] = [v.rsplit('(',1)[0] for v in flipkart_reviews_cleaned['Product Name']]

flipkart_products_cleaned = flipkart_products_cleaned[['Product Name', 'Variant', 'Base Price (INR)',
       'Discount (%)', 'Discounted Price (INR)', 'Average Rating (5)',
       'Number of Ratings', 'URL']]

flipkart_reviews_cleaned = flipkart_reviews_cleaned[['Product Name', 'Reviewer Name', 'Review Rating',
       'Review Title', 'Review Detail', 'Date', 'Review Helpful',
       'Popularity Score']]

croma_products_cleaned = croma_products_cleaned[['Product Name', 'Variant', 'Base Price (INR)',
       'Discount (%)', 'Discounted Price (INR)', 'Average Rating (5)',
       'Number of Ratings', 'URL']]

croma_reviews_cleaned = croma_reviews_cleaned[['Product Name', 'Reviewer Name', 'Review Rating',
       'Review Title', 'Review Detail', 'Date', 'Review Helpful',
       'Popularity Score']]

amazon_products_cleaned = amazon_products_cleaned[['Product Name', 'Variant', 'Base Price (INR)',
       'Discount (%)', 'Discounted Price (INR)', 'Average Rating (5)',
       'Number of Ratings', 'URL']]

amazon_reviews_cleaned = amazon_reviews_cleaned[['Product Name', 'Reviewer Name', 'Review Rating (5)',
       'Review Title', 'Review Detail', 'Date', 'Review Helpful',
       'Popularity Score']]

def transform_product_name(df):
    df['Product Name'] = df['Product Name'].str.lower().str.strip()
    return df

def merge_dataframes(df1,df2,s1, s2, join_type):
    merged_df = pd.merge(
                df1,
                df2,
                on=['Product Name', 'Product Name'],
                how=join_type,
                suffixes=(s1,s2)
            )
    return merged_df

# main method to merge files
def main():
    transform_product_name(flipkart_products_cleaned)
    transform_product_name(flipkart_reviews_cleaned)
    transform_product_name(croma_products_cleaned)
    transform_product_name(croma_reviews_cleaned)
    transform_product_name(amazon_products_cleaned)
    transform_product_name(amazon_reviews_cleaned)

    print("Merging....")
    merged_products_raw = merge_dataframes(amazon_products_cleaned, croma_products_cleaned,'_amazon','_croma', 'outer')
    merged_products_raw = merge_dataframes(merged_products_raw, flipkart_products_cleaned,'','_flipkart', 'outer')

    merged_products_cleaned = merge_dataframes(amazon_products_cleaned, croma_products_cleaned,'_amazon','_croma', 'inner')
    merged_products_cleaned = merge_dataframes(merged_products_cleaned, flipkart_products_cleaned,'','_flipkart', 'inner')

    merged_reviews_raw = merge_dataframes(amazon_reviews_cleaned, croma_reviews_cleaned,'_amazon','_croma', 'outer')
    merged_reviews_raw = merge_dataframes(merged_reviews_raw, flipkart_reviews_cleaned,'','_flipkart', 'outer')

    merged_reviews_cleaned = merge_dataframes(amazon_reviews_cleaned, croma_reviews_cleaned,'_amazon','_croma', 'inner')
    merged_reviews_cleaned = merge_dataframes(merged_reviews_cleaned, flipkart_reviews_cleaned,'','_flipkart', 'inner')


    merged_products_raw.rename({"Variant":"Variant_flipkart",
                                "Base Price (INR)":"Base Price (INR)_flipkart",
                                "Discount (%)":"Discount (%)_flipkart",
                                "Discounted Price (INR)":"Discounted Price (INR)_flipkart",
                                "Average Rating (5)":"Average Rating (5)_flipkart",
                                "Number of Ratings": "Number of Ratings_flipkart",
                                "URL":"URL_flipkart"
                               }, axis=1, inplace=True)

    merged_products_cleaned.rename({"Variant":"Variant_flipkart",
                                "Base Price (INR)":"Base Price (INR)_flipkart",
                                "Discount (%)":"Discount (%)_flipkart",
                                "Discounted Price (INR)":"Discounted Price (INR)_flipkart",
                                "Average Rating (5)":"Average Rating (5)_flipkart",
                                "Number of Ratings": "Number of Ratings_flipkart",
                                "URL":"URL_flipkart"
                               }, axis=1, inplace=True)

    merged_reviews_raw.rename({"Reviewer Name" :"Reviewer Name_flipkart" ,
                                "Review Rating" : "Review Rating_flipkart",
                                "Review Title" : "Review Title_flipkart",
                                "Review Detail": "Review Detail_flipkart",
                                "Date": "Date_flipkart",
                                "Review Helpful": "Review Helpful_flipkart",
                                "Popularity Score": "Popularity Score_flipkart"
                               }, axis=1, inplace=True)

    merged_reviews_cleaned.rename({"Reviewer Name" :"Reviewer Name_flipkart" ,
                                "Review Rating" : "Review Rating_flipkart",
                                "Review Title" : "Review Title_flipkart",
                                "Review Detail": "Review Detail_flipkart",
                                "Date": "Date_flipkart",
                                "Review Helpful": "Review Helpful_flipkart",
                                "Popularity Score": "Popularity Score_flipkart"
                               }, axis=1, inplace=True)
    
    print("Please wait. We are getting the data ready for you...\n")

    try:
       os.mkdir("data/merged/products")
    except:
       print("data/merged/products already exists ... \nContinuing \n")
    
    try:
           os.mkdir("data/merged/reviews")
    except:
       print("data/merged/reviews already exists ... \nContinuing \n")

    try:
       os.mkdir("data/merged/tweets")
    except:
       print("data/merged/tweets already exists ... \nContinuing \n")

    merged_products_raw.to_csv("data/merged/products/Merged_Products_Data_Raw.csv")
    merged_products_cleaned.to_csv("data/merged/products/Merged_Products_Data_Cleaned.csv")
    merged_reviews_raw.to_csv("data/merged/reviews/Merged_Products_Reviews_Raw.csv")
    merged_reviews_cleaned.to_csv("data/merged/reviews/Merged_Products_Reviews_Cleaned.csv")
    print("Merging done !!!")
    
    #print the shape of all the cleaned files
    print('\n')
    print("Amazon Products: " ,amazon_products_cleaned.shape) 
    print("Croma Products: " ,croma_products_cleaned.shape)
    print("Flipkart Products: " ,flipkart_products_cleaned.shape)
    print("Merged Products: " ,merged_products_cleaned.shape) 
    print("Amazon Reviews: " ,amazon_reviews_cleaned.shape)
    print("Croma Reviews: " ,croma_reviews_cleaned.shape)
    print("Flipkart Reviews: " ,flipkart_reviews_cleaned.shape)
    print("Merged Reviews: " ,merged_reviews_cleaned.shape)
    print('\n')