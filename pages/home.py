# 
from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.A("UCI - Heart Disease", 
           href="https://archive.ics.uci.edu/dataset/45/heart+disease",
           target="_blank", 
           rel="noopener noreferrer")
])

