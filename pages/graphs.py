from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

heart_disease = fetch_ucirepo(id=45)
data = heart_disease.data.features

figure_histogram = px.histogram(data,
                                x='age',
                                title='Age histogram')


data['disease'] = 1*(heart_disease.data.targets > 0)
figure_box_plot = px.box(data,
                         x='disease',
                         y='age',
                         title='Box plot age',
                         color='disease')

div_histogram = html.Div([
    dcc.Graph(figure=figure_histogram)
])
div_box_plot = html.Div([
    dcc.Graph(figure=figure_box_plot)
])

layout = html.Div([
    html.H1('UCI Repository Heart Disease', className= 'text-center mb-5'),
    dbc.Container([
        dbc.Row([
            dbc.Col([div_histogram], md=7),
            dbc.Col([div_box_plot], md =5)
        ])
    ])
])
