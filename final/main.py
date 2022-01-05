# file name:
	# main.py
# description:
	# provides GUI and user driven menu for customer to interact with application
# names of group members:  
    # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# files that import this module:
	# none
# other modules the file import:
	# pandas, re, warnings, 
    # nltk , nltk.corpus, nltk.tokenize
    # import engines.Product_Engine 
    # engines.Review_
    # engines.Specs_Engine
    # scripts.Products_Analysis 
    # scripts.Tweet_Sentiment_Analysis 
    # scripts.scraper
    # scripts.review_analysis 
# dependency files
    # data/currency_api/currency_conversion_api_data_cleaned.csv
# online resources
    # none

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import scripts.merge_files as mf
import re
import warnings
warnings.filterwarnings('ignore')
import os

# import module
import traceback

mf.main()

import engines.Product_Engine as Product
import engines.Review_Engine as Review
import engines.Specs_Engine as ProductSpecs
import scripts.Products_Analysis as pa
import scripts.Tweet_Sentiment_Analysis as twa
import scripts.scraper as scr
import scripts.review_analysis as ra


try:
    os.makedirs("results")
except:
    print("results folder already exists")
    

# printing the starting line
print("\nWELCOME TO OK DEAL!")

conversion_value = 0
rupee_value = 85.23
file = None

def getCurrencyConversion(input_currency):
    currency_df = pd.read_csv('data/currency_api/currency_conversion_api_data_cleaned.csv')

    # Set rupee conversion rate
    rows = currency_df.loc[currency_df['currency'] == "INR"]
    rupee_value = rows.iloc[0]['value']
    print("Rupee value", rupee_value)

    # Set conversion rate of currency selected
    rows = currency_df.loc[currency_df['currency'] == input_currency]
    conversion_value = rows.iloc[0]['value']
    print("Conversion value", conversion_value)

# getCurrencyConversion("USD")

def chooseCurrency():

    while True:
        print("\nChoose preferred currency")
        print("1. Indian Rupee INR")
        print("2. United States Dollar USD")
        print("3. Australian Dollar AUD")
        print("4. EURO EUR")
        print("0. Go back\n")

        user_input = input("Enter the Choice: ")

        try:
            choice = int(user_input)

            if choice == 1:
                getCurrencyConversion("INR")
                break

            elif choice == 2:
                getCurrencyConversion("USD")
                break

            elif choice == 3:
                getCurrencyConversion("AUD")
                break

            elif choice == 4:
                getCurrencyConversion("EUR")
                break

            elif choice == 0:
                return "Back"

            else:
                print("\nPlease enter a valid input\n")

        except Exception as e:
            print(e)
            print("That is an invalid choice, please try again")
            traceback.print_exc()
    return "Done"

def searchByProductName():

    backOption = chooseCurrency()
    if backOption == "Back":
        return

    user_input_product_name = input("Enter a product name: ")

    file = getProductNameDetails(user_input_product_name.lower())

    return file
  

def searchByBrandName():
    user_input_brand_name = input("Enter a brand name ")
    print(user_input_brand_name)

