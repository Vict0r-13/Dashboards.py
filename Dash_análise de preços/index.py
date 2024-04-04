# Importar bibliotecas
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Import from folders/theme changer
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# Estilos
tema_template1 = "darkly"
tema_template2 = "zephyr"
url_tema1 = dbc.themes.DARKLY
url_tema2 = dbc.themes.ZEPHYR

# Leitura do dataframe
df = pd.read_csv(r'C:\Users\HP Probook\OneDrive\Área de Trabalho\business intelligence\Dash_análise de preços\data_clean.csv')
estado_selecao = [{"label": x, "value": x} for x in df.ESTADO.unique()]

# Layout
app.layout = dbc.Container(children=[
   # Row 1
   dbc.Row([
        # Col 1
        dbc.Col([
            ThemeSwitchAIO(aio_id="theme", themes=[url_tema1, url_tema2]),
            html.H3('Preço x Estado'),
            dcc.Dropdown(
                id="estados",
                value=[estado['label'] for estado in estado_selecao[:3]],
                multi=True,
                options=estado_selecao,
                style={'color': 'black'}  # Definindo a cor da fonte como preto
            ),
            dcc.Graph(id='line_graph') 
        ], sm=12),
    ]),   
    # Row 2
    dbc.Row([
        # Dropdown 1
        dbc.Col([
            dcc.Dropdown(
                id="estado1",
                value=estado_selecao[0]['label'],
                options=estado_selecao,
                style={'color': 'black'}  # Definindo a cor da fonte como preto
            ),
        ], sm=12 , md=6),
        # Dropdown 2
        dbc.Col([
            dcc.Dropdown(
                id="estado2",
                value=estado_selecao[3]['label'],
                options=estado_selecao,
                style={'color': 'black'}  # Definindo a cor da fonte como preto
            ),
        ], sm=12 , md=6),
        # Col 1
        dbc.Col([
            dcc.Graph(id='indicador1'),
        ], sm=6),
        # Col 2
        dbc.Col([
            dcc.Graph(id='indicador2')
        ], sm=6)
    ])
])

# Callbacks
# Gráfico simples de comparação
@app.callback(
    Output('line_graph', 'figure'),
    Input('estados', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), "value")
)
def animation(estados, toggle):
    template = tema_template1 if toggle else tema_template2

    df_data = df.copy(deep=True)
    mask = df_data['ESTADO'].isin(estados)
    fig = px.line(df_data[mask], x='DATA', y='VALOR REVENDA (R$/L)',
                  color='ESTADO', template=template)
    
    return fig

# Gráficos indicadores 1 e 2
@app.callback(
    Output("indicador1", "figure"),
    Output("indicador2", "figure"),
    Input('estado1', 'value'),
    Input('estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), "value")
)
def card1(estado1, estado2, toggle):
    template = tema_template1 if toggle else tema_template2

    df_data = df.copy(deep=True)
    data_estado1 = df_data[df_data.ESTADO.isin([estado1])]
    data_estado2 = df_data[df_data.ESTADO.isin([estado2])]

    data_inicial = str(int(df_data['ANO'].min()) - 1)
    data_final = df_data['ANO'].max()

    iterable = [(estado1, data_estado1), (estado2, data_estado2)]
    indicadores= []

    for estado, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode= "number+delta",
            title= {"text": f"<span>{estado}</span><br><span style='font-size:0.7em'>{data_inicial} - {data_final}</span>"},
            value= data.at[data.index[-1],'VALOR REVENDA (R$/L)'],
            number = {'prefix': "R$", 'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0],'VALOR REVENDA (R$/L)']}
        ))
        fig.update_layout(template=template)
        indicadores.append(fig)

    return indicadores

# Rodar servidor
if __name__ == '__main__':
    app.run_server(debug=True)
