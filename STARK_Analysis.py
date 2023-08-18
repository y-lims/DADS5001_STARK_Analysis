import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table

# File Path
data_local_path = 'C:/Users/User/Desktop/New folder/5001_STARK_Analysis/Dataset/STARK_Data.csv'
news_local_path = 'C:/Users/User/Desktop/New folder/5001_STARK_Analysis/Dataset/STARK_News.csv'
data_path = 'https://github.com/y-lims/DADS5001_STARK_Analysis/blob/main/Dataset/STARK_Data.csv'
news_path = 'https://github.com/y-lims/DADS5001_STARK_Analysis/blob/main/Dataset/STARK_News.csv'

# Read file
all_Data = pd.read_csv(data_local_path)
STARK_News = pd.read_csv(news_local_path)

##### STARK DATA #####
# Add columns calculated the fluctuation rate per day for each sector and STARK
all_Data['flucAgro'] = round(((all_Data['hAgro']-all_Data['lAgro'])/all_Data['lAgro'])*100, 2)
all_Data['flucConsump'] = round(((all_Data['hConsump']-all_Data['lConsump'])/all_Data['lConsump'])*100, 2)
all_Data['flucFincial'] = round(((all_Data['hFincial']-all_Data['lFincial'])/all_Data['lFincial'])*100, 2)
all_Data['flucIndus'] = round(((all_Data['hIndus']-all_Data['lIndus'])/all_Data['lIndus'])*100, 2)
all_Data['flucResourc'] = round(((all_Data['hResourc']-all_Data['lResourc'])/all_Data['lResourc'])*100, 2)
all_Data['flucService'] = round(((all_Data['hService']-all_Data['lService'])/all_Data['lService'])*100, 2)
all_Data['flucTech'] = round(((all_Data['hTech']-all_Data['lTech'])/all_Data['lTech'])*100, 2)
all_Data['flucPropcon'] = round(((all_Data['hPropcon']-all_Data['lPropcon'])/all_Data['lPropcon'])*100, 2)
all_Data['flucSTARK'] = round(((all_Data['hSTARK']-all_Data['lSTARK'])/all_Data['lSTARK'])*100, 2)

# Convert file to DataFrame
all_Data = pd.DataFrame(all_Data)
STARK_News = pd.DataFrame(STARK_News)

### ------------------------------------------------------------------- ###

##### STARK Background #####
# Query Data for STARK Analysis
STARK_price = all_Data[['Date', 'pSTARK', 'hSTARK', 'lSTARK', 'flucSTARK', 'vmSTARK']]

# First Date & Last Date
firstDate = STARK_price['Date'].min()
lastestDate = STARK_price['Date'].max()

## STARK Scorecard
minPrice = STARK_price['pSTARK'].min()
maxPrice = STARK_price['pSTARK'].max()
avgPrice = round(STARK_price['pSTARK'].mean(), 2)
avgFluc = round(STARK_price['flucSTARK'].mean(), 2)
avgVol = round(STARK_price['vmSTARK'].mean(), 2)

## Create the STARK Price Historical Data [Line Chart]
# STARK Historical Data
STARK_price['Date'] = pd.to_datetime(STARK_price['Date'])
STARK_News['Date'] = pd.to_datetime(STARK_News['date'])

# Join the STARK_News with STARK_price
merged_data = STARK_price.merge(STARK_News, on='Date', how='left')
merged_data['topic'].fillna('-', inplace=True)
merged_data['description'].fillna('-', inplace=True)

# Line Plot
lineChart = px.line(merged_data, x='Date', y='pSTARK', title='STARK Stock Price Historical Data', hover_data=['topic', 'description'])
lineChart.update_layout(template='simple_white')
lineChart.update_yaxes(type='log', title='Stock Price')
lineChart.update_xaxes(title='Date')

## Create the STARK trading volume [Bar Chart]
barChart = px.bar(STARK_price, x='Date', y='vmSTARK',
                  color_discrete_sequence=['blue'])
barChart.update_layout(template='simple_white')
barChart.update_yaxes(type='log', title='Trading Volume (Million) in Log Scale')
barChart.update_xaxes(title='Date')

