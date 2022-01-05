# File name:
	# Product_Analysis.py
# Description:
	# generates statistics and plot on the merged products data the application outputs
# Names of group members:  
       # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# pandas
       # pandas, numpy, seaborn
       # matplotlib.pyplot
# Dependency files
       # data/merged/products/Merged_Products_Data_Cleaned.csv
       # data/analysis/stats.xlsx
       # data/analysis/Crosstab_variant_amazon.xlsx
       # data/analysis/Crosstab_variant_croma.xlsx
       # data/analysis/Crosstab_variant_flipkart.xlsx
# Online resources
       # none

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# file = open("crosstab.csv","w")

pd.set_option('display.width', 120)

#
def prepare_dataframe():
    df = pd.read_csv("data/merged/products/Merged_Products_Data_Cleaned.csv",encoding='utf-8')
    df = df.drop(['Unnamed: 0'], axis = 1)
    return df
    

# generates statistics
def stats():
    print("\n\nWriting statistics files...\n")
    df = prepare_dataframe()
    df_stats = df.describe()
    df_stats.to_excel("data/analysis/stats.xlsx")
    print("Check out the product statistics at final/data/analysis/stats.xlsx\n")
    ct1 = pd.crosstab(index=df['Product Name'], columns=df['Variant_amazon'])
    ct1.to_excel("data/analysis/Crosstab_variant_amazon.xlsx")
    print("Check out the cross tab files at final/data/analysis/Crosstab_variant_amazon.xlsx\n")

    ct2 = pd.crosstab(index=df['Product Name'], columns=df['Variant_croma'])
    ct2.to_excel("data/analysis/Crosstab_variant_croma.xlsx")
    print("Check out the cross tab files at final/data/analysis/Crosstab_variant_croma.xlsx\n")

    ct3 = pd.crosstab(index=df['Product Name'], columns=df['Variant_flipkart'])
    ct3.to_excel("data/analysis/Crosstab_variant_flipkart.xlsx")
    print("Check out the cross tab files at final/data/analysis/Crosstab_variant_flipkart.xlsx\n")

    print("Writing cross tab files... DONE\n\n")
    #print("Check out the cross tab files at notebooks/Crosstab_variant_{variant_name}\n\n")

    corr = df.corr()

    fig = plt.figure(figsize=(12,12),dpi=80)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='BuPu', robust=True, center=0,
            square=True, linewidths=.5)
    plt.title('Correlation of products data', fontsize=15)
    plt.show()

# creates a triple_plot
def triple_plot(x, title,c):
    fig, ax = plt.subplots(3,1,figsize=(20,10),sharex=True)

    sns.distplot(x, ax=ax[0],color=c)
    ax[0].set(xlabel=None)
    ax[0].set_title('Histogram + KDE')
    sns.boxplot(x, ax=ax[1],color=c)
    ax[1].set(xlabel=None)
    ax[1].set_title('Boxplot')
    sns.violinplot(x, ax=ax[2],color=c)
    ax[2].set(xlabel=None)
    ax[2].set_title('Violin plot')

    fig.suptitle(title, fontsize=16)
    plt.tight_layout(pad=3.0)
    plt.show()

def plot_distribution(df, col1, col2, col3, title):
    plt.figure(figsize=(16,8))
    sns.kdeplot(df[col1],color=custom_colors[0],label="Amazon")
    sns.kdeplot(df[col2],color=custom_colors[1],label="Croma")
    sns.kdeplot(df[col3],color=custom_colors[2],label="Flipkart")
    plt.xlabel(title, fontsize=18)
    plt.legend(loc='upper right',shadow=True, ncol=2)
    plt.title(title)
    plt.show()

custom_colors = ["#3F88C5","#136F63","#F72585","#FFBA08"]
customPalette = sns.set_palette(sns.color_palette(custom_colors))

# gets base price across platforms
def basePriceDistribution():
    plot_distribution(prepare_dataframe(), 'Base Price (INR)_amazon', 'Base Price (INR)_croma', 'Base Price (INR)_flipkart','Base Price Distribution')

# gets discount percentage across platforms                                                              
def discountPercentDistribution():
    plot_distribution(prepare_dataframe(), 'Discount (%)_amazon', 'Discount (%)_croma', 'Discount (%)_flipkart','Discount % Distribution')

# gets discount price distribution
def discountPriceDistribution():
    plot_distribution(prepare_dataframe(), 'Discounted Price (INR)_amazon', 'Discounted Price (INR)_croma', 'Discounted Price (INR)_flipkart','Discounted Price Distribution')

# gets average rating on amaaon
def averageRatingDistribution():
    plot_distribution(prepare_dataframe(), 'Average Rating (5)_amazon', 'Average Rating (5)_croma', 'Average Rating (5)_flipkart','Average Rating (5) Distribution')

# gets all distributions
def showAllDistributionPlots():
    basePriceDistribution()
    discountPercentDistribution()
    discountPriceDistribution()
    averageRatingDistribution()

# gets base price plot
def basePriceTriplePlot():
    triple_plot(prepare_dataframe()['Base Price (INR)_amazon'], "Base Price Amazon", custom_colors[0] )
    triple_plot(prepare_dataframe()['Base Price (INR)_croma'], "Base Price Croma", custom_colors[1] )
    triple_plot(prepare_dataframe()['Base Price (INR)_flipkart'], "Base Price Flipkart", custom_colors[2])

# gets discounts percentage plot
def discountPercentTriplePlot():
    triple_plot(prepare_dataframe()['Discount (%)_amazon'], "Discount (%) Amazon", custom_colors[0] )
    triple_plot(prepare_dataframe()['Discount (%)_croma'], "Discount (%) Croma", custom_colors[1] )
    triple_plot(prepare_dataframe()['Discount (%)_flipkart'], "Discount (%) Flipkart", custom_colors[2])

# gets price triple plots
def discountedPriceTriplePlot():
    triple_plot(prepare_dataframe()['Discounted Price (INR)_amazon'], "Discounted Price (INR) Amazon", custom_colors[0] )
    triple_plot(prepare_dataframe()['Discounted Price (INR)_croma'], "Discounted Price (INR) Croma", custom_colors[1] )
    triple_plot(prepare_dataframe()['Discounted Price (INR)_flipkart'], "Discounted Price (INR) Flipkart", custom_colors[2])

#gets the average rating triple plots
def averageRatingTriplePlot():
    triple_plot(prepare_dataframe()['Average Rating (5)_amazon'], "Average Rating (5) Amazon", custom_colors[0] )
    triple_plot(prepare_dataframe()['Average Rating (5)_croma'], "Average Rating (5) Croma", custom_colors[1] )
    triple_plot(prepare_dataframe()['Average Rating (5)_flipkart'], "Average Rating (5) Flipkart", custom_colors[2])
