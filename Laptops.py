import keepa
import numpy as np
from numpy.core.fromnumeric import prod, product

def getKeepaLaptop():
    accesskey = 'ep1re2emp4vq52o7o0cmrtp6fkrkv3m6mrjqu7btspqst3arj5koivj46gc96kel' # enter real access key here
    api = keepa.Keepa(accesskey)

    product_parms = {
        'page':0,
        'categories_include': [565108,13896615011,13896609011],
        'title': "HP ENVY Ryzen",
        }
    products_asins = api.product_finder(product_parms)

    asins = np.asarray(products_asins)

    products = api.query(asins)

    result = []
    # print(products[0].keys())
    for count,product in enumerate(products):
        li = []
        li.append(product['asin'])
        li.append(product['title'])
        # print(product['data']['NEW'])
        # print(product['data']['NEW_time'])
        result.append(li)
        # aoa.append(product['title'])
    
    return result