## Create the Proportion of STARK News Topic [TreeMap]
# Group 'topic' and count 'Date' for TreeMap
topic_counts = STARK_News.groupby('topic')['Date'].count().reset_index()
topic_counts.rename(columns={'Date': 'Count'}, inplace=True)

# TreeMap plot
treeMap = px.treemap(topic_counts, path=['topic'], values='Count', title='STARK News Topics')

## Create the STARK News Table
columns = ['date', 'topic', 'description']

# Table plot
table_fig = go.Figure(data=[go.Table(
    header=dict(values=columns),
    cells=dict(values=STARK_News[columns].transpose().values.tolist(),
               align='left',
               height=30))
])
table_fig.update_layout(title='STARK News Table')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("STARK Data Analysis", style={'textAlign': 'center'}),
    html.Br(),

    html.Div([
        html.Div(id='firstDate', children=f"First Date: {firstDate}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
        html.Div(id='lastestDate', children=f"Lastest Date: {lastestDate}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gridGap': '30px'}),
    html.Br(),

    html.Div([
        html.Div(id='minPrice', children=f"Min Price: {minPrice}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
        html.Div(id='maxPrice', children=f"Max Price: {maxPrice}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
        html.Div(id='avgPrice', children=f"Avg Price: {avgPrice}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
        html.Div(id='avgFluc', children=f"Avg Fluctuation: {avgFluc}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
        html.Div(id='avgVol', children=f"Avg Volume: {avgVol}",
                 style={'border': '1px solid black', 'textAlign': 'center', 'fontSize': 24}),
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(5, 1fr)', 'gridGap': '10px'}),

    dcc.Graph(id='line-chart', figure=lineChart),
    dcc.Graph(id='bar-chart', figure=barChart),
    dcc.Graph(id='tree-map', figure=treeMap),
    dcc.Graph(id='table-fig', figure=table_fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
### ------------------------------------------------------------------- ###

##### Sectoral Analysis #####
# Sectoral Fluctuation Data
flucSector = all_Data[['Date', 'flucAgro', 'flucConsump', 'flucFincial', 'flucIndus', 'flucPropcon', 'flucResourc', 'flucService', 'flucTech', 'flucSTARK']]

# Rename the columns
flucSector = flucSector.rename(columns={
    'flucAgro': 'AGRO',
    'flucConsump': 'CONSUMP',
    'flucFincial': 'FINCIAL',
    'flucIndus': 'INDUS',
    'flucPropcon': 'PROPCON',
    'flucResourc': 'RESOURC',
    'flucService': 'SERVICE',
    'flucTech': 'TECH',
    'flucSTARK': 'STARK'
})

# Convert 'Date' column to datetime format
flucSector['Date'] = pd.to_datetime(flucSector['Date'])

# Create subplots for comparing fluctuations with STARK
fig = make_subplots(rows=3, cols=3, subplot_titles=flucSector.columns[1:], shared_xaxes=True, vertical_spacing=0.1)

for i, sector in enumerate(flucSector.columns[1:]):
    row = (i // 3) + 1
    col = (i % 3) + 1
    
    sorted_flucSector = flucSector.sort_values(by='Date')
    
    fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector[sector], mode='lines', name=sector), row=row, col=col)
    
    # Set y-axis to log scale
    fig.update_yaxes(type='log', row=row, col=col)

    # Show y-axis only in the first column
    if col == 1:
        fig.update_yaxes(showticklabels=True, row=row, col=col)
    else:
        fig.update_yaxes(showticklabels=False, row=row, col=col)

fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=1, col=1)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=1, col=2)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=1, col=3)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=2, col=1)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=2, col=2)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=2, col=3)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=3, col=1)
fig.add_trace(go.Scatter(x=sorted_flucSector['Date'], y=sorted_flucSector['STARK'], 
                         mode='lines', name='STARK', line=dict(color='rgba(169,169,169,0.5)')), 
                         row=3, col=2)

# Customize x-axis for the last row
for i in range(1, 4):
    fig.update_xaxes(title_text="Date", row=3, col=i)

# Update subplot layout
fig.update_layout(height=800, width=2000, template='simple_white')
fig.update_layout(showlegend=False)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Sectoral Fluctuation Comparison with STARK", style={'textAlign':'center'}),

    dcc.Graph(id='subplot-chart', figure=fig)
    
])

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)