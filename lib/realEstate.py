#!/usr/bin/env python
"""
@author: Vincent Roy 

This module implements the real estate classes

"""



from asset import *


class RealEstate(Asset):
    """
    This class is the abstract real estate class


    Attributes :

        - aaa : (aaa) aaa


    """


    def __init__(self,assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership, ticker):
        Asset.__init__(self, assetID, purchaseDate, purchasePrice, saleDate, salePrice, volume, percentOwnership,ticker)




        self.feedType = 'ARCHIVED'
        self.feedRef = feedRef

        # load the archived values from the assigned csv file
        df = pd.read_csv(self.feedRef, parse_dates=['Date'])
        df = pd.DataFrame(df['Adj Close'].values, index=df['Date'], columns=['Adj Close'])
        self.archivedValues = df




    def getHistoricalValues(self, startDate, endDate):
        """
        Gets the historical stat values (price) from the feed for the asset (close open avg etc.)

        Args :
        - startDate : (string) string representing the start date for the query of the historical asset prices
        - endDate : (string) string representing the end date for the query of the historical asset prices

        Note : if startDate is equal to endDate the method will return the last entry

        Return :
            - (DataFrame) matrix of the historical stat values of the asset

        """

        try:

            # get reference trading days for the specified periode by using the IBM stock and add a new column
            # with NaN
            referenceDates = pdr.DataReader('IBM', data_source='yahoo', start=startDate, end=endDate)
            referenceDates['New'] = np.NaN


            # from the reference dates create a new frame for the historical values
            histValues = pd.DataFrame(referenceDates['New'])


            # append and sort the archived values of the asset
            histValues = histValues.append(self.archivedValues)
            histValues = histValues.sort_index()

            # interpolate the reference dates with the archived values
            histValues = histValues.interpolate()

            # clean up the data frame
            histValues = histValues.drop('New',1)
            histValues = histValues.loc[startDate:endDate]


            return  histValues

        except:

            return None



