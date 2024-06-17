import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as pltgo
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

df = pd.read_csv('dataset.csv')
print(df.head())

tab_card = { 'heigth': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "xanchor": "left",
        "y": 0.9,
        "x": 0.1,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0, 0, 0, 0.5)"
    },
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"dispplayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

df_copy = df.copy()


df.loc [ df["Mês"] == 'Jan', 'Mês'] = 1
df.loc [ df["Mês"] == 'Fev', 'Mês'] = 2
df.loc [ df["Mês"] == 'Mar', 'Mês'] = 3
df.loc [ df["Mês"] == 'Abr', 'Mês'] = 4
df.loc [ df["Mês"] == 'Mai', 'Mês'] = 5
df.loc [ df["Mês"] == 'Jun', 'Mês'] = 6
df.loc [ df["Mês"] == 'Jul', 'Mês'] = 7
df.loc [ df["Mês"] == 'Ago', 'Mês'] = 8
df.loc [ df["Mês"] == 'Set', 'Mês'] = 9
df.loc [ df["Mês"] == 'Out', 'Mês'] = 10
df.loc [ df["Mês"] == 'Nov', 'Mês'] = 11
df.loc [ df["Mês"] == 'Dez', 'Mês'] = 12

df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
df.loc[df['Status de Pagamento'] == 'Pago', "Status de Pagamento"] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0
df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)
df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)
df['Valor Pago'] = df['Valor Pago'].astype(int)
print(df.head(25))

options_month = [{'label': 'Ano todo', 'value': 0}]



for i, j in zip(df_copy['Mês'].unique(), df['Mês'].unique()):
    options_month.append({'label': i, 'value': j})

options_month = sorted(options_month, key=lambda x: x['value'])

options_team = [{'label': 'Todas Equipes', 'value': i}]

for i in df['Equipe'].unique():
    options_team.append({'label': 'Todas Equipes', 'value': 0})

def month_filter(month):
    if month == 0:
        mask = df['Mês'].isin(df['Mês'].unique())
    else:
        mask=df['Mês'].isin([month])

    return mask

def team_filter(team):
    if team == 0:
        mask=df['Equipe'].isin(df['Equipe'].unique())
    else:
        mask = df['Equipe'].isin([team])

    return mask


def convert_to_txt(month):
    match month:
        case 0:
            x = 'Ano Todo'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x

print(df.head(25))


#Layout

app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    # dcc.Store(id='dataset', data=df_store),

    # Layout
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Vinícius Corrêa Dev")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="#")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Top Consultores por Equipe')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'},
                                     className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph7', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph8', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Valores de Propaganda convertidos por mês"),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Equipe'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})

if __name__ == '__main__':
    app.run_server(debug=False)





