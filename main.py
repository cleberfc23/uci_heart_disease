from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pages
from app import app

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Graphs", href="/graphs")),
        dbc.NavItem(dbc.NavLink("Form", href="/forms"))
    ],
    brand="UCI Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='content')
])


@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def show_page(pathname):
    if pathname == '/forms':
        return pages.forms.layout
    elif pathname == '/graphs':
        return pages.graphs.layout
    else:
        return pages.home.layout


app.run_server(debug=True)
# app.run_server(debug=False,
#                port=8080,
#                host='0.0.0.0')
