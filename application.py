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
import json

import ssl 

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	pass
else:
	ssl._create_default_https_context = _create_unverified_https_context


state_populations = pd.DataFrame({'State': {0: 'California', 1: 'Texas', 2: 'Florida', 3: 'New York', 4: 'Illinois', 5: 'Pennsylvania', 6: 'Ohio', 7: 'Georgia', 8: 'North Carolina', 9: 'Michigan', 10: 'New Jersey', 11: 'Virginia', 12: 'Washington', 13: 'Arizona', 14: 'Massachusetts', 15: 'Tennessee', 16: 'Indiana', 17: 'Missouri', 18: 'Maryland', 19: 'Wisconsin', 20: 'Colorado', 21: 'Minnesota', 22: 'South Carolina', 23: 'Alabama', 24: 'Louisiana', 25: 'Kentucky', 26: 'Oregon', 27: 'Oklahoma', 28: 'Connecticut', 29: 'Utah', 30: 'Iowa', 31: 'Nevada', 32: 'Arkansas', 33: 'Mississippi', 34: 'Kansas', 35: 'New Mexico', 36: 'Nebraska', 37: 'West Virginia', 38: 'Idaho', 39: 'Hawaii', 40: 'New Hampshire', 41: 'Maine', 42: 'Montana', 43: 'Rhode Island', 44: 'Delaware', 45: 'South Dakota', 46: 'North Dakota', 47: 'Alaska', 48: 'DC', 49: 'Vermont', 50: 'Wyoming'}, 'July 2019 Estimate': {0: 39512223.0, 1: 28995881.0, 2: 21477737.0, 3: 19453561.0, 4: 12671821.0, 5: 12801989.0, 6: 11689100.0, 7: 10617423.0, 8: 10488084.0, 9: 9986857.0, 10: 8882190.0, 11: 8535519.0, 12: 7614893.0, 13: 7278717.0, 14: 6949503.0, 15: 6833174.0, 16: 6732219.0, 17: 6137428.0, 18: 6045680.0, 19: 5822434.0, 20: 5758736.0, 21: 5639632.0, 22: 5148714.0, 23: 4903185.0, 24: 4648794.0, 25: 4467673.0, 26: 4217737.0, 27: 3956971.0, 28: 3565287.0, 29: 3205958.0, 30: 3155070.0, 31: 3080156.0, 32: 3017825.0, 33: 2976149.0, 34: 2913314.0, 35: 2096829.0, 36: 1934408.0, 37: 1792147.0, 38: 1787065.0, 39: 1415872.0, 40: 1359711.0, 41: 1344212.0, 42: 1068778.0, 43: 1059361.0, 44: 973764.0, 45: 884659.0, 46: 762062.0, 47: 731545.0, 48: 705749.0, 49: 623989.0, 50: 578759.0}})
state_codes = pd.DataFrame({'state_name': {0: 'Alabama', 1: 'Alaska', 2: 'American Samoa', 3: 'Arizona', 4: 'Arkansas', 5: 'California', 6: 'Colorado', 7: 'Connecticut', 8: 'Delaware', 9: 'District Of Columbia', 10: 'Florida', 11: 'Georgia', 12: 'Guam', 13: 'Hawaii', 14: 'Idaho', 15: 'Illinois', 16: 'Indiana', 17: 'Iowa', 18: 'Kansas', 19: 'Kentucky', 20: 'Louisiana', 21: 'Maine', 22: 'Maryland', 23: 'Massachusetts', 24: 'Michigan', 25: 'Minnesota', 26: 'Mississippi', 27: 'Missouri', 28: 'Montana', 29: 'Nebraska', 30: 'Nevada', 31: 'New Hampshire', 32: 'New Jersey', 33: 'New Mexico', 34: 'New York', 35: 'North Carolina', 36: 'North Dakota', 37: 'Northern Mariana Is', 38: 'Ohio', 39: 'Oklahoma', 40: 'Oregon', 41: 'Pennsylvania', 42: 'Puerto Rico', 43: 'Rhode Island', 44: 'South Carolina', 45: 'South Dakota', 46: 'Tennessee', 47: 'Texas', 48: 'Utah', 49: 'Vermont', 50: 'Virginia', 51: 'Virgin Islands', 52: 'Washington', 53: 'West Virginia', 54: 'Wisconsin', 55: 'Wyoming'}, 'abbreviation': {0: 'AL', 1: 'AK', 2: 'AS', 3: 'AZ', 4: 'AR', 5: 'CA', 6: 'CO', 7: 'CT', 8: 'DE', 9: 'DC', 10: 'FL', 11: 'GA', 12: 'GU', 13: 'HI', 14: 'ID', 15: 'IL', 16: 'IN', 17: 'IA', 18: 'KS', 19: 'KY', 20: 'LA', 21: 'ME', 22: 'MD', 23: 'MA', 24: 'MI', 25: 'MN', 26: 'MS', 27: 'MO', 28: 'MT', 29: 'NE', 30: 'NV', 31: 'NH', 32: 'NJ', 33: 'NM', 34: 'NY', 35: 'NC', 36: 'ND', 37: 'MP', 38: 'OH', 39: 'OK', 40: 'OR', 41: 'PA', 42: 'PR', 43: 'RI', 44: 'SC', 45: 'SD', 46: 'TN', 47: 'TX', 48: 'UT', 49: 'VT', 50: 'VA', 51: 'VI', 52: 'WA', 53: 'WV', 54: 'WI', 55: 'WY'}})

