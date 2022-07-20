import keepa
import numpy as np
import datetime
import math
import re


class Laptops:

    def __init__(self, searchKeyWords, maxSalesRank=15000):
        self.product_parms = {
            'categories_include': [565108, 13896615011, 13896609011],
            'title': searchKeyWords,
            'current_SALES_lte': maxSalesRank
        }
        self.__accesskey = 'ep1re2emp4vq52o7o0cmrtp6fkrkv3m6mrjqu7btspqst3arj5koivj46gc96kel'

    def __getKeepaApi(self):
        return keepa.Keepa(self.__accesskey)

    def getSearchedProductDetail(self):
        aoa = []  # result array of array
        keepa = self.__getKeepaApi()
        asins = keepa.product_finder(self.product_parms)
        products = keepa.query(asins, offers=20)

        lastMonth = datetime.datetime.now() - datetime.timedelta(30)
        lastWeek = datetime.datetime.now() - datetime.timedelta(7)
        today = datetime.datetime.now()

        for index, product in enumerate(products):
            li = []

            salesRankDataframe = product['data']['df_SALES']
            curSalesRank = salesRankDataframe['value'].tail(1).item()

            # price Of New Condition Product Dataframe
            priceOfNewDF = product['data']['df_NEW']
            # price Of Avg Cur Month New Condition Product
            priceOfAvgMonNewDF = priceOfNewDF.loc[lastMonth:today]
            meanPriceOfAvgMonNew = priceOfAvgMonNewDF["value"].mean()

            if(math.isnan(meanPriceOfAvgMonNew)):
                # if price records less than a month, get the avg of all price value
                meanPriceOfAvgMonNew = priceOfNewDF["value"].mean()
                if(math.isnan(meanPriceOfAvgMonNew)):
                    # if no price record, set 0.00
                    meanPriceOfAvgMonNew = float(0.00)

            estimateSales = self.getSalesFigureEst(curSalesRank)
            productSpeci = self.getVariant(product["title"])
            li.append(product["asin"])
            li.append(product["title"])
            li.append(curSalesRank)
            li.append(meanPriceOfAvgMonNew)
            li.append(productSpeci)
            li.append(round(estimateSales, 0))
            aoa.append(li)

        return aoa

    def getSalesFigureEst(self, salesRank):
        sr = []
        for i in range(15):
            sr.append((i+1)*1000)
        sn = [494, 247, 159, 125, 105, 85, 65, 55, 53, 50, 48, 46, 44, 42, 40]

        coef = np.polyfit(sr, sn, 3)

        return np.polyval(coef, salesRank)

    def getVariant(self, title):
        ramReg = re.search("(\d*)\s?GB\s?(?i)(memory|ram|ddr4|Storage)", title, re.I)
        ssdReg = re.search(
            "(\d*)\s?(GB|TB)\s?(?i)(ssd|pcie|nvme|solid state|m.2)", title, re.I)
        hddReg = re.search(
            "(\d*)\s?(GB|TB)\s?(?i)(hdd|hard drive)", title, re.I)

        ram = 0 if ramReg is None else ramReg.group(1)
        ssd = 0 if ssdReg is None else ssdReg.group(1)
        hdd = 0 if hddReg is None else hddReg.group(1)

        return f'{ram}GB RAM | {ssd}GB/TB SSD + {hdd}GB/TB HDD'