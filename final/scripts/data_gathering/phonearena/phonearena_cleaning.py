#!/usr/bin/env python3

# File name:
	# phonearena_cleaning.py
# Description:
	# formats phonearena specifications extrated csv file. cleans it
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
	# scrape_phonearena.py
# Other modules the file import:
	# lxml > html
    # os, pandas , time
    # warnings
    # requests
# Dependency files
    # data/phonearena/phonearena_scrapped.json
    # data/phonearena/phonearena_cleaned.csv
    # data/phonearena/phonearena_raw.csv
# Online resources
    # none

# imports
import json
import pandas as pd
import numpy as np

# Clean PhoneArena scrapped data
def clean_phonearena_scrapped_data():
    
    # Reading uncleaned data from phonearena_scrapped.json 
    with open('data/phonearena/phonearena_scrapped.json', 'r', encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    
    # Column names for the scrapped data    
    column_names = ["Phone Name", "PhoneArena Score", "User Score", "Released Date", "Display", "Camera", "Hardware", "Storage", "Battery", "OS", "Description", "Pros", "Cons", "Detailed Specifications"]
    f2 = pd.DataFrame(columns = column_names)
    
    index = 0
    for key in data.keys():
        f2.loc[index] = tuple(data[key].values())
        index += 1
    
    # Storing uncleaned data
    f2.to_csv('data/phonearena/phonearena_raw.csv', index=False)
    
    print("\nStarted cleaning scrapped data from PhoneArena\n")
    
    # Cleaning starts
    f2.fillna(value=np.nan, inplace=True)
    f2 = f2.replace(r'^\s*$', np.NaN, regex=True)
    
    column_names = ["Phone Name", "PhoneArena Score", "User Score", "Released Date", "Display", "Camera", "Hardware", "Storage", "Battery", "OS", "Description", "Pros", "Cons", "Detailed Display", "Detailed Hardware", "Detailed Battery", "Detailed Camera", "Detailed Design", "Detailed Cellular", "Detailed Multimedia", "Detailed Connectivity & Features", "Detailed Phone Features", "Detailed Regulatory Approval"]
    f3 = pd.DataFrame(columns = column_names)
    
    
    month_to_number_long = {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04',              
                           'May' : '05', 'June' : '06', 'July' : '07', 'August' : '08', 
                           'September' : '09', 'October' : '10', 'November' : '11', 'December' : '12'}
    
    month_to_number_short = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04',              
                           'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug' : '08', 
                           'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}
    
    index = 0
    for i, j in f2.iterrows():
        
        # Cleaning 'Released Date' field
        new_j3 = ""
        if str(j[3]) != "nan":
            try:
                if len(j[3].split()) == 2:
                    j[3] = j[3].split()[1] + '-' + month_to_number_long[j[3].split()[0]]
                    new_j3 = j[3]
                elif len(j[3].split()) == 3:
                    j[3] = j[3].split()[2] + '-' + month_to_number_short[j[3].split()[0]] + '-' + j[3].split()[1][:-1]
                    new_j3 = j[3]
            except KeyError:
                new_j3 = "No Information"
        
        # Cleaning 'Display' field
        new_j4 = ""
        if str(j[4]) != "nan":
            for display in j[4]:
                if display != "":
                    new_j4 += display + "\n"
        
        # Cleaning 'Camera' field
        new_j5 = ""
        if str(j[5]) != "nan":
            for camera in j[5]:
                if camera != "":
                    new_j5 += camera + "\n"
        
        # Cleaning 'Hardware' field
        new_j6 = ""
        if str(j[6]) != "nan":
            for hardware in j[6]:
                if hardware != "":
                    new_j6 += hardware + "\n"
        
        # Cleaning 'Storage' field
        new_j7 = ""
        if str(j[7]) != "nan":
            new_j7 = list(j[7])[0]
        
        # Cleaning 'Battery' field
        new_j8 = ""
        if str(j[8]) != "nan":
            new_j8 = list(j[8])[0]
        
        # Cleaning 'OS' field
        new_j9 = ""
        if str(j[9]) != "nan":
            for os in j[9]:
                if os != "":
                    new_j9 += os + "\n"
        
        # Cleaning 'Pros' field
        new_j11 = ""
        if str(j[11]) != "nan":
            for pros in j[11]:
                if pros != "":
                    new_j11 += pros + "\n"
        
        # Cleaning 'Cons' field
        new_j12 = ""
        if str(j[12]) != "nan":
            for cons in j[12]:
                if cons != "":
                    new_j12 += cons + "\n"
        
        # Cleaning 'Description' field
        f3.loc[index] = ("" * 23)
        if str(j[13]) != "nan":
            for key1, values in j[13].items():
                description = ""
                for key, value in values.items():
                    description += str(key) + " " + str(value) + "\n"
                f3.at[index, "Detailed " + key1] = description
        
        f3.at[index, "Phone Name"] = str(j[0])
        f3.at[index, "PhoneArena Score"] = str(j[1])
        f3.at[index, "User Score"] = str(j[2])
        f3.at[index, "Released Date"] = new_j3
        f3.at[index, "Display"] = new_j4[:-1]
        f3.at[index, "Camera"] = new_j5[:-1]
        f3.at[index, "Hardware"] = new_j6[:-1]
        f3.at[index, "Storage"] = new_j7
        f3.at[index, "Battery"] = new_j8
        f3.at[index, "OS"] = new_j9[:-1]
        f3.at[index, "Description"] = str(j[10])
        f3.at[index, "Pros"] = new_j11[:-1]
        f3.at[index, "Cons"] = new_j12[:-1]
    
        index += 1
    
    # Storing cleaned data to CSV file    
    f3.to_csv('data/phonearena/phonearena_cleaned.csv', index=False)
    
    print("PhoneArena Specifications for Products:", f3.shape) 
    print("Cleaning completed for the scrapped data from PhoneArena")