available_indicators = sorted(state_populations['State'].unique().tolist())
stat_indicators = ['New Cases','Deaths','Hospitalized']

#Layout
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

application = app.server

def serve_layout():
	return html.Div([

	dbc.Col(html.H1(children='COVID-19 Dashboard'),width=12),
	dbc.Col(html.H5(children=dt.datetime.strftime(dt.datetime.now(),'%B %-d, %Y')),width=12),
	#dbc.Col(html.H4(children=dt.datetime.strftime(months[-1],'%B %Y')),width=6),

	html.Div([
	dbc.Row([
		dbc.Col([
		dbc.Card(
			dbc.CardBody(
				[
					html.H5(id='cases-yesterday', className="card-title"),
					html.P([
							"New  Cases Yesterday", 
							html.Br(),
							html.P(id='cases-trend')],
						className="card-text"
						
					),
				]
			)
		)],lg=4),
		
		dbc.Col([
		dbc.Card(
			dbc.CardBody(
				[
					html.H5(id='deaths-yesterday', className="card-title"),
					html.P([
						"Deaths Yesterday",
						html.Br(),
						html.P(id='deaths-trend')],
						className="card-text",
					),
				]
			)
		)],lg=4),

		dbc.Col([
		dbc.Card(
			dbc.CardBody(
				[
					html.H5(id='hospitalized-yesterday', className="card-title"),
					html.P([
						"Hospitalized Yesterday",
						html.Br(),
						html.P(id='hospitalized-trend')],
						className="card-text",
					),
				]
			)
		)],lg=4)
	]
	, align='center')],className="container-fluid"),

	#test
	html.Br(),

	dbc.Row([
		dbc.Col([
			(html.Div([dcc.Graph(id='example-graph-1')]))
	],lg=6),

		dbc.Col([
			(html.Div([dcc.Graph(id='example-graph-2')]))
	],lg=6),

		dbc.Col([
			(html.Div([dcc.Graph(id='example-graph-3')]))
	],lg=6)
],className='container-fluid'),

		

	dcc.Graph(
		id='example-graph-4',
		
		),
	dcc.Graph(
		id='example-graph-5',
		
		),
	
	#click data
	html.Div([
		dbc.Col(html.H5(children='Click on a State Above to see cases'),width=12),
			#html.H5(id='click-data'),
			html.Div([dcc.Graph(id='indicator-graphic-2')]),
		]),

	#end click data

	dbc.Col(html.H1(children='State Data'),width=12),

		html.Div([
		dbc.Form([
			dbc.Col(
			dbc.FormGroup(
			[
			dcc.Dropdown(
				id='state',
			   options=[{'label': i, 'value': i} for i in available_indicators],
				value='Minnesota'),
			
			]
			),width=4),
			dbc.Col(
			dbc.FormGroup(
				[
				dcc.Dropdown(
					id='indicator',
					options=[{'label': i, 'value': i} for i in stat_indicators],
					value='New Cases')
				]
			),
			width=2)]),]),

	html.Div([dcc.Graph(id='indicator-graphic-1')]),

	dbc.Col(html.P(children='Data as of '+dt.datetime.strftime(dt.datetime.now(),'%B %-d, %Y %H:%M:%S')),width=12),
	dbc.Col(html.P(children='Data from the COVID Tracking Project'),width=12),

	#html.Div(id='intermediate-value-1', style={'display': 'none'}),

	html.P(id='placeholder'),
	html.P(id='placeholder2')

	])  


