from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

app = Dash(__name__)
app.layout = html.Div([
    html.Label('Age'),
    dcc.Input(id = 'age_input', type= 'number', value = 0),
    html.Button('Submit', id = 'submit_button', n_clicks=0),
    html.Div(id='output_months')
])

@app.callback(
        output = Output('output_months', 'children'),
        inputs= Input('submit_button', 'n_clicks'),
        state = State('age_input', 'value'),
        prevent_initial_call = True
)


def month_calculate(n_clicks,age):
    if n_clicks == 0 or age ==0:
        return ''
    return age*12

app.run_server(debug = True)