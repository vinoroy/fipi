# -*- coding: utf-8 -*-
"""
@author: Vincent Roy [*]

This module contains the classes and functions for the FiPi web app.

"""

from __future__ import division


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import dash_auth
import plotly.graph_objs as go


import securities as st
from portfolio import *
from ssap import *

import numpy as np
import pandas as pd


def generate_assetMenu():
    """
    This helper method creates the menu items that lists the assets in the portfolio

    Args :
        - None

    Return :
        - (list of dicts) label and value of all the assets in the portfolio


    """

    menuItems = []

    for asset in app.config['PORT'].getAssetList():
        menuItems.append(dict(label=asset, value=asset))

    return menuItems



def loadPortfolio(dbFile):
    """
    This helper method loads a portfolio given the tiny db file that contains the info of the assets int 
    the portfolio. The portfolio object and a list of assets are stored in the app.config variable 

    Args :
        - dbFile (string) 

    Return :
        - None


    """

    # create the portfolio object
    app.config['PORT'] = Portfolio('../data/'+dbFile)

    # create a menu of the assets in the portfolio
    app.config['MENU'] = generate_assetMenu()


# load ssap
ssap = loadSsap()

# authentification section
VALID_USERNAME_PASSWORD_PAIRS = ssap

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)



# load the dash CSS
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# load the screen loading CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

# create a dictionary of the available portfolios
availPortfolios = [{'label': 'regular', 'value': 'reg.json'},
                    {'label': 'fiducie Amelie', 'value': 'fidAmelie.json'},
                    {'label': 'aa', 'value': 'aa'}]



# create a portfolio object for the first portfolio
loadPortfolio('reg.json')


# app layout
app.layout = html.Div([

                # header info of the app
                html.H1('FIPI ASSET MANAGER'),

                # portfolio analysis section
                html.Hr(),
                html.H3('Portfolio analysis'),

                # dropdown menu for the selection of the portfolio
                html.Div([
                html.Br(),
                html.Label('Select a portfolio'),
                dcc.Dropdown(
                    id='portfolio_name_menu',
                    options=[
                        {'label': 'regular', 'value': 'reg.json'},
                        {'label': 'fiducie Amelie', 'value': 'fidAmelie.json'},
                        {'label': 'aa', 'value': 'aa'}],
                    value='reg.json'
                    )
                ],style={'width': '150px'}),
                html.Br(),

                # table of the key performance indicators of the portfolio
                html.Div([
                    dcc.Graph(id='portfolio_table')
                    ]),
                html.Br(),


                # menu for the portfolio performance graf type
                html.Div([
                    html.Label('Select graf type'),
                    dcc.Dropdown(
                        id='portfolio_graf_type',
                        options=[
                            {'label': 'Close', 'value': 'Close'},
                            {'label': 'Adj Close', 'value': 'Adj Close'},
                            {'label': 'Market', 'value': 'Market'},
                            {'label': 'Est Profit', 'value': 'Est Profit'},
                            {'label': '% Est Profit', 'value': '% Est Profit'}],
                        value='Market'
                        )
                    ],style={'width': '150px'}),

                # graf of the portfolio performance based on the selected graf type
                html.Br(),
                html.Div([
                    dcc.Graph(id='portfolio_graf')
                    ]),
                html.Br(),

                # asset analysis section
                html.Hr(),
                html.H3('Asset analysis'),

                # asset and graf type selection menus
                html.Div([
                    html.Div([
                        html.Label('Select asset'),
                        dcc.Dropdown(
                            id='asset_menu',
                            options=app.config['MENU'],
                            value=app.config['MENU'][0]['label']
                            )
                    ],style={'width': '150px'}),
                    html.Div([
                        html.Label('Select graf type'),
                        dcc.Dropdown(
                        id='asset_graf_type',
                        options=[
                            {'label': 'Close', 'value': 'Close'},
                            {'label': 'Adj Close', 'value': 'Adj Close'},
                            {'label': 'Market', 'value': 'Market'},
                            {'label': 'Est Profit', 'value': 'Est Profit'},
                            {'label': '% Est Profit', 'value': '% Est Profit'}],
                        value='Market'
                        )
                    ],style={'width': '150px'}),
                ]),

                # graf of the asset based on the selected asset and the selected graf type
                dcc.Graph(id='asset_graf')
                ])



# portfolio update. This is performed onyl when a new portfolio is selected
@app.callback(
    Output(component_id='asset_menu', component_property='options'),
    [Input(component_id='portfolio_name_menu', component_property='value')]
)
def update_portfolio(input_value):

    # load the selected portfolio
    loadPortfolio(input_value)

    # return to the asset selection menu the new list of assets in the menu form (labal and value)
    return app.config['MENU']


# portfolio graf callback. This is performed if a new portfolio graf type is selected or when a new portfolio is
# selected
@app.callback(
    Output(component_id='portfolio_graf', component_property='figure'),
    [Input(component_id='portfolio_graf_type', component_property='value'),
     Input(component_id='portfolio_name_menu', component_property='value')]
)
def update_portfolio_graf(input_value1,input_value2):

    # get the desired portfolio graf type value
    columnToGraf = input_value1

    # for each asset create a scatter (trace) object based on the selected graf type
    traces = []
    for asset in app.config['PORT'].assets:
        tempTrace = go.Scatter(
            x=asset.perfMatrix.index,
            y=asset.perfMatrix[columnToGraf],
            mode='lines',
            name=asset.assetID)

        traces.append(tempTrace)

    # return the plotly graf object
    return {
        'data': traces,
        'layout': go.Layout(
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
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(count=2,
                             label='2y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                type='date',
                title='Date'
            ),
            #xaxis={'title': 'Date'},
            yaxis={'title': columnToGraf},
            #margin={'l': 20, 'b': 40, 't': 10, 'r': 20},
            hovermode='closest'
        )
    }



# individual asset graf callback. This is called if a new asset is selected, a new asset graf type is selected or the a
# new portfolio is selected
@app.callback(
    Output(component_id='asset_graf', component_property='figure'),
    [Input(component_id='asset_menu', component_property='value'),
     Input(component_id='asset_graf_type', component_property='value'),
     Input(component_id='portfolio_name_menu', component_property='value')]
)
def update_asset_graf(input_value1,input_value2,input_value3):


    # get the asset index from input value 1
    assetIdx = app.config['PORT'].getAssetIdx(input_value1)

    # get the graf type from input value 2
    grafType = input_value2

    # get the asset from the portfolio
    asset = app.config['PORT'].assets[assetIdx]

    # create the trace for the upper and down component of the graf
    trace_high = go.Scatter(
        x=asset.perfMatrix.index,
        y=asset.perfMatrix[grafType],
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_low = go.Scatter(
        x=asset.perfMatrix.index,
        y=asset.perfMatrix[grafType],
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_high, trace_low]

    # layout of the graf
    layout = dict(
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
            type='date',
            title='Date'
        ),
        yaxis = {'title': grafType},
    )

    fig = dict(data=data, layout=layout)

    return fig


# callback for the table. This update is perforemed if a new portfolio is selected
@app.callback(
    Output(component_id='portfolio_table', component_property='figure'),
    [Input(component_id='portfolio_name_menu', component_property='value'),
     Input(component_id='portfolio_graf_type', component_property='value')]
)
def update_portfolio_table(input_value,input2):


    return ff.create_table(app.config['PORT'].summary)



if __name__ == '__main__':
    app.run_server(debug=True)