app.layout = serve_layout

@app.callback(
	dash.dependencies.Output('cases-yesterday', 'children'),
	dash.dependencies.Output('cases-trend', 'children'),

	dash.dependencies.Output('deaths-yesterday', 'children'),
	dash.dependencies.Output('deaths-trend', 'children'),

	dash.dependencies.Output('hospitalized-yesterday', 'children'),
	dash.dependencies.Output('hospitalized-trend', 'children'),

	Output('example-graph-1', 'figure'),
	Output('example-graph-2', 'figure'),
	Output('example-graph-3', 'figure'),
	Output('example-graph-4', 'figure'),

	Input('placeholder', 'id'))

def national_data(placeholder):

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
			return "7-day Trend: ↑ " + str("{:.0%}".format(change))
		elif change < 0:
			return "7-day Trend ↓ " + str("{:.0%}".format(change))
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

	us_cases_yesterday = '{:,}'.format(int(us_daily_df_new_per_day.loc[yesterday]['positive']))
	us_cases_death = '{:,}'.format(int(us_daily_df_new_per_day.loc[yesterday]['death']))
	us_cases_hospitalized = '{:,}'.format(int(us_daily_df_new_per_day.loc[yesterday]['hospitalizedCumulative']))

	us_cases_seven_day_trend = us_daily_df_new_per_day_rolling.loc[yesterday]['positive'] / us_daily_df_new_per_day_rolling.loc[one_week_ago]['positive'] - 1
	cases_trend = change_text(us_cases_seven_day_trend)

	us_death_seven_day_trend = us_daily_df_new_per_day_rolling.loc[yesterday]['death'] / us_daily_df_new_per_day_rolling.loc[one_week_ago]['death'] - 1
	deaths_trend = change_text(us_death_seven_day_trend)

	us_hospitalized_seven_day_trend = us_daily_df_new_per_day_rolling.loc[yesterday]['hospitalizedCumulative'] / us_daily_df_new_per_day_rolling.loc[one_week_ago]['hospitalizedCumulative'] - 1
	hospitalized_trend = change_text(us_hospitalized_seven_day_trend)

	#New Cases
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

	#New Deaths
	fig2 = go.Figure()
	fig2.add_trace(go.Bar(x=us_daily_df_new_per_day.index, 
						  y=us_daily_df_new_per_day['death'], 
						  marker_color='lightblue', 
						  name= 'Deaths',
						 hovertemplate ='%{y:,.0f}'))

	fig2.add_trace(go.Scatter(x=us_daily_df_new_per_day_rolling.index, 
							  y=us_daily_df_new_per_day_rolling['death'], 
							  marker_color='#000080', 
							  name = '7 Day Moving Average',
							 hovertemplate ='%{y:,.0f}'))


	fig2.update_layout(template='none', height=500, autosize=True, hovermode= 'x unified', title='New Daily COVID Deaths',legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
	))

	#New Hospitalizations:
	fig3 = go.Figure()


	fig3.add_trace(go.Bar(x=us_daily_df.index, 
						  y=us_daily_df['hospitalizedCurrently'], 
						  marker_color='lightblue', 
						  name= 'New Daily Deaths',
						 hovertemplate ='%{y:,.0f}'))

	df = us_daily_df[['hospitalizedCurrently']].rolling(window=7).mean()
	fig3.add_trace(go.Scatter(x=df.index, 
							  y=df['hospitalizedCurrently'], 
							  marker_color='#000080', 
							  name = '7 Day Moving Average',
							 hovertemplate ='%{y:,.0f}'))


	fig3.update_layout(template='none', height=500, autosize=True, hovermode= 'x unified', title='Currently Hospitalized',legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
	))

	#Cumulative Cases
	fig10 = go.Figure()

	fig10.add_trace(go.Scatter(x=us_daily_df.index, 
							  y=us_daily_df['positive'], 
							  marker_color='#000080', 
							  name = 'Total Cases',
							 hovertemplate ='%{y:,.0f}'))


	fig10.update_layout(template='none', height=500, autosize=True,hovermode="x unified", title='Cumulative COVID Cases in the US',legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
	))

	return us_cases_yesterday, cases_trend, us_cases_death, deaths_trend, us_cases_hospitalized, hospitalized_trend, fig1,fig2,fig3,fig10

