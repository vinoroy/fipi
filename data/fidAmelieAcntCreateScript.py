from tinydb import TinyDB, Query
import pandas as pd

db = TinyDB('fidAmelie.json')
db.purge()


# insert Scotia Bank
db.insert({'assetID': 'Scotia',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':82.81,
           'volume':60,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'BNS.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Royal Bank first purchase
db.insert({'assetID': 'Royal-1',
           'assetType':'COMMON',
           'purchaseDate': '2014-09-29',
           'purchasePrice':81.1,
           'volume':60,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'RY.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert Royal Bank second purchase
db.insert({'assetID': 'Royal-2',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':101.32,
           'volume':50,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'RY.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert TD
db.insert({'assetID': 'TD',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':72.75,
           'volume':70,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'TD.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert Enbridge
db.insert({'assetID': 'Enbridge',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':49.03,
           'volume':100,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'ENB.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Fortis
db.insert({'assetID': 'Fortis',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':47.305,
           'volume':105,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'FTS.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert HydroOne
db.insert({'assetID': 'HydroOne',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':22.41,
           'volume':225,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'H.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Canadian Tire
db.insert({'assetID': 'CanadianTire',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':158.38,
           'volume':30,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'CTC-A.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert CP
db.insert({'assetID': 'CP',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':224.42,
           'volume':20,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'CP.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



# insert Pembina Pipe Line
db.insert({'assetID': 'Pembina',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':41.63,
           'volume':121,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'PPL.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})


# insert Telus
db.insert({'assetID': 'Telus',
           'assetType':'COMMON',
           'purchaseDate': '2017-10-27',
           'purchasePrice':46.71,
           'volume':135,
           'saleDate':None,
           'salePrice':None,
           'priceFeedType':'YAHOO',
           'priceFeedRef':'T.TO',
           'debtFeedType':None,
           'debtFeedRef':None,
           'percentOwnership':1,
           'thresholds':[]})



allAssets = db.all()


for ass in allAssets:

    print ass


frame = pd.DataFrame(allAssets)

print frame
