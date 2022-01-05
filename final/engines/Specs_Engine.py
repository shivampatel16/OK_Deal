import pandas as pd


class ProductSpecs:
    dict_phoneArena = {}

    def __init__(self, phone_name):
        self._prod_name = phone_name.lower().strip()
        specs = pd.read_csv("data/phonearena/phonearena_cleaned.csv")
        #phoneArena specs info
        for index, row in specs.iterrows(): 
            self.dict_phoneArena[row['Phone Name'].strip().lower()] = {}
            for column in specs.columns[1:9]:
                self.dict_phoneArena[row['Phone Name'].strip().lower()][column] = row[column]

    def get_specs(self):
        return self.dict_phoneArena[self._prod_name] if self._prod_name in self.dict_phoneArena else None


if __name__ == '__main__':
    product = ProductSpecs('Apple iPhone 13')  
    print("--------Phone Specifications--------")
    result = product.get_specs()
    if result is not None:
        print(result)
    else:
        print('No Product Specifications Data')

    

   






