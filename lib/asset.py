#!/usr/bin/env python
"""
@author: Vincent Roy [D]

This module implements the base class asset that is the superclass of all financial assets

"""


from __future__ import division


import numpy as np
import pandas as pd
import datetime


import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure, Layout
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


init_notebook_mode(connected=True)






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





    #-------------------------------------------------------------------------------------------------------------------
    #
    # Asset performance calculations methods
    #
    #-------------------------------------------------------------------------------------------------------------------


    def calcAcquistionValue(self):
        """
        Calculates the acquisition value based on the purchase price of the asset and the volume

        Return :
            - (float) acquisition value of the asset
        """

        return self.purchasePrice * self.volume


    def getLastPrice(self):
        """
        Gets the last price of the asset on the last trading day. 

        Args :
        - none

        Return :
        - (list) date and value
        
        """

        pass



    def getHistoricalPrice(self,startDate,endDate):
        """
        Gets the historical price at a given date for a unit of the asset. 

        Args :
        - startDate : (string) start date of the extraction (format YY-MM-DD)
        - endDate : (string) end date of the extraction (format YY-MM-DD)

        Return :
            - (Dataframe) 
        """

        raise NotImplementedError("Should have implemented this")



    def calcAssetPerformanceMatrix(self,startDate,endDate):
        """
        Calculates the asset performance matrix composed of the key performance indicators for each of the trading dates
        between the selected start and end dates :
            - Open, High, Low, Close and volume
            - Market value of the asset
            - Estimated profit of the asset
            - % Estimated profit of the asset
        
        Args :
        - startDate : (string) start date of the extraction (format YY-MM-DD)
        - endDate : (string) end date of the extraction (format YY-MM-DD)


        Return :
            - (float) 
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


        perfMat['Time Delta'] = (perfMat.index.values - perfMat.index.values[0]) / np.timedelta64(1, 'D') / 365
        perfMat['% Return'] = perfMat['Adj Close'] / perfMat[0:]['Adj Close'].values[0]
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
            - Open, High, Low, Close and volume
            - Market value of the asset
            - Estimated profit of the asset
            - % Estimated profit of the asset

    
        Return :
            - (DataFrame) matrix of the key performance indicators for the last trading day
        """



        perfVector = self.perfMatrix.iloc[[-1]]

        perfVector = perfVector[['Adj Close', 'Market', 'Est Profit', '% Est Profit','Annual Return']]

        perfVector['Asset ID'] = self.assetID
        perfVector['Purchase date'] = self.purchaseDate
        perfVector['Purchase price'] = self.purchasePrice
        perfVector['Volume'] = self.volume
        perfVector['Acquisition'] = self.volume * self.purchasePrice


        perfVector = perfVector[['Asset ID','Purchase date','Purchase price','Volume','Acquisition','Adj Close', 'Market',
                                 'Est Profit', '% Est Profit', 'Annual Return']]



        return perfVector


    #------------- Sale performance ---------------------------------------------------------------------------------


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


        if self.saleDate != None:

            endDate = self.saleDate

        else:

            endDate = datetime.datetime.now().strftime("%Y-%m-%d")


        self.perfMatrix = self.calcAssetPerformanceMatrix(self.purchaseDate,endDate)

        self.annualReturn = self.perfMatrix[-1:]['Annual Return']

        self.perfVector = self.calcCurrentPerformanceVector()





    #------------- Grafing ---------------------------------------------------------------------------------



    def grafAsset(self,grafType='Adj Close'):

        trace_high = go.Scatter(
            x=self.perfMatrix.index,
            y=self.perfMatrix[grafType],
            name="AAPL High",
            line=dict(color='#17BECF'),
            opacity=0.8)

        trace_low = go.Scatter(
            x=self.perfMatrix.index,
            y=self.perfMatrix[grafType],
            name="AAPL Low",
            line=dict(color='#7F7F7F'),
            opacity=0.8)

        data = [trace_high, trace_low]

        layout = dict(
            title='Time Series with Rangeslider',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
        )

        fig = dict(data=data, layout=layout)
        iplot(fig, filename="Time Series with Rangeslider")



    def getGrafTraces(self,grafType='Adj Close'):

        trace_high = go.Scatter(
            x=self.perfMatrix.index,
            y=self.perfMatrix[grafType],
            name="AAPL High",
            line=dict(color='#17BECF'),
            opacity=0.8)

        trace_low = go.Scatter(
            x=self.perfMatrix.index,
            y=self.perfMatrix[grafType],
            name="AAPL Low",
            line=dict(color='#7F7F7F'),
            opacity=0.8)

        data = [trace_high, trace_low]

        layout = dict(
            title='Time Series with Rangeslider',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
        )

        fig = dict(data=data, layout=layout)


        return fig