#State Data
@app.callback(
	Output('example-graph-5', 'figure'),
	#Output('intermediate-value-1', 'children'),
	Input('placeholder2', 'id'))

def create_all_the_charts(placeholder):

	#calculating dates
	dates_days = pd.date_range(start='1/31/2020', end= dt.datetime.now())

	yesterday = dates_days[-2]
	two_days_ago = dates_days[-3]
	one_week_ago = dates_days[-8]

	#State Data
	us_states_cases_df = pd.read_json('https://api.covidtracking.com/v1/states/daily.json')
	us_states_cases_df['date'] = pd.to_datetime(us_states_cases_df['date'],format='%Y%m%d')
	us_states_cases_df.sort_values(by='date', ascending=True, inplace=True)
	us_states_cases_df.set_index(['state','date'], drop=True, inplace=True)
	state_list = us_states_cases_df.index.get_level_values(level=0).unique().tolist()

	def new_daily_cases(lst):
		'''
		Since the data is cumluative, this function calculates the daily change
		'''
		
		df_new_cases = pd.DataFrame()
		df_new_cases_rolling = pd.DataFrame()
		
		for i in lst:
			state_df = us_states_cases_df[us_states_cases_df.index.isin([i], level=0)][['positive','hospitalizedCumulative','death']].diff(periods=1)
			df_new_cases = pd.concat([df_new_cases,state_df])
			
			df_rolling = state_df.rolling(window=7).mean()
			df_new_cases_rolling = pd.concat([df_new_cases_rolling,df_rolling])
			
		return df_new_cases, df_new_cases_rolling
		
	us_state_daily_cases, us_state_daily_cases_rolling = new_daily_cases(state_list)
	us_state_and_rolling = pd.merge(us_state_daily_cases, us_state_daily_cases_rolling, how='inner', left_index=True, right_index=True, suffixes = ['_new','_rolling'])	

	us_state_and_rolling.fillna(0, inplace=True)
	us_state_and_rolling[us_state_and_rolling < 0 ] = 0 #This removes negative numbers because I think there are some days with missing data
	us_state_and_rolling_reset = us_state_and_rolling.reset_index()

	us_states_daily_df_codes = pd.merge(us_state_and_rolling_reset,state_codes,how='inner',left_on='state',right_on='abbreviation')
	us_states_daily_df_population = pd.merge(us_states_daily_df_codes,state_populations,how='inner',left_on='state_name',right_on='State')

	us_states_daily_df_population['cases_per_hundred_thousand'] = us_states_daily_df_population['positive_new'] / (us_states_daily_df_population['July 2019 Estimate'] / 100000)

	df = us_states_daily_df_population[us_states_daily_df_population['date'] >= one_week_ago].groupby(['state','state_name']).mean().reset_index()


	df['text'] = df.apply(lambda x: x['state_name'] +'<br>' + 'New Cases Last 7 Days Avg: ' + '{:,.0f}'.format(x['positive_new']) + '<br>' + 'Per 100,000 people: ' + '{:,.0f}'.format(x['cases_per_hundred_thousand']),axis=1)
	#df['state_name'] + '<br>' + 'Last 7 Days Average ' + df['positive_new'].astype('str') + '<br>' + 'Per 100,000 ' + df['cases_per_hundred_thousand'].astype('str')

	fig4 = go.Figure(data=go.Choropleth(
		locations=df['state'],
		z=df['cases_per_hundred_thousand'],
		locationmode='USA-states',
		colorscale='Reds',
		autocolorscale=False,
		text=df['text'], # hover text
		marker_line_color='white', # line markers between states
		colorbar_title="Cases per 100,000 people",
		hoverinfo="text"
	))

	fig4.update_layout(
		title_text='COVID-19 Cases',
		clickmode='event+select',
		geo = dict(
			scope='usa',
			projection=go.layout.geo.Projection(type = 'albers usa'),
			showlakes=True, # lakes
			lakecolor='rgb(255, 255, 255)'),
	)

	return fig4

