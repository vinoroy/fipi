#!/usr/bin/env python
"""
@author: Vincent Roy [D]

This module implements the abstract and concrete securities classes

"""



from asset import *
from pandas_datareader import data as pdr



class Security(Asset):
    """
    This class is the abstract securities class that is the superclass of all securities type assets

    Attributes :


    """


    def __init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker):
        Asset.__init__(self, assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker)



class Equity(Security):
    """
    This class is the abstract equity class that is the superclass of all equities type assets

    Attributes :


    """

    def __init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker):
        Security.__init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker)



class CommonStock(Equity):
    """
    This class implements a concrete common stock class that is a child of the equity class


    Attributes :

        - none


    """

    def __init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker):
        Equity.__init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker)
        self.assetType = 'COMMON'


    def getHistoricalPrice(self, startDate, endDate):
        """
        Gets the historical price at a given date for a unit of the asset. 

        Args :
        - startDate : (string) start date of the extraction (format YY-MM-DD)
        - endDate : (string) end date of the extraction (format YY-MM-DD)

        Return :
            - (Dataframe) 
        """

        try :
            histValues = pdr.DataReader(self.ticker, data_source='yahoo', start=startDate,end=endDate)

            return histValues

        except:

            return None





class PreferredStock(Equity):
    """
    This class implements a concrete preferred stock class that is a child of the equity class


    Attributes :

        - none


    """

    def __init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker):
        Equity.__init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker)
        self.assetType = 'PREFERRED'












