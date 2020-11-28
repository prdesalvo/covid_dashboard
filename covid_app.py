import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


import pandas as pd
import os
import datetime as dt
import numpy as np

import ssl 

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#DataFrames

us_daily_df = pd.read_json('https://api.covidtracking.com/v1/us/daily.json')
us_daily_df['date'] = pd.to_datetime(us_daily_df['date'],format='%Y%m%d')

#calculating dates
dates_days = pd.date_range(start='1/31/2020', end= dt.datetime.now())

yesterday = dates_days[-2]
two_days_ago = dates_days[-3]
one_week_ago = dates_days[-8]

us_daily_df.set_index('date', drop=True, inplace=True)
us_daily_df.sort_index(inplace=True)
us_daily_df_new_per_day = us_daily_df[['positive','hospitalizedCumulative','death']].diff(periods=1)
us_daily_df_new_per_day_rolling = us_daily_df_new_per_day.rolling(window=7).mean()

def change_text(change):
    '''
    This function defines the % change subtext in the top stats part
    '''
    if change > 0:
        return "↑ " + str("{:.0%}".format(change)+' 7-day Trend')
    elif change < 0:
        return "↓ " + str("{:}%".format(change)+' 7-day Trend')
    elif change == 0:
        return "No Change 7-day Trend"
    else:
        pass

def change_color(change):
    '''
    This function defines the % change subtext in the top stats part
    '''
    if change > 0:
        return "red"
    elif change < 0:
        return "green"
    elif change == 0:
        return "grey"
    else:
        pass

fig1 = go.Figure()
fig1.add_trace(go.Bar(x=us_daily_df_new_per_day.index, 
                      y=us_daily_df_new_per_day['positive'], 
                      marker_color='lightblue', 
                      name= 'Positive Cases',
                      hovertemplate = '%{y:,.0f}'
                     ))
fig1.add_trace(go.Scatter(x=us_daily_df_new_per_day_rolling.index, 
                          y=us_daily_df_new_per_day_rolling['positive'], 
                          marker_color='#000080', 
                          name = '7 Day Moving Avg.',
                         hovertemplate ='%{y:,.0f}'))


fig1.update_layout(template='none', height=500, autosize=True,hovermode="x unified", title='New Daily COVID Cases',legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))


#Layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

	dbc.Col(html.H1(children='COVID-19 Dashboard'),width=6),
    #dbc.Col(html.H4(children=dt.datetime.strftime(months[-1],'%B %Y')),width=6),


    #test
    html.Br(),



        dcc.Graph(
        id='example-graph',
        figure=fig1
    )

    ])	



if __name__ == '__main__':
    app.run_server(debug=True)