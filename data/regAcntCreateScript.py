from tinydb import TinyDB, Query
import pandas as pd

db = TinyDB('reg.json')
db.purge()


# insert Manulife Financial Corporation
db.insert({'assetID': 'MFC',
           'assetType':'COMMON',
           'purchaseDate': '2018-02-23',
           'purchasePrice':24.609,
           'volume':700,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'MFC.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert HydroOne
db.insert({'assetID': 'HydroOne',
           'assetType':'COMMON',
           'purchaseDate': '2015-11-05',
           'purchasePrice':20.5,
           'volume':500,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'H.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Pembina pipeline
db.insert({'assetID': 'Pembina',
           'assetType':'COMMON',
           'purchaseDate': '2018-02-16',
           'purchasePrice':41.486,
           'volume':410,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'PPL.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert Rogers
db.insert({'assetID': 'Rogers',
           'assetType':'COMMON',
           'purchaseDate': '2018-02-16',
           'purchasePrice':58.663,
           'volume':300,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'RCI-B.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert BCE
db.insert({'assetID': 'BCE',
           'assetType':'COMMON',
           'purchaseDate': '2012-01-01',
           'purchasePrice':2.858,
           'volume':179,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'BCE.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



allAssets = db.all()


for ass in allAssets:

    print ass


frame = pd.DataFrame(allAssets)

print frame

