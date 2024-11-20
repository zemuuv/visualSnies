import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px

# Conexión a la base de datos
conn = sqlite3.connect('baseDatos.db', check_same_thread=False)

# Función para obtener y graficar los Inscritos por Sexo y Formación
'''
def grafico_inscritos_por_sexo_y_formacion():
    # Consulta SQL para obtener los datos
    consulta = 
    SELECT
        Dimension_Formacion.Formacion AS FORMACION,
        Dimension_Sexo.Sexo AS SEXO,
        COUNT(Tabla_Inscritos.ID_Inscritos) AS TOTAL
    FROM Tabla_Inscritos
    INNER JOIN  Tabla_Inscritos.ID_Formacion ON Dimension_Formacion= Dimension_Formacion.ID_Formacion
    INNER JOIN  Tabla_Inscritos.ID_Sexo ON Dimension_Sexo = Dimension_Sexo.ID_Sexo
    GROUP BY Dimension_Formacion.Formacion, Dimension_Sexo.Sexo;
    
    
    # Cargar los datos en un DataFrame
    df = pd.read_sql_query(consulta, conn)
    print(df)  # Verifica que los datos están bien cargados
    
    # Crear gráfico de barras agrupadas con Plotly Express
    fig = px.bar(
        df,
        x="FORMACION",
        y="TOTAL",
        color="SEXO",
        barmode="group",
        title="Inscritos por Sexo y Tipo de Formación",
        labels={"TOTAL": "Número de Inscritos", "FORMACION": "Tipo de Formación"}
    )
    return fig

# Función para obtener y graficar los Admitidos por Metodología
def grafico_admitidos_en_metodologia_a_distancia():
    query_admitidos = """
    SELECT M.Tipo_Metodologia, COUNT(A.ID) AS Admitidos
    FROM Tabla_Admitidos A
    JOIN Dimension_Metodologia M ON A.ID_Metodologia = M.ID_Metodologia
    WHERE A.ID_Institucion = 2712
    GROUP BY M.Tipo_Metodologia
    """
    
    # Cargar los datos en un DataFrame
    df_admitidos = pd.read_sql(query_admitidos, conn)
    print(df_admitidos)  # Verifica que los datos están bien cargados
    
    # Crear gráfico de barras con Plotly Express
    fig = px.bar(
        df_admitidos,
        x="Tipo_Metodologia",
        y="Admitidos",
        title="Admitidos por Metodología a Distancia",
        labels={"Admitidos": "Número de Admitidos", "Tipo_Metodologia": "Tipo de Metodología"}
    )
    return fig
'''
# Función para obtener y graficar los Inscritos por Programa Académico
def grafico_inscritos_por_programa():
    query_inscritos = query = """
    SELECT da.Nombre_Programa_Academico, SUM(i.ID_inscritos) AS total_inscritos
    FROM dimension_Institucion di
    JOIN dimension_academico da ON da.id_institucion = di.id_institucion
    JOIN tabla_Inscritos i ON i.id_academica = da.id_academica
    WHERE da.Nombre_Programa_Academico = 'INGENIERÍA DE SISTEMAS'
    GROUP BY da.Nombre_Programa_Academico;
    """
    
    # Cargar los datos en un DataFrame
    df_inscritos = pd.read_sql(query_inscritos, conn)
    print(df_inscritos)  # Verifica que los datos están bien cargados
    
    # Crear gráfico de barras con Plotly Express
    fig = px.bar(df, x='Nombre_Programa_Academico', y='total_inscritos',
                 title='Número de inscritos en el programa de Ingeniería',
                 labels={'total_inscritos': 'Total Inscritos', 'Nombre_Programa_Academico': 'Programa Académico'})
    
    return fig

# Crear la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la app
app.layout = html.Div([
    html.H1("Dashboard SNIES", style={'textAlign': 'center'}),
    html.Hr(),
    
    dbc.Row([
        #dbc.Col([dcc.Graph(id='grafico_inscritos', figure=grafico_inscritos_por_sexo_y_formacion())]),
        #dbc.Col([dcc.Graph(id='grafico_admitidos', figure=grafico_admitidos_en_metodologia_a_distancia())]),
        dbc.Col([dcc.Graph(id='grafico_programa', figure=grafico_inscritos_por_programa())]),
    ])
])

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
