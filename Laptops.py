from re import M
import keepa
import numpy as np
import datetime
from numpy.core.fromnumeric import prod, product
from numpy.core.numeric import NaN
from numpy.lib.function_base import append
import math

def getKeepaLaptop(serach_word):
    accesskey = 'ep1re2emp4vq52o7o0cmrtp6fkrkv3m6mrjqu7btspqst3arj5koivj46gc96kel' # enter real access key here
    api = keepa.Keepa(accesskey)

    product_parms = {
        'categories_include': [565108,13896615011,13896609011],
        'title': serach_word,
        'current_SALES_lte':50000
        }

    products_asins = api.product_finder(product_parms)
    asins = np.asarray(products_asins)
    products = api.query(asins)

    result = []
    # print(products[0].keys())
    for count,product in enumerate(products):
        li = []

        # date var
        last_30date = datetime.datetime.now() - datetime.timedelta(30)
        last_5date = datetime.datetime.now() - datetime.timedelta(5)
        now_date = datetime.datetime.now()

        # get current sales rank
        df_sales = product['data']['df_SALES']
        df_sales_5days = df_sales.loc[last_5date:now_date]
        mean_sale = round(df_sales_5days["value"].mean())
        current_sale=df_sales['value'].tail(1).item()

        # get New product price df
        df_newPrice = product['data']['df_NEW']
        df_newPrice_30days =df_newPrice.loc[last_30date:now_date]
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
