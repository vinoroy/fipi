# -*- coding: utf-8 -*-

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

import numpy as np
import pandas as pd



def generate_assetMenu(myP):

    menuItems = []

    for asset in myP.getAssetList():
        menuItems.append(dict(label=asset, value=asset))


    return menuItems



# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

myP = Portfolio('/Users/vincentroy/Documents/fipi/data/reg.json')

assetMenuList = generate_assetMenu(myP)







app.layout = html.Div([
                html.H1('FIPI asset manager'),
                html.Br(),
                html.H4('Portfolio performance'),
                html.Div([
                    dcc.Graph(id='portfolio_table')
                    ]),
                html.Br(),
                html.Div([
                    html.Label('Select graf type'),
                    dcc.Dropdown(
                        id='portfolio_graf_type',
                        options=[
                            {'label': 'Acquisition', 'value': 'Acquisition'},
                            {'label': 'Adj Close', 'value': 'Adj Close'},
                            {'label': 'Market', 'value': 'Market'},
                            {'label': 'Est Profit', 'value': 'Est Profit'},
                            {'label': '% Est Profit', 'value': '% Est Profit'}],
                        value='Market'
                        )
                    ],style={'width': '150px'}),
                html.Br(),
                html.Div([
                    dcc.Graph(id='portfolio_graf')
                    ]),
                html.Br(),
                html.Hr(),
                html.H4('Asset analysis'),
                html.Div([
                    html.Div([
                        html.Label('Select asset'),
                        dcc.Dropdown(
                            id='asset_menu',
                            options=assetMenuList,
                            value=assetMenuList[0]['label']
                            )
                    ],style={'width': '150px'}),
                    html.Div([

                        html.Label('Select graf type'),
                        dcc.Dropdown(
                        id='asset_graf_type',
                        options=[
                            {'label': 'Acquisition', 'value': 'Acquisition'},
                            {'label': 'Adj Close', 'value': 'Adj Close'},
                            {'label': 'Market', 'value': 'Market'},
                            {'label': 'Est Profit', 'value': 'Est Profit'},
                            {'label': '% Est Profit', 'value': '% Est Profit'}],
                        value='Market'
                        )
                    ],style={'width': '150px'}),
                ]),
                dcc.Graph(id='asset_graf')
                ])



@app.callback(
    Output(component_id='portfolio_graf', component_property='figure'),
    [Input(component_id='portfolio_graf_type', component_property='value')]
)
def update_portfolio_graf(input_value):

    columnToGraf = input_value

    traces = []

    for asset in myP.assets:
        tempTrace = go.Scatter(
            x=asset.perfMatrix.index,
            y=asset.perfMatrix[columnToGraf],
            mode='lines',
            name=asset.assetID)

        traces.append(tempTrace)


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Asset performance graf'},
            yaxis={'title': 'Aaaa'},
            margin={'l': 200, 'b': 40, 't': 10, 'r': 200},
            hovermode='closest'
        )
    }



@app.callback(
    Output(component_id='asset_graf', component_property='figure'),
    [Input(component_id='asset_menu', component_property='value'),Input(component_id='asset_graf_type', component_property='value')]
)
def update_asset_graf(input_value1,input_value2):

    print 'okok'
    print input_value1
    print input_value2


    assetIdx = myP.getAssetIdx(input_value1)
    grafType = input_value2

    print 'asset index:'
    print assetIdx


    asset = myP.assets[assetIdx]

    trace_high = go.Scatter(
        x=asset.perfMatrix.index,
        y=asset.perfMatrix[grafType],
        name="AAPL High",
        line=dict(color='#17BECF'),
        opacity=0.8)

    trace_low = go.Scatter(
        x=asset.perfMatrix.index,
        y=asset.perfMatrix[grafType],
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



@app.callback(
    Output(component_id='portfolio_table', component_property='figure'),
    [Input(component_id='portfolio_graf_type', component_property='value')]
)
def update_portfolio_table(input_value):


    return ff.create_table(myP.summary)





if __name__ == '__main__':
    app.run_server(debug=True)


