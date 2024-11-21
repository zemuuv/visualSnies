import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import plotly.express as px

# Conexión a la base de datos
conn = sqlite3.connect('baseDatos.db', check_same_thread=False)

def grafico_inscritos_por_sexo_y_formacion():
  
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

    df = pd.read_sql_query(consulta, conn)
    
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

def grafico_admitidos_en_metodologia_a_distancia():
    query_admitidos = """
    SELECT M.Tipo_Metodologia, COUNT(A.ID) AS Admitidos
    FROM Tabla_Admitidos A
    JOIN Dimension_Metodologia M ON A.ID_Metodologia = M.ID_Metodologia
    WHERE A.ID_Institucion = 2712
    GROUP BY M.Tipo_Metodologia
    """
    
    df_admitidos = pd.read_sql(query_admitidos, conn)
    
    fig = px.bar(
        df_admitidos,
        x="Tipo_Metodologia",
        y="Admitidos",
        title="Admitidos por Metodología a Distancia",
        labels={"Admitidos": "Número de Admitidos", "Tipo_Metodologia": "Tipo de Metodología"}
    )
    return fig

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
    
    df_inscritos = pd.read_sql(query_inscritos, conn)
    
    fig = px.bar(df_inscritos, x='Programa_Academico', y='Total_Inscritos',
                 title='Número de inscritos en el programa de Ingeniería',
                 labels={'total_inscritos': 'Total Inscritos', 'Nombre_Programa_Academico': 'Programa Académico'})
    
    return fig

def generar_grafico_pastel():

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
    
    df = pd.read_sql(query, conn)

    fig = px.pie(df, 
                 names='Programa_Academico', 
                 values='Total_Matriculados', 
                 title="Distribución de matriculados por Programa academico (ingeniería de sistemas, ingeniería industrial)",
                 color='Programa_Academico', 
                 color_discrete_map={'Masculino': 'blue', 'Femenino': 'pink'})
    
    return fig

def grafico_graduados_por_programa():
    query_graduados = '''
    SELECT
        g.ID_Graduado,
        d.Estado_Acreditacion
    FROM
        Tabla_Graduados g
    INNER JOIN
        Dimension_Acreditacion d
    ON
        g.ID_Acreditacion = d.ID_Acreditacion
    WHERE
        d.Estado_Acreditacion = 'No';  -- Filtramos por los graduados no acreditados
    '''
    
    df = pd.read_sql(query_graduados, conn)

    # Verificar las columnas del DataFrame
    print("Columnas del DataFrame:", df.columns)

    if 'ID_graduado' in df.columns:
        graduados_no_acreditados = df['ID_graduado'].count()
    else:
        print("La columna 'ID_graduado' no está presente en el DataFrame.")
        graduados_no_acreditados = 0  # Si no existe, asignar 0 para evitar errores

    graduados_por_programa = pd.DataFrame({
        'Estado_Acreditacion': ['No Acreditado'],
        'Total_Graduados': [graduados_no_acreditados]
    })
    
    fig = px.bar(
        graduados_por_programa,
        x='Estado_Acreditacion',
        y='Total_Graduados',
        title='Número de Graduados con Programa No Acreditados',
        labels={'Estado_Acreditacion': 'Estado de Acreditación', 'Total_Graduados': 'Cantidad de Graduados'},
        color_discrete_sequence=['skyblue']
    )
    
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Dashboard SNIES", style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='grafico_inscritos', figure=grafico_inscritos_por_sexo_y_formacion())]),
        dbc.Col([dcc.Graph(id='grafico_admitidos', figure=grafico_admitidos_en_metodologia_a_distancia())]),
        dbc.Col([dcc.Graph(id='grafico_programa', figure=grafico_inscritos_por_programa())]),
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure=generar_grafico_pastel())])
    ]),

    dbc.Row([
        dbc.Col([dcc.Graph(id='grafico_graduados', figure=grafico_graduados_por_programa())])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
