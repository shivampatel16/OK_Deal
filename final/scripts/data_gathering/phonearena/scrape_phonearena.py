#!/usr/bin/env python3

# File Name:
	# scrape_phonearena.py
# Description:
	# uses beaufitfulSoup to extract phoneArena products specifications
# Scraping tool used:
	# BeautifulSoup
# Names of group members:  
	# Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# Files that import this module:
	# scripts/scraper.py
# Other modules the file import:
	# re
    # json
    # .phonearena_cleaning > clean_phonearena_scrapped_data
    # warnings
    # requests
# Dependency files
    # data/phonearena/phonearena_scrapped.json
# Online resources
    # https://www.phonearena.com/phones/page/ (for phonearena products specifications)


#imports
import requests
from bs4 import BeautifulSoup
import re
import json
from .phonearena_cleaning import clean_phonearena_scrapped_data

# Scrape and clean PhoneArena data
def scrape_phonearena():

    phone_links = [] # Stores links to various phones on PhoneArena site
    
    print("Started scrapping PhoneArena data")
    
    # Scrape links to all phones on PhoneArena
    for i in range(1, 244):
        res = requests.get('https://www.phonearena.com/phones/page/' + str(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        for i in soup.find_all(class_="thumbnail"):
            phone_links.append(str(i).split(">")[0].split("\"")[3])
      
    # Store scrapped links 
    with open("data/phonearena/phonearena_links.txt", "w") as out_file:
        for phone_link in phone_links:
            out_file.write(phone_link + "\n")
            
    print("\nTotal", len(phone_links), "mobile specifications to scrape")
    print("\nScrapping in progress...\n")
            
    phone_link_count = 1
    phone_specifications = {}
    
    # Detailed scrapping started
    for phone_link in phone_links:
        phone_specification = {}
       
        # For scrapping status
        if phone_link_count % 100 == 0:
            print("Scraped specifications of", phone_link_count, "mobiles from PhoneArena...")
            
        res = requests.get(phone_link)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        phone_name = str(soup.title).split(" specs")[0].split("<title>")[-1].replace("\n", "").strip()
        phone_specification["Phone Name"] = phone_name
        
        # Scrape 'PhoneArena Rating' field
        phonearena_score = None
        for i in soup.find_all(class_="widgetRating__phonearena"):
            phonearena_score = str(i).split("</div>")[0].split(">")[-1].replace(" ", "").replace("\n", "")
        phone_specification["PhoneArena Score"] = phonearena_score
        
        # Scrape 'User Rating' field
        user_score = None
        for i in soup.find_all(class_="widgetRating__user"):
            user_score = str(i).split("</div>")[0].split(">")[-1].replace(" ", "").replace("\n", "")
        phone_specification["User Score"] = user_score
        
        # Scrape 'Released Date' field
        released_date = None
        for i in soup.find_all(class_="widgetQuickSpecs__link calendar"):
            released_date = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0]
        phone_specification["Released Date"] = released_date
        
        # Scrape 'Display' field
        display = None
        for i in soup.find_all(class_="widgetQuickSpecs__link display"):
            display = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["Display"] = display
        
        # Scrape 'Camera' field
        camera = None
        for i in soup.find_all(class_="widgetQuickSpecs__link camera"):
            camera = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["Camera"] = camera
        
        # Scrape 'Hardware' field
        hardware = None
        for i in soup.find_all(class_="widgetQuickSpecs__link hardware"):
            hardware = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["Hardware"] = hardware
        
        # Scrape 'Storage' field
        storage = None
        for i in soup.find_all(class_="widgetQuickSpecs__link storage"):
            storage = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["Storage"] = storage
        
        # Scrape 'Battery' field
        battery = None
        for i in soup.find_all(class_="widgetQuickSpecs__link battery"):
            battery = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["Battery"] = battery
        
        # Scrape 'OS' field
        os = None
        for i in soup.find_all(class_="widgetQuickSpecs__link os"):
            os = str(i).split("<p class=\"widgetQuickSpecs__title_paragraph\">")[1].split("</p>")[0].replace("<br/>", "").split("\n")
        phone_specification["OS"] = os
        
        # Scrape 'Description' field
        description = None
        for i in soup.find_all(class_="widgetTextExpandable__text"):
            description = str(i).split("</p>")[0].split("<p class=\"widgetTextExpandable__text\">")[1].strip()
        phone_specification["Description"] = description
        
        # Scrape 'Pros' field
        pros = None
        for i in soup.find_all(class_="pros"):
            a1 = str(i).split("<ul class=\"pros\">")[1].split("</ul>")[0].strip().replace("<li>", "").replace("</li>", "")
            pros = re.sub('<[^>]+>', '', a1).split("\n")
        phone_specification["Pros"] = pros
        
        # Scrape 'Cons' field
        cons = None
        for i in soup.find_all(class_="cons"):
            a1 = str(i).split("<ul class=\"cons\">")[1].split("</ul>")[0].strip().replace("<li>", "").replace("</li>", "")
            cons = re.sub('<[^>]+>', '', a1).split("\n")
        phone_specification["Cons"] = cons
        
        specs_title = []
        specs_details = []
    
        count = 1
        for i in soup.find_all("thead"):
            if count <= 5:
                specs_title.append(str(i).split("</h3>")[0].split("<h3>")[1].replace("&amp;", "&"))
                count += 1
        
        for i in soup.find_all("tbody"):
            inner_dict = {}
            a1 = str(i)
    
            a = re.findall('<th>(.*?)</td', a1, re.DOTALL)
    
            for i in a:
                i1 = i.split("</th>")[0]
                i2 = re.sub('<[^>]+>', '', i1).strip()
                s1 = i.split("</th>")[1].split("<td>")[1].strip()
                inner_dict[i2] = s1
            specs_details.append(inner_dict)
    
        specs_details = specs_details[:5]
        specs = dict(zip(specs_title, specs_details))
        phone_specification["Detailed Specifications"] = specs
        
        phone_specifications["Phone " + str(phone_link_count)] = phone_specification
            
        phone_link_count += 1
       
      
    # Store scrapped data
    with open("data/phonearena/phonearena_scrapped.json", "w", encoding = 'utf-8') as out_file:
        json.dump(phone_specifications, out_file, indent=4)
     
    print("\nAll", len(phone_links), "mobile specifications scraped successfully!\n")
    print("PhoneArena data scrapping completed")
    
    clean_phonearena_scrapped_data()
            
# scrape_phonearena()