from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np


margin_bottom_card_group = 'mb-3'
model = joblib.load('xgboost_model.pkl')
medians = joblib.load('medians.pkl')

app = Dash(__name__,
           external_stylesheets=[dbc.themes.FLATLY])

forms = dbc.Container([
    html.P("Fill the fields below and click on the button to predict",
           className="text-center mb-5"),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label("Age"),
                dbc.Input(id='age', type='number',
                          placeholder='input age'),
            ], class_name='mb-3'),

            dbc.CardGroup(
                [dbc.Label('Gender'),
                 dbc.Select(id='sex',
                            placeholder='select option',
                            options=[
                                        {'label': 'male', 'value': '1'},
                                        {'label': 'female', 'value': '0'}
                            ])], class_name='mb-3'),

            dbc.CardGroup([
                dbc.Label('Chest Pain'),
                dbc.Select(id='cp',
                           placeholder='select option',  # improve option selection
                           options=[
                                       {'label': 'typical angina', 'value': '1'},
                                       {'label': 'atypical angina', 'value': '2'},
                                       {'label': 'non-anginal pain', 'value': '3'},
                                       {'label': 'asymptomatic', 'value': '4'}
                           ])
            ], class_name='mb-3'),

            dbc.CardGroup([
                dbc.Label(
                    'Resting Blood Pressure (in mm Hg on admission to the hospital)'),
                dbc.Input(id='trestbps', type='number',
                          placeholder='input a value')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Serum Cholestoral in mg/dl'),
                dbc.Input(id='chol', type='number',
                          placeholder='Input a value')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Fasting blood sugar > 120 mg/dl'),
                dbc.Select(id='fbs',
                           options=[
                               {'label': '< 120 mg/dl', 'value': '0'},
                               {'label': '> 120 mg/dl ', 'value': '1'}
                           ])
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Resting Electrocardiographic Results'),
                dbc.Select(id='restecg',
                           options=[
                               {'label': 'normal', 'value': '0'},
                               {'label': 'having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)', 'value': '1'},
                               {'label': 'showing probable or definite left ventricular hypertrophy by Estes criteria', 'value': '2'},
                           ])
            ], className='mb-3')
        ]),

        dbc.Col([
            dbc.CardGroup([
                dbc.Label('Maximum Heart Rate Achieved'),
                dbc.Input(id='thalach', type='number',
                          placeholder='Input value')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('Exercise Induced Angina'),
                dbc.Select(id='exang', options=[
                    {'label': 'Yes', 'value': '1'},
                    {'label': 'No', 'value': '0'}
                ], className='mb-3')]),

            dbc.CardGroup([
                dbc.Label(
                    'ST depression induced by exercise relative to rest'),
                dbc.Input(id='oldpeak', type='number',
                          placeholder='input value')
            ], className='mb-3'),

            dbc.CardGroup([
                dbc.Label('The Slope of the Peak exercise ST segment'),
                dbc.Select(id='slope', options=[
                    {'label': 'Upsloping', 'value': '1'},
                    {'label': 'Flat', 'value': '2'},
                    {'label': 'Downsloping', 'value': '3'}
                ], className=margin_bottom_card_group)]),

            dbc.CardGroup([
                dbc.Label(
                    'Number of major vessels (0-3) colored by flourosopy'),
                dbc.Select(id='ca', options=[
                    {'label': '0', 'value': '0'},
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '3', 'value': '3'}
                ], className=margin_bottom_card_group)]),

            dbc.CardGroup([
                dbc.Label('Myocardial Scintigraphy'),
                dbc.Select(id='thal', options=[
                    {'label': 'normal', 'value': '3'},
                    {'label': 'fixed defect', 'value': '6'},
                    {'label': 'reversable defect', 'value': '7'}
                ], className=margin_bottom_card_group)
            ]),

            dbc.Button('Predict', id='predict_button',
                       color='success', n_clicks=0, class_name='mt-4')
        ])
    ])
], fluid=True)


app.layout = html.Div([
    html.H1("Heart Disease Forecast", className="text-center mt-5"),
    forms,
    html.Div(id='prediction_result')
])


@app.callback(
    Output('prediction_result', 'children'),
    [Input('predict_button', 'n_clicks')],
    [State('age', 'value'),
     State('sex', 'value'),
     State('cp', 'value'),
     State('trestbps', 'value'),
     State('chol', 'value'),
     State('fbs', 'value'),
     State('restecg', 'value'),
     State('thalach', 'value'),
     State('exang', 'value'),
     State('oldpeak', 'value'),
     State('slope', 'value'),
     State('ca', 'value'),
     State('thal', 'value')
     ]
)
def predict_disease(n_clicks, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    if n_clicks == 0:
        return ''
    else:
        user_input = pd.DataFrame(
            data=[[age, sex, cp, trestbps, chol, fbs, restecg,
                   thalach, exang, oldpeak, slope, ca, thal]],
            columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                     'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        )

        user_input.fillna(medians, inplace=True)
        user_input['oldpeak'] = user_input['oldpeak'].astype(np.float64)

        for col in user_input.columns:
            if col != 'oldpeak':
                user_input[col] = user_input[col].astype(int)  # !

        prediction = model.predict(user_input)[0]

        if prediction == 1:
            message = "Heart disease has been detected!"
            color_message = 'danger'
        else:
            message = "Healthy"
            color_message = 'light'

        alert = dbc.Alert(message, color = color_message, className='d-flex justify-content-center mb-5')
        return alert

app.run_server(debug=True)
