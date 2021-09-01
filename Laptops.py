import enum
from os import access
from re import M
import keepa
import numpy as np
import datetime
from numpy.core.fromnumeric import prod, product
from numpy.core.numeric import NaN
from numpy.lib.function_base import append
import math
import re
import pandas as pd


class Laptops:
    # class attributes
    CONST_INDEX = 0
    CONST_TUPLE_DIC = 1

    def __init__(self, search):

        self.product_parms = {
            'categories_include': [565108, 13896615011, 13896609011],
            'title': "",
            'current_SALES_lte': 20000
        }
        # enter real access key here
        self.accesskey = 'ep1re2emp4vq52o7o0cmrtp6fkrkv3m6mrjqu7btspqst3arj5koivj46gc96kel'

        if search:
            self.product_parms["title"] = search

        self.initial_set(self.accesskey)

    def initial_set(self, accesskey):
        api = keepa.Keepa(accesskey)
        products_asins = api.product_finder(self.product_parms)
        self.products = api.query(products_asins)

    def get_asins(self):
        asins = []
        for product in enumerate(self.products):
            asins.append(product[self.CONST_TUPLE_DIC]['asin'])
        return asins

    def get_titles(self):
        titles = []
        for product in enumerate(self.products):

            titles.append(product[self.CONST_TUPLE_DIC]['title'])

        return titles

    def get_salesRanks(self):
        sales_ranks = []
        for product in enumerate(self.products):
            df_sales = product[self.CONST_TUPLE_DIC]['data']['df_SALES']
            current_sale = df_sales['value'].tail(1).item()
            sales_ranks.append(current_sale)
        return sales_ranks

    def get_meanNewPrice(self):
        meanNewPrices = []
        # date var
        last_30date = datetime.datetime.now() - datetime.timedelta(30)
        last_5date = datetime.datetime.now() - datetime.timedelta(5)
        now_date = datetime.datetime.now()

        for product in enumerate(self.products):
            df_newPrice = product[self.CONST_TUPLE_DIC]['data']['df_NEW']
            df_newPrice_30days = df_newPrice.loc[last_30date:now_date]
            mean_newPrice = df_newPrice_30days["value"].mean()
            if(math.isnan(mean_newPrice)):
                mean_newPrice = df_newPrice["value"].mean()
                if(math.isnan(mean_newPrice)):
                    mean_newPrice = float(0.00)
            meanNewPrices.append(mean_newPrice)
        return meanNewPrices

    def get_newPrice(self):
        for product in enumerate(self.products):
            df_newPrice = product[self.CONST_TUPLE_DIC]['data']['df_NEW']
            newPrices_df = pd.concat(df_newPrice)
        return newPrices_df

    def get_variants(self):
        variants = []
        ram_size = ""
        ssd_size = ""
        hdd_size = ""

        for title in self.get_titles():
            ram = re.search("(\d*)\s?GB\s?(?i:memory|ram|ddr4)", title, re.I)
            if ram:
                ram_size = ram.group(1)

            ssd = re.search(
                "(\d*)\s?(?i:GB|TB)\s?(?i:ssd|pcie|nvme|solid state)", title, re.I)
            if ssd:
                ssd_size = ssd.group(1)

            hdd = re.search(
                "(\d*)\s?(?i:GB|TB)\s?(?i:hdd|hard drive)", title, re.I)
            if hdd:
                hdd_size = hdd.group(1)
                variant = f'{ram_size}GB Ram | {ssd_size}GB/TB SSD + {hdd_size} GB/TB HDD'
            else:
                variant = f'{ram_size}GB Ram | {ssd_size}GB/TB SSD'

            variants.append(variant)
        return variants


# l=Laptops("HP Envy 17.3 i7 1165G7")
# asins = l.get_asins()
# titles = l.get_titles()
# variants = l.get_variants()

def getKeepaLaptop():
    # enter real access key here
    accesskey = 'ep1re2emp4vq52o7o0cmrtp6fkrkv3m6mrjqu7btspqst3arj5koivj46gc96kel'
    api = keepa.Keepa(accesskey)

    product_parms = {
        'categories_include': [565108, 13896615011, 13896609011],
        'title': "Asus Zephyrus G14 Ryzen 9",
        'current_SALES_lte': 50000
    }

    products_asins = api.product_finder(product_parms)
    asins = np.asarray(products_asins)
    products = api.query(asins)

    result = []
    # print(products[0].keys())
    for count, product in enumerate(products):
        li = []

        # date var
        last_30date = datetime.datetime.now() - datetime.timedelta(30)
        last_5date = datetime.datetime.now() - datetime.timedelta(5)
        now_date = datetime.datetime.now()

        # get current sales rank
        df_sales = product['data']['df_SALES']
        # df_sales_5days = df_sales.loc[last_5date:now_date]
        # mean_sale = round(df_sales_5days["value"].mean())
        current_sale = df_sales['value'].tail(1).item()

        # get New product price df
        df_newPrice = product['data']['df_NEW']
        df_newPrice_30days = df_newPrice.loc[last_30date:now_date]
        mean_newPrice = df_newPrice_30days["value"].mean()
        if(math.isnan(mean_newPrice)):
            mean_newPrice = df_newPrice["value"].mean()
            if(math.isnan(mean_newPrice)):
                mean_newPrice = float(0.00)

        # prepare upload gSheet array
        li.append(product['asin'])
        li.append(product['title'])
        li.append(current_sale)
        li.append(mean_newPrice)
        li.append(product['size'])
        result.append(li)

    return result
