#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module implements the base class asset that is the superclass of all financial assets.

"""


from __future__ import division


import numpy as np
import pandas as pd
import datetime


class Asset(object):
    """
    This class is the base class asset that is the superclass of all financial assets


    Attributes :

        - assetID : (string) asset ID
        - assetType : (string) type of asset (ex securities, real-estate, etc.)
        - purchaseDate : (float) dateNumber of the purchase date of the asset
        - purchasePrice : (float) purchase price of the asset
        - saleDate : (float) dateNumber of sale date of the asset
        - salePrice : (float) unit price of the asset at time of sale
        - volume : (float) number of asset units
        - percentOwnership : (float) percent ownership of the asset
        - ticker : (string) id of stock on martkets
        - perfMatrix : (DataFrame) time stamped matrix with the following columns
                Open - day market open of stock
                High - day market high of stock
                Low - day market low of stock
                Close - day market close of stock
                Adj Close - day market close adjusted for dividends
                Volume - day traded volume of stock
                Market - market value of asset = number of stock * adj close
                Est Profit - profit with regards to acquisition value of the asset
                % Est Profit - % porfit of asset
                RateReturn
                Time Delta
                % Return
                Annual Return
        - perfVector : (DataFrame) vector (actually a one row dataFrame) with the following attributes based on the last trading day
                Asset ID
                Purchase date
                Purchase price
                Volume
                Acquisition
                Adj Close
                Market
                Est Profit
                % Est Profit
                Annual Return
        - annualReturn : (float) based on the simple return
        
        
    """


    def __init__(self,assetID='', purchaseDate=None, purchasePrice=None, saleDate=None, salePrice=None, volume=None, percentOwnership=None,ticker=None):
        self.assetID = assetID
        self.assetType = ''
        self.purchaseDate = purchaseDate
        self.purchasePrice = purchasePrice
        self.saleDate = saleDate
        self.salePrice = salePrice
        self.volume = volume
        self.percentOwnership = percentOwnership
        self.ticker = ticker
        self.perfMatrix = []
        self.perfVector = []
        self.annualReturn = []


        self.setAssetData()


    def calcAcquistionValue(self):
        """
        Calculates the acquisition value based on the purchase price of the asset and the volume

        Return :
            - (float) acquisition value of the asset
        """

        return self.purchasePrice * self.volume



    def getHistoricalPrice(self,startDate,endDate):
        """
        Gets the historical prices (open, low, high, close, adj close and volume) between a set of dates 

        Args :
        - startDate : (string) start date of the extraction (format YY-MM-DD)
        - endDate : (string) end date of the extraction (format YY-MM-DD)

        Return :
            - (DataFrame) open, low, high, close, adj close and volume matrix between a set of dates 
        """

        raise NotImplementedError("Should have implemented this")



    def calcAssetPerformanceMatrix(self,startDate,endDate):
        """
        Calculates the asset performance matrix composed of the key performance indicators for each of the trading dates
        between the selected start and end dates :
            - Open, High, Low, Close, Adj Close and volume
            - Market value of the asset
            - Estimated profit of the asset
            - % Estimated profit of the asset
            - Annual return
        
        Args :
        - startDate : (string) start date of the extraction (format YY-MM-DD)
        - endDate : (string) end date of the extraction (format YY-MM-DD)


        Return :
            - (DataFrame) matrix of the key performance indicators for each date 
        """

        # get the price data from the feed
        perfMat = self.getHistoricalPrice(startDate, endDate)

        # calculate the performance values for each time stamp
        perfMat['Market'] = perfMat[['Adj Close']] * self.volume
        perfMat['Est Profit'] = perfMat['Market'] - self.calcAcquistionValue()
        perfMat['% Est Profit'] = perfMat['Est Profit'] / self.calcAcquistionValue() * 100

        # calculate the daily simple return
        perfMat['RateReturn'] = perfMat['Adj Close'] / perfMat['Adj Close'].shift(1) - 1

        # calculate the elapsed time in years
        perfMat['Time Delta'] = (perfMat.index.values - perfMat.index.values[0]) / np.timedelta64(1, 'D') / 365

        #
        perfMat['% Return'] = perfMat['Adj Close'] / perfMat[0:]['Adj Close'].values[0]

        # calculate the annual return
        perfMat['Annual Return'] = perfMat['% Return'] ** (1 / perfMat['Time Delta']) - 1


        perfMat = perfMat.round(2)


        # if the asset is sold then insert nans for the performance values
        if self.saleDate != None:

            perfMat.loc[self.saleDate:,'Market'] = np.nan
            perfMat.loc[self.saleDate:,'Est Profit'] = np.nan
            perfMat.loc[self.saleDate:,'% Est Profit'] = np.nan


        return perfMat


    def calcCurrentPerformanceVector(self):
        """
        Calculates the asset performance vector composed of the key performance indicators for the last valid trading 
        day :
            - Open, High, Low, Close, Adj Close and volume
            - Acquistion value of the asset
            - Market value of the asset
            - Estimated profit of the asset
            - % Estimated profit of the asset
            
        Args :
            - None

    
        Return :
            - (DataFrame) (actually a one row dataFrame) indicators above based on the last trading day
        """


        # get the last row of the performance matrix
        perfVector = self.perfMatrix.iloc[[-1]]

        # extract the desired columns
        perfVector = perfVector[['Adj Close', 'Market', 'Est Profit', '% Est Profit','Annual Return']]

        # add other indicators
        perfVector['Asset ID'] = self.assetID
        perfVector['Purchase date'] = self.purchaseDate
        perfVector['Purchase price'] = self.purchasePrice
        perfVector['Volume'] = self.volume
        perfVector['Acquisition'] = self.volume * self.purchasePrice


        # reorganize the sequence of the indicators
        perfVector = perfVector[['Asset ID','Purchase date','Purchase price','Volume','Acquisition','Adj Close', 'Market',
                                 'Est Profit', '% Est Profit', 'Annual Return']]


        return perfVector




    def calcSaleProfit(self):
        """
        Calculates the sale profit based on the sale value minus the acquistion value of the asset

        Return :
            - (float) profit of the sale of the asset. If the asset has not been sold the result is -1
        """

        # only perform the calculation if the asset has been sold
        if self.saleDate != None:
            result = (self.salePrice - self.purchasePrice) * self.volume

        else:
            result = None

        return result




    def setAssetData(self):
        """
        This method is called after the asset is created to set the perfMatrix and the perfVector 
        
        Args :
            - None

        Return :
            - None
        """


        # determin the end date of the oerformance matrix based on the status of the asset. If the asset has already been
        # sold then the end date will correspond to the sale date, inf not then it is the last trading day
        if self.saleDate != None:

            endDate = self.saleDate

        else:

            endDate = datetime.datetime.now().strftime("%Y-%m-%d")


        # calculate the performance matrix
        self.perfMatrix = self.calcAssetPerformanceMatrix(self.purchaseDate,endDate)

        # calculate the performace vector
        self.perfVector = self.calcCurrentPerformanceVector()

        # get the annual return from the perfmatrix for the last trading day
        self.annualReturn = self.perfMatrix[-1:]['Annual Return']


