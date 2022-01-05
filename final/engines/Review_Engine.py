# file name:
	# Review_Engine.py
# description:
	#  Define reveiw class/object for UI usage. Contains logic to transform review information from cleaned files.
# names of group members:  
    # Adrian Menezes(ajmeneze@andrew.cmu.edu), Gautam Naik(gnaik@andrew.cmu.edu),
	# Michael Affare(maffare@andrew.cmu.edu), Ruchi Bhatia(rsbhatia@andrew.cmu.edu),
	# Shivam Patel(shpatel@andrew.cmu.edu), Yao-Chang Wang(yaochanw@andrew.cmu.edu)
# files that import this module:
	# main.py
# other modules the file import:
	# json
# dependency files
    # data/amazon/amazon_reviews_cleaned.json
    # data/flipkart/flipkart_reviews_cleaned.json
    # data/croma/croma_reviews_cleaned.json
# online resources
    # none

import json


class Review:

    def __init__(self, phone_name):
        self._prod_name = phone_name
        with open('data/amazon/amazon_reviews_cleaned.json', 'r') as f_amazon:
            self.result_amazon = json.load(f_amazon)
        with open('data/flipkart/flipkart_reviews_cleaned.json', 'r') as f_flipkart:
            self.result_flipkart = json.load(f_flipkart)
        with open('data/croma/croma_reviews_cleaned.json', 'r') as f_croma:
            self.result_croma = json.load(f_croma)

    def get_amazon(self):
        return self.result_amazon[self._prod_name][0:10] if self._prod_name in self.result_amazon else None

    def get_flipkart(self):
        return self.result_flipkart[self._prod_name][0:10] if self._prod_name in self.result_flipkart else None

    def get_croma(self):
        return self.result_croma[self._prod_name][0:10] if self._prod_name in self.result_croma else None


if __name__ == '__main__':
    review = Review('apple iphone xr')  # samsung galaxy a52

    print("--------Amazon Reviews--------")
    result = review.get_amazon()
    if result is not None:
        for r in result:
            print(r)
    else:
        print('No Amazon Review Data')

    print("\n\n--------FlipKart Reviews--------")
    result = review.get_flipkart()
    if result is not None:
        for r in result:
            print(r)
    else:
        print('No Flipkart Review Data')

    print("\n\n--------Croma Reviews--------")
    result = review.get_croma()
    if result is not None:
        for r in result:
            print(r)
    else:
        print('No Croma Review Data')
