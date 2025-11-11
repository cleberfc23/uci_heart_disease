from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import Dash, dcc, html 

heart_disease = fetch_ucirepo(id=45)
data = heart_disease.data.features

# print(data.head())

figure_histogram = px.histogram(data, 
                      x = 'age', 
                      title = 'Histograma de idades')


data['disease'] = 1*(heart_disease.data.targets > 0)
figure_box_plot = px.box(data, 
                         x = 'disease', 
                         y = 'age',
                         title = 'Box plot age' ,
                         color = 'disease')

div_histogram = html.Div([
        html.H2('Age Histogram'),
        dcc.Graph(figure=figure_histogram)
    ])
div_box_plot = html.Div([
    html.H2('Disease Box plot'),
    dcc.Graph(figure=figure_box_plot)
])

app = Dash(__name__)
app.layout = html.Div([
    html.H1('UCI Repository Heart Disease'),
    div_histogram,  
    div_box_plot])
# app.layout.children.append() --> adicionar de forma dinamica
app.run_server(debug=True)
