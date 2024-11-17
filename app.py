import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px

#Conexion a la base de datos
conn = sqlite3.connect('snies.db', check_same_thread=False)

def programa_dropdown():
    df_programa = pd.read_sql_query("SELECT * FROM PROGRAMA", conn)
    options = [{"label": nombre, "value": id} for id, nombre in zip(df_programa["ID"], df_programa["NOMBRE"])]
    # Agregar una opción adicional para 'Todas'
    options.insert(0, {"label": "Todas", "value": 0})
    return options

def area_dropdown():
    df_area = pd.read_sql_query("SELECT * FROM AREA", conn)
    options = [{"label": nombre, "value": id} for id, nombre in zip(df_area["ID"], df_area["NOMBRE"])]
     # Agregar una opción adicional para 'Todas'
    options.insert(0, {"label": "Todas", "value": 0})
    return options

def grafico_barras(programa=0, area=0):
    if programa == 0 and area == 0:
        consulta = '''
            SELECT
            PROGRAMA.NOMBRE AS PROGRAMA,
            SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
            SUM(SNIES_FACT.MATRICULADOS) AS MATRICULADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa != 0 and area == 0:
        consulta = f'''
            SELECT
            PROGRAMA.NOMBRE AS PROGRAMA,
            SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
            SUM(SNIES_FACT.MATRICULADOS) AS MATRICULADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE PROGRAMA.ID = {programa}
            GROUP BY PROGRAMA.NOMBRE
        '''
    elif programa == 0 and area != 0:
        consulta = f'''
            SELECT
            PROGRAMA.NOMBRE AS PROGRAMA,
            SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
            SUM(SNIES_FACT.MATRICULADOS) AS MATRICULADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE SNIES_FACT.ID_AREA = {area}
            GROUP BY PROGRAMA.NOMBRE
        '''
    else:
        consulta = f'''
            SELECT
            PROGRAMA.NOMBRE AS PROGRAMA,
            SUM(SNIES_FACT.ADMITIDOS) AS ADMITIDOS,
            SUM(SNIES_FACT.MATRICULADOS) AS MATRICULADOS
            FROM SNIES_FACT
            INNER JOIN PROGRAMA ON SNIES_FACT.ID_PROGRAMA = PROGRAMA.ID
            WHERE PROGRAMA.ID = {programa} AND SNIES_FACT.ID_AREA = {area}
            GROUP BY PROGRAMA.NOMBRE
        '''


    df_snies_fact_matriculados = pd.read_sql_query(consulta, conn)

    # Transformar los datos para Plotly
    df_plot = df_snies_fact_matriculados.melt(id_vars=["PROGRAMA"], value_vars=["ADMITIDOS", "MATRICULADOS"],
                                          var_name="Categoría", value_name="Total")

    # Crear el gráfico de barras agrupadas con Plotly Express
    fig = px.bar(
        df_plot, 
        x="PROGRAMA", 
        y="Total", 
        color="Categoría", 
        barmode="group",
        title="Comparación de Admitidos y Matriculados por Programa",
        labels={"Total": "Número de Estudiantes", "PROGRAMA": "Programa"}
    )
    return fig



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Dashboard SNIES"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Label("Programa"),
            dcc.Dropdown(
                            id='programa_dropdown',
                            options=programa_dropdown(),
                            value=0
                        )
            ]),
        dbc.Col([
            html.Label("Area"),
            dcc.Dropdown(
                            id='area_dropdown',
                            options=area_dropdown(),
                            value=0
                        )
            ]),
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico_barras', figure=grafico_barras())
        ])
    ])
])

@app.callback(
    Output(component_id='grafico_barras', component_property='figure'),
    [Input(component_id= 'programa_dropdown', component_property='value'),
    Input(component_id='area_dropdown', component_property='value')]
)
def update_graph(programa, area):
    return grafico_barras(programa, area)


if __name__ == '__main__':
    app.run_server(debug=True)