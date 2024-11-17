from model import Database
from model import Cargue
import pandas as pd

base_datos = Database('baseDatos.db')
# base_datos.create_table_Departamento()
#base_datos.create_table_acreditacion()
#base_datos.create_table_institucion()
#base_datos.create_table_metodologia()
#base_datos.create_table_programa()
#base_datos.create_table_sexo()
#base_datos.create_table_formacion()
#base_datos.create_table_graduados()
#base_datos.create_table_admitidos()
#base_datos.create_table_inscritos()
#base_datos.create_table_matriculados()

carga = Cargue()
institucion = [2712]

df_admitidos_2023 = carga.cargue_archivo(nombre_archivo='Admitidos2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion)
df_matriculados_2023 = carga.cargue_archivo(nombre_archivo='Matriculados2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion)
df_graduados_2023 = carga.cargue_archivo(nombre_archivo='Graduados2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion)
df_inscritos_2023 = carga.cargue_archivo(nombre_archivo='Inscritos2023.xlsx',hoja=1, encabezado=5, codigo_institucion=institucion)



#Cargue de programas
columnas = ['CÓDIGO DEL DEPARTAMENTO (PROGRAMA)', 'DEPARTAMENTO DE OFERTA DEL PROGRAMA']
base_datos.insert_departamento(df_graduados_2023,columnas)
'''
#Cargue de areas
columnas_area = ['ID ÁREA', 'ÁREA DE CONOCIMIENTO']
base_datos.insert_area(df_admitidos_2023,columnas_area)

#Cargue de SNIES_FACT
columnas_admitidos = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID ÁREA','ID SEXO','AÑO','SEMESTRE','ADMITIDOS']
df_admitidos_2023 = df_admitidos_2023[columnas_admitidos]
columnas_matriculados = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID ÁREA','ID SEXO','AÑO','SEMESTRE','MATRICULADOS']
df_matriculados_2023 = df_matriculados_2023[columnas_matriculados]

columnas_clave = ['CÓDIGO DE LA INSTITUCIÓN','CÓDIGO SNIES DEL PROGRAMA','ID ÁREA','ID SEXO','AÑO','SEMESTRE']

df_fact = pd.merge(df_admitidos_2023, df_matriculados_2023, on=columnas_clave, how='inner')
df_fact['MATRICULADOS'] = df_fact['MATRICULADOS'].astype(int)
df_fact['ADMITIDOS'] = df_fact['ADMITIDOS'].astype(int)
df_fact['ID ÁREA'] = df_fact['ID ÁREA'].astype(int)
df_fact['ID SEXO'] = df_fact['ID SEXO'].astype(int)
df_fact['AÑO'] = df_fact['AÑO'].astype(int)
df_fact['SEMESTRE'] = df_fact['SEMESTRE'].astype(int)
df_fact['CÓDIGO SNIES DEL PROGRAMA'] = df_fact['CÓDIGO SNIES DEL PROGRAMA'].astype(int)
print(df_fact)
base_datos.insert_snies_fact(df=df_fact,columnas=df_fact.columns)
'''