#Click Data
@app.callback(
	#Output('click-data', 'children'),
	#dash.dependencies.Output('click-data', 'children'),
	Output('indicator-graphic-2', 'figure'),
	Input('example-graph-5', 'clickData'))
	#[dash.dependencies.Input('example-graph-5', 'clickData')],
	#Input('intermediate-value-1', 'children'))

def display_click_data(clickData):
	#clicked_json = json.loads(json.dumps(clickData))

	def clicked_variable(x):
		if x is None:
			return 'MN'  # val exists and is None
		else:
			return x['points'][0]['location']
	
	clicked_state = clicked_variable(clickData)


	single_state_data_api = pd.read_json('https://api.covidtracking.com/v1/states/'+clicked_state+'/daily.json')

	single_state_data_api['date'] = pd.to_datetime(single_state_data_api['date'],format='%Y%m%d')
	single_state_data_api.set_index('date', drop=True, inplace=True)
	single_state_data_api.sort_index(inplace=True)

	single_state_data_api_new_per_day = single_state_data_api[['positive','hospitalizedCumulative','death']].diff(periods=1)
	single_state_data_api_new_per_day.fillna(0)
	single_state_data_api_new_per_day[single_state_data_api_new_per_day < 0 ] = 0

	single_state_data_api_new_per_day_rolling = single_state_data_api_new_per_day.rolling(window=7).mean()
	single_state_data_api_new_per_day_rolling.fillna(0)
	single_state_data_api_new_per_day_rolling[single_state_data_api_new_per_day_rolling < 0 ] = 0

	fig100 = go.Figure()
	fig100.add_trace(go.Bar(x=single_state_data_api_new_per_day.index, 
					  y=single_state_data_api_new_per_day['positive'], 
					  marker_color='lightblue', 
					  name= 'Positive Cases',
					  hovertemplate = '%{y:,.0f}'
					 ))
	fig100.add_trace(go.Scatter(x=single_state_data_api_new_per_day_rolling.index, 
						  y=single_state_data_api_new_per_day_rolling['positive'], 
						  marker_color='#000080', 
						  name = '7 Day Moving Avg.',
						 hovertemplate ='%{y:,.0f}'))


	fig100.update_layout(template='none', height=500, autosize=True,hovermode="x unified", title=clicked_state.upper()+' New Daily COVID Cases',legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
		))
