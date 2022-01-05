# file name:
	# Product_Engine.py
# description:
	# Define product class/object for UI usage. Contains logic to transform product information from merged file.
# names of group members:  
    # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# files that import this module:
	# main.py
# other modules the file import:
	# pandas
# dependency files
    # data/merged/products/Merged_Products_Data_Cleaned.csv
# online resources
    # none

import pandas as pd


class Product:
    dict_amazon = {}
    dict_flipkart = {}
    dict_croma = {}

    def __init__(self, phone_name):
        self._prod_name = phone_name
        products = pd.read_csv('data/merged/products/Merged_Products_Data_Cleaned.csv')
        product_amazon = products.iloc[:, 1:9].drop_duplicates()
        product_flipkart = products.iloc[:, [1, 16, 17, 18, 19, 20, 21, 22]].drop_duplicates()
        product_croma = products.iloc[:, [1, 9, 10, 11, 12, 13, 14, 15]].drop_duplicates()

        # amazon info
        for index, row in product_amazon.iterrows():
            if row['Product Name'].strip() not in self.dict_amazon:
                self.dict_amazon[row['Product Name'].strip()] = {}
            self.dict_amazon[row['Product Name'].strip()].setdefault(row['Variant_amazon'], {}).update(
                {'price': row['Base Price (INR)_amazon'], 'discount': row['Discount (%)_amazon'],
                 'discounted_price': row['Discounted Price (INR)_amazon'],
                 'average_rating': row['Average Rating (5)_amazon'], 'URL': row['URL_amazon']})

        # flipkart info
        for index, row in product_flipkart.iterrows():
            if row['Product Name'].strip() not in self.dict_flipkart:
                self.dict_flipkart[row['Product Name'].strip()] = {}
            self.dict_flipkart[row['Product Name'].strip()].setdefault(row['Variant_flipkart'].replace("????", ", "),
                                                                       {}).update(
                {'price': row['Base Price (INR)_flipkart'], 'discount': row['Discount (%)_flipkart'],
                 'discounted_price': row['Discounted Price (INR)_flipkart'],
                 'average_rating': row['Average Rating (5)_flipkart'], 'URL': row['URL_flipkart']})

        # Croma info
        for index, row in product_croma.iterrows():
            if row['Product Name'].strip() not in self.dict_croma:
                self.dict_croma[row['Product Name'].strip()] = {}
            self.dict_croma[row['Product Name'].strip()].setdefault(row['Variant_croma'], {}).update(
                {'price': row['Base Price (INR)_croma'], 'discount': row['Discount (%)_croma'],
                 'discounted_price': row['Discounted Price (INR)_croma'],
                 'average_rating': row['Average Rating (5)_croma'], 'URL': row['URL_croma']})

    def get_amazon(self):
        return self.dict_amazon[self._prod_name] if self._prod_name in self.dict_amazon else None

    def get_flipkart(self):
        return self.dict_flipkart[self._prod_name] if self._prod_name in self.dict_flipkart else None

    def get_croma(self):
        return self.dict_croma[self._prod_name] if self._prod_name in self.dict_croma else None


if __name__ == '__main__':
    product = Product('samsung galaxy m12')  # apple iphone se

    print("--------Amazon Products--------")
    result = product.get_amazon()
    if result is not None:
        for variant, spec in result.items():
            print(variant)
            print(spec)
    else:
        print('No Amazon Product Data')

    print("\n\n--------Flipkart Products--------")
    result = product.get_flipkart()
    if result is not None:
        for variant, spec in result.items():
            print(variant)
            print(spec)
    else:
        print('No Flipkart Product Data')

    print("\n\n--------Croma Products--------")
    result = product.get_croma()
    if result is not None:
        for variant, spec in result.items():
            print(variant)
            print(spec)
    else:
        print('No Croma Product Data')
