import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output, callback_context
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd


token = mapbox_access_token = 'pk.eyJ1Ijoib2xla3NhbmRyMTcxNyIsImEiOiJja3piZW55eHkwN21vMnZwODloenR0Z2p3In0.NYw3yhwYd6QJfEB23IcgIQ'
df = pd.read_csv('City.csv')


status_bins = [0, 1, 2, 3, 4]
names = ['Normal conditions', 'Non critical error', 'Critical error', 'Lift doesn`t work']
df['status'] = pd.cut(df['Status'], status_bins, labels=names)

fig = px.scatter_mapbox(df, lat='lat', lon='lon',hover_name='status', color='status', zoom=3, height=500)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])


app.layout = dbc.Container([
                 dbc.Row(
                      dbc.Col(
                          html.H1("Superviser",className='text-center'),
                          width=12
                             )
                    ),
                 dbc.Row([
                         html.Div([
                    dbc.Button("Normal conditions", color="success", id='btn-nclicks-1', n_clicks=0),
                    dbc.Button("Non critical error", color="warning", id='btn-nclicks-2', n_clicks=0),
                    dbc.Button("Critical error", color="danger", id='btn-nclicks-3', n_clicks=0),
                    dbc.Button("Lift doesn`t work", color="dark", id='btn-nclicks-4', n_clicks=0)
                                  ])
                         ]),
                 dbc.Row([
                     html.Div(id='container-button-timestamp')]),
                dbc.Row([
                    dcc.Graph(id='map', figure=fig)])

        ])









@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks')
)
def displayClick(btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        msg = 'Button 1 was most recently clicked'
    elif 'btn-nclicks-2' in changed_id:
        msg = 'Button 2 was most recently clicked'
    elif 'btn-nclicks-3' in changed_id:
        msg = 'Button 3 was most recently clicked'
    elif 'btn-nclicks-4' in changed_id:
        msg = 'Button 4 was most recently clicked'
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)