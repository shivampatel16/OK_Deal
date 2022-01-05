# File name:
	# review_analysis.py
# Description:
	# generates an analysis on merged reviews data
# Names of group members:  
       # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# pandas
    # wordcloud
    # matplotlib.pyplot
# Dependency files
    # data/merged/reviews/Merged_Products_Reviews_Cleaned.csv
# Online resources
    # none

#import
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image


# function to prepare dataframe for review analysis
def prepare_dataframe():
    df = pd.read_csv("data/merged/reviews/Merged_Products_Reviews_Cleaned.csv")

    df["Review Detail_amazon"] = df["Review Detail_amazon"].astype(str)
    df["Review Detail_croma"] = df["Review Detail_croma"].astype(str)
    df["Review Detail_flipkart"] = df["Review Detail_flipkart"].astype(str)
    return df

# function to prepare wordcloud for review analysis
def generate_wordcloud(df, col, filename):
    wc = WordCloud(stopwords=STOPWORDS,background_color="white", contour_width=2, contour_color='blue',width=1500, height=750,max_words=150, max_font_size=256,random_state=42)
    wc.generate(' '.join(df[col]))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
    plt.savefig(filename, format="png")
    plt.show()

# display wordclouds
# generate_wordcloud(df,"Review Detail_amazon")
# generate_wordcloud(df,"Review Detail_croma")
# generate_wordcloud(df,"Review Detail_flipkart")

def generateAmazonWordcloud():
    im = Image.open(r"data/merged/reviews/Amazon Reviews Wordcloud.png") 
    im.show() 
    # generate_wordcloud(prepare_dataframe(),"Review Detail_amazon")

def generateCromaWordcloud():
    im = Image.open(r"data/merged/reviews/Croma Reviews Wordcloud.png") 
    im.show() 
    # generate_wordcloud(prepare_dataframe(),"Review Detail_croma")

def generateFlipkartWordcloud():
    im = Image.open(r"data/merged/reviews/Flipkart Reviews Wordcloud.png") 
    im.show() 
    # generate_wordcloud(prepare_dataframe(),"Review Detail_flipkart")
