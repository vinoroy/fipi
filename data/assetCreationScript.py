from tinydb import TinyDB, Query
import pandas as pd

db = TinyDB('fiDB.json')
db.purge()


# insert IBM stock
db.insert({'assetID': 'IBM',
           'assetType':'COMMON',
           'purchaseDate': '2012-01-01',
           'purchasePrice':156.5,
           'volume':1000,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'IBM',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert Telus
db.insert({'assetID': 'Telus',
           'assetType':'COMMON',
           'purchaseDate': '2016-01-01',
           'purchasePrice':34.8,
           'volume':1000,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'T.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Apple
db.insert({'assetID': 'Apple',
           'assetType':'COMMON',
           'purchaseDate': '2009-12-01',
           'purchasePrice':30.2,
           'volume':1000,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'AAPL',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})




# AAPL dec 1 2009 30.10



# insert 1748 Des Cassandres asset
# db.insert({'assetID': '1748',
#            'assetType':'REAL',
#            'purchaseDate': '2008-08-01',
#            'purchasePrice':375000,
#            'volume':1,
#            'saleDate':None,
#            'salePrice':None,
#            'priceFeedType':'ARCHIVED',
#            'priceFeedRef':'/Users/vincentroy/Documents/fipi/data/1748market.csv',
#            'debtFeedType':'ARCHIVED',
#            'debtFeedRef':'1748mortgage.csv',
#            'percentOwnership':0.5,
#            'thresholds':[]})


allAssets = db.all()


for ass in allAssets:

    print ass


frame = pd.DataFrame(allAssets)

print frame

