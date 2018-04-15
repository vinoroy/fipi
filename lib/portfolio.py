#!/usr/bin/env python
"""
@author: Vincent Roy [D]

This module implements the portfolio class. The class is responsible for holding and mangaging the assets in a given portfolio

"""


from tinydb import TinyDB
import securities as st
import pandas as pd
import numpy as np



class Portfolio(object):
    """
    This class is the portfolio class. The class is responsible for holding and mangaing the assets in a given portfolio
 

    Attributes :

        - portfolioDBFile (string) name of the database file that contains the attributes of the assets in the portfolio
        - assets (Asset) list of assets
        - summary (DataFrame) summary table of the assets in the portfolio

    """

    def __init__(self, portfolioDBFile):

        self.portfolioDBFile = portfolioDBFile
        self.assets = []
        self.summary = []

        self.loadPortfolio()
        self.createSummaryTable()



    def loadPortfolio(self):
        """
        This method loads and creates a portfolio of assets from a database on file 

        Args :
            - None

        Return :
            - None
        """

        # load the db from file
        db = TinyDB(self.portfolioDBFile)


        # for each asset in the db
        for asset in db:

            print 'Creating asset: ' + asset['assetID']

            # create the asset
            newAsset = st.CommonStock(asset['assetID'],
                                      asset['purchaseDate'],
                                      asset['purchasePrice'],
                                      asset['saleDate'],
                                      asset['salePrice'],
                                      asset['volume'],
                                      asset['percentOwnership'],
                                      asset['priceFeedRef'])


            # append the nes asset to the list of assets in the portfolio
            self.assets.append(newAsset)



    def getAssetList(self):
        """
        This method creates a list of the names of the assets in the portfolio 

        Args :
            - None

        Return :
            - (list of strings) lst of the names of the assets in the portfolio
        """

        
        assetList = []

        for asset in self.assets:
            
            assetList.append(asset.assetID)

        return assetList


    def getGrafParams(self):
        """
        This method creates a list of the parameters that can be graphed 

        Args :
            - None

        Return :
            - (list of strings) lst of the names of the parameters that can be graphed 
        """


        return ['Acquisition', 'Adj Close', 'Market','Est Profit', '% Est Profit']



    def getAssetIdx(self,assetID):
        """
        This method gets the index in the portfolio of an asset with a given id
        
        Args :
            - asset id

        Return :
            - (int) index of the asset in the portfolio 
        """

        for idx in range(len(self.assets)):

            if self.assets[idx].assetID == assetID:

                return idx




    def createSummaryTable(self):
        """
        This method creates a summary table of the key attributes of the assets in the portfolio

        Args :
            - None

        Return :
            - None 
        """


        # create an empty dataframe with the column headings (must create a dummy row)
        summary = pd.DataFrame(
            [['Dummy', '00-00-00', np.nan, np.nan,np.nan ,np.nan, np.nan, np.nan, np.nan, np.nan]],
            columns=['Asset ID', 'Purchase date', 'Purchase price', 'Volume','Acquisition', 'Adj Close', 'Market',
                     'Est Profit', '% Est Profit', 'Annual Return'])

        # add the perfprmance vector of each asset to the newly created dataframe
        for asset in self.assets:
            summary = pd.concat([summary, asset.perfVector])

        # remove the dummy row
        summary = summary[1:]


        # remove date indexes
        summary = pd.DataFrame(summary.values, columns=summary.columns)

        # create a dataframe with the sum of some of the performace indicators
        total = pd.DataFrame([['Total', '', '', '', summary['Acquisition'].sum(), '', summary['Market'].sum(), summary['Est Profit'].sum(), '', '']],
                            columns=['Asset ID', 'Purchase date', 'Purchase price', 'Volume', 'Acquisition', 'Adj Close', 'Market',
                                     'Est Profit', '% Est Profit', 'Annual Return'])

        # add the sum dataframe to the summary table
        summary = pd.concat([summary, total])


        self.summary = summary



            
            


