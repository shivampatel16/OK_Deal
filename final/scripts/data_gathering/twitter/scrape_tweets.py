# File name:
	# scrape_tweets.py
# Description:
	# uses twint to extract tweets related to phones
# Scraping tool used:
	# Twint
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# pandas
    # twint
    # os
    # pathlib > Path
# Dependency files
    # data/croma/croma_products_cleaned.csv
    # data/flipkart/flipkart_products_cleaned.xlsx
    # data/amazon/amazon_products_cleaned.csv
# Online resources
    # https://www.phonearena.com/phones/page/ (for phonearena products specifications)


# imports
import pandas as pd
import twint
import nest_asyncio
import os
from pathlib import Path
import glob


# method to scrape tweets related to phone items
def scrape_tweets():
    nest_asyncio.apply()

    df1 = pd.read_csv("data/croma/croma_products_cleaned.csv")
    df1 = df1.drop(['Unnamed: 0'], axis=1)

    df2 = pd.read_excel("data/flipkart/flipkart_products_cleaned.xlsx")
    df2 = df2.drop(['Unnamed: 0'], axis=1)

    df3 = pd.read_csv("data/amazon/amazon_products_cleaned.csv")
    df3 = df3.drop(['Unnamed: 0'], axis=1)

    phone_names = set()
    phone_names_croma = set()
    phone_names_flipkart = set()
    phone_names_amazon = set()

    # get product names from croma
    for idx, row in df1.iterrows():
        text = row['Product Name']
        sep = '('
        try:
            stripped = text.split(sep, 1)[0].strip().lower()
            phone_names.add(stripped)
            phone_names_croma.add(stripped)
        except:
            continue

    # get product names from flipkart
    for idx, row in df2.iterrows():
        text = row['Product Name']
        sep = '('
        try:
            stripped = text.split(sep, 1)[0].strip().lower()
            phone_names.add(stripped)
            phone_names_flipkart.add(stripped)
        except:
            continue

    # get product names from amazon
    for idx, row in df3.iterrows():
        text = row['Product Name']
        sep = '('
        try:
            stripped = text.split(sep, 1)[0].strip().lower()
            phone_names.add(stripped)
            phone_names_amazon.add(stripped)
        except:
            continue

    phones = phone_names_croma.intersection(phone_names_flipkart)
    phones = phones.intersection(phone_names_amazon)

    try:
        os.makedirs("data/merged/tweets")
        os.chdir("data/merged/tweets")
    except:
        print("data/merged/tweets already exists")
        
    print("Scraping tweets...")
    for phone in phones:
        folder_name = "tweets_" + phone.replace(" ", "_")
        try:
            c = twint.Config()
            c.Lang = "en"
            c.Search = phone
            c.Hide_output = True
            # c.Since = "2010-1-1"
            c.Since = "2021-11-08"
            c.Until = "2021-11-09"
            c.Pandas_clean = True
            c.Verified = True
            c.Store_csv = True
            c.Output = folder_name
            twint.run.Search(c)

        except:
            continue
            
    print("Scraping tweets completed...")

    # get tweets from different folders
    paths = []
    for path, subdirs, files in os.walk("."):
        for name in files:
            if 'tweets.csv' in name and '_tweets.csv' not in name and 'merged' not in name:
                paths.append(os.path.join(path, name))
    print(paths)  
    for p in paths:
        po = Path(p)
        old_name = str(po)
        print("Old: ",old_name)
        new_name = str(po.parent).split("/",2)
        print("New: ",new_name)
        new_name = "/data/tweets/"+"/".join(new_name) + ".csv"
        print("New: ",new_name)
        os.rename(old_name, new_name)
        os.rmdir(new_name[:-4])
        
    all_files = glob.glob("*.csv")
    li = []
    usr = 0

    for filename in all_files:
        phone_name = filename.split("_")[1:]
        phone_name = " ".join(phone_name) 
        df = pd.read_csv(filename, index_col=None, header=0)
        
        df['phone name']=phone_name
        li.append(df)
        
    df_merged = pd.concat(li)
    df_merged = df_merged.reset_index(drop=True)
    df_merged.to_csv("data/merged/tweets/tweets_merged_not_cleaned.csv")

    print("Tweets merged file created...")