def getProductNameDetails(product_name,flag = True):
    product_not_found_flag = 1
    product = Product.Product(product_name)
    result_amazon = product.get_amazon()
    result_flipkart = product.get_flipkart()
    result_croma = product.get_croma()

    file = open("results/"+product_name+".txt","w")
    file.write(product_name + "\n" + "-" * 100 + "\n")
        
    if result_amazon is not None:
        product_not_found_flag = 0
        file.write("\nPLATFORM OVERVIEW")
        file.write("\n\n\t\t--------Amazon Products--------\n\n")
        for variant, spec in result_amazon.items():
            file.write("\t\t\t\tVariant name : " + variant + "\n")
            file.write("\t\t\t\t\t\tPrice : " + str((spec['price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tDiscount (%) : " + str(spec['discount']) + "% \n")
            file.write("\t\t\t\t\t\tDiscount price : " + str((spec['discounted_price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tAvg rating : " + str(spec['average_rating']) + "\n")
            file.write("\t\t\t\t\t\tProduct URL : " + str(spec['URL']) + "\n\n")

    else:
        file.write("\t\t\t\t" + "Product not found on Amazon" + "\n")

    if result_flipkart is not None:
        product_not_found_flag = 0
        file.write("\n\t\t--------Flipkart Products--------\n\n")
        for variant, spec in result_flipkart.items():
            file.write("\t\t\t\tVariant name : " + variant + "\n")
            file.write("\t\t\t\t\t\tPrice : " + str((spec['price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tDiscount (%) : " + str(spec['discount']) + "% \n")
            file.write("\t\t\t\t\t\tDiscount price : " + str((spec['discounted_price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tAvg rating : " + str(spec['average_rating']) + "\n")
            file.write("\t\t\t\t\t\tProduct URL : " + str(spec['URL']) + "\n\n")
    else:
        file.write("\t\t\t\t" + "Product not found on Flipkart" + "\n")

    if result_croma is not None:
        product_not_found_flag = 0
        file.write("\n\t\t--------Croma Products--------\n\n")
        for variant, spec in result_croma.items():
            file.write("\t\t\t\tVariant name : " + variant + "\n")
            file.write("\t\t\t\t\t\tPrice : " + str((spec['price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tDiscount (%) : " + str(spec['discount']) + "% \n")
            file.write("\t\t\t\t\t\tDiscount price : " + str((spec['discounted_price']/rupee_value) * conversion_value) + "\n")
            file.write("\t\t\t\t\t\tAvg rating : " + str(spec['average_rating']) + "\n")
            file.write("\t\t\t\t\t\tProduct URL : " + str(spec['URL']) + "\n\n")
    else:
        file.write("\t\t\t\t" + "Product not found on Croma" + "\n")
    
    if(product_not_found_flag == 1):
        file.close()
        print("\n\nProduct not found... Showing you some suggestions")
        os.remove("results/"+product_name+".txt")
        getCosineSimilaritySuggestions(product_name)
    else:
        if flag:
            getReviewDetails(product_name, file)
            getPhoneArenaSpecs(product_name, file)
            print("\n\nProduct found! You can view the product data in results/"+product_name+".txt")
        else:
            print("\n\nYou can view the product data in results/"+product_name+".txt")
    
    return file
        


def getReviewDetails(product_name, file = None):
    review = Review.Review(product_name)

    file.write("\n\nREVIEWS & RATINGS ACROSS PLATFORMS\n")
    file.write("\n\t\t--------Amazon Reviews--------\n\n")

    result = review.get_amazon()
    if result is not None:
        for r in result:
            file.write("\t\t\t\tReviewer name : " + str(r['Reviewer_Name'])  + "\n")
            file.write("\t\t\t\t\t\tRating : " + str(r['Rating'])  + "\n")
            file.write("\t\t\t\t\t\tDescription : " + str(deEmojify(r['Description']))  + "\n\n")
    else:
        file.write("\t\t\t\t" + "Sorry, we could not find any reviews on Amazon" + "\n")

    file.write("\n\n\t\t--------Flipkart Reviews--------\n\n")

    result = review.get_flipkart()
    if result is not None:
        for r in result:
            file.write("\t\t\t\tReviewer name : " + str(r['Reviewer_Name'])  + "\n")
            file.write("\t\t\t\t\t\tRating : " + str(r['Rating'])  + "\n")
            file.write("\t\t\t\t\t\tDescription : " + str(deEmojify(r['Description']))  + "\n\n")
    else:
        file.write("\t\t\t\t" + "Sorry, we could not find any reviews on Flipkart" + "\n")

    file.write("\n\n\t\t--------Croma Reviews--------\n\n")

    result = review.get_croma()
    if result is not None:
        for r in result:
            file.write("\t\t\t\tReviewer name : " + str(r['Reviewer_Name'])  + "\n")
            file.write("\t\t\t\t\t\tRating : " + str(r['Rating'])  + "\n")
            file.write("\t\t\t\t\t\tDescription : " + str(deEmojify(r['Description']))  + "\n\n")
    else:
        file.write("\t\t\t\t" + "Sorry, we could not find any reviews on Croma" + "\n")

def getPhoneArenaSpecs(product_name,file = None):
    file.write("\n\nPHONE ARENA SPECS\n\n")
    phone_arena = ProductSpecs.ProductSpecs(product_name)
    result = phone_arena.get_specs()
    if result is not None:
        for key,value in result.items():
            value = str(value).replace('\n', ' ; ').replace('\r', '').replace('\t','')
            file.write("\t\t\t\t"+key+" : "+value + "\n")
    else:
        file.write("\t\t\t\t" + "Sorry, we could not find any phone specifications on Phone Arena" + "\n")

def productAnalysisVisualization():

    while True:
        print("Product Analysis Visualization")
        print("1. Base price distribution")
        print("2. Discount % distribution")
        print("3. Discount price distribution")
        print("4. Average rating distribution")
        print("5. Show all distribution plots")
        print("6. Base price triple plot")
        print("7. Discount percent triple plot")
        print("8. Discount price triple plot")
        print("9. Average rating triple plot")
        print("10. Descriptive statistics for Amazon, Croma and Flipkart")
        print("0. Go back\n")

        user_input = input("Enter the Choice: ")

        try:
            choice = int(user_input)

            if choice == 1:
                pa.basePriceDistribution()

            elif choice == 2:
                pa.discountPercentDistribution()

            elif choice == 3:
                pa.discountPriceDistribution()

            elif choice == 4:
                pa.averageRatingDistribution()

            elif choice == 5:
                pa.showAllDistributionPlots()

            elif choice == 6:
                pa.basePriceTriplePlot()

            elif choice == 7:
                pa.discountPercentTriplePlot()

            elif choice == 8:
                pa.discountedPriceTriplePlot()

            elif choice == 9:
                pa.averageRatingTriplePlot()

            elif choice == 10:
                pa.stats()

            elif choice == 0:
                break

            else:
                print("\nPlease enter a valid input\n")

        except Exception as e:
            print(e)
            print("That is an invalid choice, please try again")
            traceback.print_exc()


def twitterAnalysisVisualization():
    while True:
        print("Twitter Analysis Visualization")
        print("1. Positive tweet charts")
        print("2. Neutral tweet charts")
        print("3. Negative tweet charts")
        print("0. Go back\n")

        user_input = input("Enter the Choice: ")

        try:
            choice = int(user_input)

            if choice == 1:
                twa.positiveTweets()

            elif choice == 2:
                twa.neutralTweets()

            elif choice == 3:
                twa.negativeTweets()

            elif choice == 0:
                break

            else:
                print("\nPlease enter a valid input\n")

        except Exception as e:
            print(e)
            print("That is an invalid choice, please try again")
            traceback.print_exc()

def scrapeData():
    while True:
        print("Scraping data")
        print("1. Product details")
        print("2. Product reviews")
        print("3. PhoneArena specifications")
        print("4. Twitter tweets")
        print("5. Currency conversion rates")
        print("0. Go back\n")

        user_input = input("Enter the Choice: ")

        try:
            choice = int(user_input)

            if choice == 1:
                print("Scraping product details")
                scr.scrape_amazon_products()
                scr.scrape_flipkart_products()
                scr.scrape_croma_products()

            elif choice == 2:
                print("Scraping product reviews")
                scr.scrape_amazon_reviews()
                scr.scrape_flipkart_reviews()
                scr.scrape_croma_reviews()

            elif choice == 3:
                print("Scraping PhoneArena specifications")
                scr.scrape_phonearena_specifications()

            elif choice == 4:
                print("Scraping Twitter tweets")
                scr.scrape_twitter_tweets()

            elif choice == 5:
                scr.scrape_currency_conversion_rates()

            elif choice == 0:
                break

            else:
                print("\nPlease enter a valid input\n")

        except Exception as e:
            print(e)
            print("That is an invalid choice, please try again")
            traceback.print_exc()

def reviewAnalysis():
    while True:
        print("Review analysis")
        print("1. Amazon review analysis")
        print("2. Croma review analysis")
        print("3. Flipkart review analysis")
        print("0. Go back\n")

        user_input = input("Enter the Choice: ")

        try:
            choice = int(user_input)
           
            if choice == 1:
                ra.generateAmazonWordcloud()

            elif choice == 2:
                ra.generateCromaWordcloud()

            elif choice == 3:
                ra.generateFlipkartWordcloud()

            elif choice == 0:
                break

            else:
                print("\nPlease enter a valid input\n")

        except Exception as e:
            print(e)
            print("That is an invalid choice, please try again")
            traceback.print_exc()

def getCosineSimilaritySuggestions(product_name):
    print("Getting suggestions...")
    products_df = pd.read_csv('data/merged/products/Merged_Products_Data_Cleaned.csv')
    product_names = products_df['Product Name']
    
    similar_product_set = set()
    
    for product in product_names:
        X = product_name
        Y = product
          
        # tokenization
        X_list = word_tokenize(X) 
        Y_list = word_tokenize(Y)

        # sw contains the list of stopwords
        sw = stopwords.words('english') 
        l1 =[];l2 =[]
        
        # remove stop words from the string
        X_set = {w for w in X_list if not w in sw} 
        Y_set = {w for w in Y_list if not w in sw}
          
        # form a set containing keywords of both strings 
        rvector = X_set.union(Y_set) 
        for w in rvector:
            if w in X_set: l1.append(1) # create a vector
            else: l1.append(0)
            if w in Y_set: l2.append(1)
            else: l2.append(0)
        c = 0
          
        # cosine formula 
        for i in range(len(rvector)):
                c+= l1[i]*l2[i]
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        
        if cosine >= 0.4:
            similar_product_set.add(Y)
            
    displaySuggestions(similar_product_set)

def displaySuggestions(similar_product_set):
    while True:
        i = 1
        for val in similar_product_set:
            if i > 10:
                break
            print(i, val)
            i+=1  
              
        if i != 1:
            print("0. Go back\n")
        
        
        if len(similar_product_set) == 0:
            print("No results found. Going back...")
            break 
        
        similar_product_list = list(similar_product_set)
        user_input = input("Enter the Choice: ")
    
        try:
            choice = int(user_input)
                    
            if (choice > len(similar_product_list)):
                print("\nPlease enter a valid input\n")
                    
            elif choice == 0:
                break
                
            else:
                product = similar_product_list[choice-1]
                print("Selected product ", product, "\n")
                file = getProductNameDetails(product, False)
                getReviewDetails(product,file)
                getPhoneArenaSpecs(product,file)
                break
        
        except ValueError as e:
            print(e)
            print("Error displaying suggestions")
            traceback.print_exc()

def deEmojify(text):
    try:
        regrex_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u'\U00010000-\U0010ffff'
                u"\u200d"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\u3030"
                u"\ufe0f"
        "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'',text)
    except:
        return text
   
# creating options
while True:
    print("\nMAIN MENU\n")
    print("1. Search by product name")
    print("2. Product analysis visualizations")
    print("3. Twitter sentiment analysis visualizations")
    print("4. Scrape data")
    print("5. Review analysis")
    print("0. Exit\n")
    user_input = input("Enter the Choice: ")
    try:
        choice = int(user_input)

        if choice == 1:
            file = searchByProductName()
            file.close()
            
        elif choice == 2:
            productAnalysisVisualization()

        elif choice == 3:
            twitterAnalysisVisualization()

        elif choice == 4:
            scrapeData()

        elif choice == 5:
            reviewAnalysis()

        elif choice == 0:
            print("Goodbye")
            break

        else:
            print("\nPlease enter a valid input\n")

    except Exception as e:
            print(e)
            traceback.print_exc()
            print("That is an invalid choice, please try again")


