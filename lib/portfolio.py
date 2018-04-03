#!/usr/bin/env python
"""
@author: Vincent Roy [D]

This module implements the base class 

"""


from tinydb import TinyDB
import securities as st
import pandas as pd
import numpy as np



import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Figure, Layout
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


init_notebook_mode(connected=True)



class Portfolio(object):
    """
    This class is the base class 


    Attributes :

        - 

    """

    def __init__(self, portfolioDBFile):

        self.portfolioDBFile = portfolioDBFile

        self.assets = self.loadPortfolio(self.portfolioDBFile)
        self.summary = self.calcSummary()



    def loadPortfolio(self,dbFile):

        db = TinyDB(dbFile)

        assets = []

        for asset in db:

            print 'Creating asset: ' + asset['assetID']

            newAsset = st.CommonStock(asset['assetID'],
                                      asset['purchaseDate'],
                                      asset['purchasePrice'],
                                      asset['saleDate'],
                                      asset['salePrice'],
                                      asset['volume'],
                                      asset['percentOwnership'],
                                      asset['priceFeedRef'])

            newAsset.setAssetData()

            assets.append(newAsset)



        return assets


    def getAssetList(self):
        
        
        assetList = []
        
        for asset in self.assets:
            
            assetList.append(asset.assetID)

        return assetList


    def getGrafParams(self):


        return ['Acquisition', 'Adj Close', 'Market','Est Profit', '% Est Profit']


    def getAssetIdx(self,assetID):

        for idx in range(len(self.assets)):

            if self.assets[idx].assetID == assetID:

                return idx






    def calcSummary(self):

        summary = pd.DataFrame(
            [['Dummy', '00-00-00', np.nan, np.nan,np.nan ,np.nan, np.nan, np.nan, np.nan, np.nan]],
            columns=['Asset ID', 'Purchase date', 'Purchase price', 'Volume','Acquisition', 'Adj Close', 'Market',
                     'Est Profit', '% Est Profit', 'Annual Return'])

        for asset in self.assets:
            summary = pd.concat([summary, asset.perfVector])

        summary = summary[1:]


        # remove date indexes
        summary = pd.DataFrame(summary.values, columns=summary.columns)

        total = pd.DataFrame([['Total', '', '', '', summary['Acquisition'].sum(), '', summary['Market'].sum(), summary['Est Profit'].sum(), '', '']],
                            columns=['Asset ID', 'Purchase date', 'Purchase price', 'Volume', 'Acquisition', 'Adj Close', 'Market',
                                     'Est Profit', '% Est Profit', 'Annual Return'])

        summary = pd.concat([summary, total])


        return summary



            
            