#py.iplot(fig1, filename = 'us_new_daily_covid_cases')

	# if clickData['points'][0]['location'] == None:
	# 	clicked_state = 'MN'
	# else: 
	# 	clicked_state = clickData['points'][0]['location']
	#return json.dumps(clickData)

	# us_states_daily_df_population = pd.read_json(jsonified_cleaned_data1, orient='split')
	# us_states_daily_df_population['date'] = pd.to_datetime(us_states_daily_df_population['date'])
	
	# df_single_state = us_states_daily_df_population[us_states_daily_df_population['abbreviation'] == clicked_state]

	# state_chart_title = 'New Cases '+df_single_state['state_name'].iloc[0]

	# fig6 = go.Figure()


	# fig6.add_trace(go.Bar(x=df_single_state['date'], 
	# 					  y=df_single_state['positive_new'], 
	# 					  marker_color='lightblue', 
	# 					  name= 'New Cases',
	# 					  hovertemplate ='%{y:,.0f}'))

	# fig6.add_trace(go.Scatter(x=df_single_state['date'], 
	# 						  y=df_single_state['positive_rolling'], 
	# 						  marker_color='#000080', 
	# 						  name = '7 Day Moving Avg.',
	# 						  hovertemplate ='%{y:,.0f}'))

	# fig6.update_layout(template='none', height=500, autosize=True, hovermode= 'x unified', title=state_chart_title,legend=dict(
	# 	orientation="h",
	# 	yanchor="bottom",
	# 	y=1.02,
	# 	xanchor="right",
	# 	x=1
	# ))

	return fig100

#original stuff in callback

@app.callback(
	Output('indicator-graphic-1', 'figure'),
	#Input('intermediate-value-1', 'children'),
	Input('state', 'value'),
	Input('indicator', 'value'))

def state_charts(state, indicator):

	dropdown_state = state_codes[state_codes['state_name'] == state]['abbreviation'].iloc[0]

	single_state_data_api = pd.read_json('https://api.covidtracking.com/v1/states/'+dropdown_state+'/daily.json')

	single_state_data_api['date'] = pd.to_datetime(single_state_data_api['date'],format='%Y%m%d')
	single_state_data_api.set_index('date', drop=True, inplace=True)
	single_state_data_api.sort_index(inplace=True)

	single_state_data_api_new_per_day = single_state_data_api[['positive','hospitalizedCumulative','death']].diff(periods=1)
	single_state_data_api_new_per_day.fillna(0)
	single_state_data_api_new_per_day[single_state_data_api_new_per_day < 0 ] = 0

	single_state_data_api_new_per_day_rolling = single_state_data_api_new_per_day.rolling(window=7).mean()
	single_state_data_api_new_per_day_rolling.fillna(0)
	single_state_data_api_new_per_day_rolling[single_state_data_api_new_per_day_rolling < 0 ] = 0

	def y_axis_cat1(x):
		if x == 'New Cases':
			return 'positive'
		elif x == 'Deaths':
			return 'death'
		elif x == 'Hospitalized':
			return 'hospitalizedCumulative'

	fig200 = go.Figure()
	fig200.add_trace(go.Bar(x=single_state_data_api_new_per_day.index, 
					  y=single_state_data_api_new_per_day[y_axis_cat1(indicator)], 
					  marker_color='lightblue', 
					  name= 'Positive Cases',
					  hovertemplate = '%{y:,.0f}'
					 ))
	fig200.add_trace(go.Scatter(x=single_state_data_api_new_per_day_rolling.index, 
						  y=single_state_data_api_new_per_day_rolling[y_axis_cat1(indicator)], 
						  marker_color='#000080', 
						  name = '7 Day Moving Avg.',
						 hovertemplate ='%{y:,.0f}'))

	fig200.update_layout(template='none', height=500, autosize=True,hovermode="x unified", title=state+' New Daily COVID Cases',legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
		))

	return fig200


if __name__ == '__main__':
	application.run(debug=True, port=8080)