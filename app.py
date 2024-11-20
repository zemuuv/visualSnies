import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px

# Conexión a la base de datos
conn = sqlite3.connect('baseDatos.db', check_same_thread=False)

# Función para obtener y graficar los Inscritos por Sexo y Formación

def grafico_inscritos_por_sexo_y_formacion():
    # Consulta SQL para obtener los datos
    consulta = '''
    SELECT 
    ds.Sexo, 
    df.Formacion, 
    SUM(ti.ID_Inscritos) AS Total_Inscritos
    FROM 
    Tabla_Inscritos ti
    INNER JOIN 
    Dimension_Sexo ds ON ti.ID_Sexo = ds.ID_Sexo
    INNER JOIN 
    Dimension_Formacion df ON ti.ID_Formacion = df.ID_Formacion
    GROUP BY 
    ds.Sexo, df.Formacion;
    '''
    
    # Cargar los datos en un DataFrame
    df = pd.read_sql_query(consulta, conn)
    
    # Crear gráfico de barras agrupadas con Plotly Express
    fig = px.bar(
        df,
        x="Formacion",
        y="Total_Inscritos",
        color="Sexo",
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
    
    # Crear gráfico de barras con Plotly Express
    fig = px.bar(
        df_admitidos,
        x="Tipo_Metodologia",
        y="Admitidos",
        title="Admitidos por Metodología a Distancia",
        labels={"Admitidos": "Número de Admitidos", "Tipo_Metodologia": "Tipo de Metodología"}
    )
    return fig

# Función para obtener y graficar los Inscritos por Programa Académico
def grafico_inscritos_por_programa():
    query_inscritos = query = """
    SELECT 
    dpa.Nombre_Programa_Academico AS Programa_Academico,
    SUM(ti.ID_Inscritos) AS Total_Inscritos
    FROM 
    Tabla_Inscritos ti
    JOIN 
    Dimension_Programa_Academico dpa ON ti.ID_Programa_Academico = dpa.ID_Programa_Academico
    WHERE 
    dpa.Nombre_Programa_Academico IN ('INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL','MATEMATICAS')
    GROUP BY 
    dpa.Nombre_Programa_Academico;
    """
    
    # Cargar los datos en un DataFrame
    df_inscritos = pd.read_sql(query_inscritos, conn)
    
    # Crear gráfico de barras con Plotly Express
    fig = px.bar(df_inscritos, x='Programa_Academico', y='Total_Inscritos',
                 title='Número de inscritos en el programa de Ingeniería',
                 labels={'total_inscritos': 'Total Inscritos', 'Nombre_Programa_Academico': 'Programa Académico'})
    
    return fig

def generar_grafico_pastel():
    # Consulta SQL para obtener los datos
    query = """
    SELECT 
    dpa.Nombre_Programa_Academico AS Programa_Academico,
    SUM(tm.ID_Matriculados) AS Total_Matriculados
    FROM 
    Tabla_Matriculados tm
    INNER JOIN 
    Dimension_Programa_Academico dpa ON tm.ID_Programa_Academico = dpa.ID_Programa_Academico
    WHERE 
    dpa.Nombre_Programa_Academico IN ('INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL')
    GROUP BY 
    dpa.Nombre_Programa_Academico
    """
    
    # Ejecutar la consulta SQL y cargar los datos en un DataFrame
    df = pd.read_sql(query, conn)

    # Crear el gráfico de pastel usando Plotly Express
    fig = px.pie(df, 
                 names='Programa_Academico', 
                 values='Total_Matriculados', 
                 title="Distribución de matriculados por Programa academico (ingeniería de sistemas, ingeniería industrial)",
                 color='Programa_Academico', 
                 color_discrete_map={'Masculino': 'blue', 'Femenino': 'pink'})
    
    return fig

# Crear la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la app
app.layout = html.Div([
    html.H1("Dashboard SNIES", style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='grafico_inscritos', figure=grafico_inscritos_por_sexo_y_formacion())]),
        dbc.Col([dcc.Graph(id='grafico_admitidos', figure=grafico_admitidos_en_metodologia_a_distancia())]),
        dbc.Col([dcc.Graph(id='grafico_programa', figure=grafico_inscritos_por_programa())]),
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure=generar_grafico_pastel())]),
        #dbc.Col([dcc.Graph(id='grafico_admitidos', figure=grafico_admitidos_en_metodologia_a_distancia())]),
        #dbc.Col([dcc.Graph(id='grafico_programa', figure=grafico_inscritos_por_programa())]),
    ])
])

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
