from model import Database
from model import Cargue
import pandas as pd

base_datos = Database('baseDatos.db')

#base_datos.create_table_Departamento()
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




#Cargue de departamentos
columnas = ['CÓDIGO DEL DEPARTAMENTO (PROGRAMA)', 'DEPARTAMENTO DE OFERTA DEL PROGRAMA']
base_datos.insert_departamento(df_graduados_2023,columnas)

#Cargue de acreditacion
columnas_acreditacion = ['CÓDIGO SNIES DEL PROGRAMA', 'PROGRAMA ACREDITADO']
base_datos.insert_acreditacion(df_graduados_2023,columnas_acreditacion)

#Cargue de institucion
columnas_acreditacion = ['CÓDIGO DE LA INSTITUCIÓN', 'INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)']
base_datos.insert_institucion(df_graduados_2023,columnas_acreditacion)

#Cargue de metodologia
columnas_acreditacion = ['ID MODALIDAD', 'MODALIDAD']
base_datos.insert_metodologia(df_admitidos_2023,columnas_acreditacion)

#Cargue de Programa_academico
columnas_acreditacion = ['CÓDIGO SNIES DEL PROGRAMA', 'PROGRAMA ACADÉMICO']
base_datos.insert_programa_academico(df_matriculados_2023,columnas_acreditacion)

#Cargue de sexo
columnas_acreditacion = ['ID SEXO', 'SEXO']
base_datos.insert_sexo(df_graduados_2023,columnas_acreditacion)

#Cargue de formacion
columnas_acreditacion = ['ID NIVEL DE FORMACIÓN', 'NIVEL DE FORMACIÓN']
base_datos.insert_formacion(df_graduados_2023,columnas_acreditacion)

##################################################################################################################################

# Filtrar el DataFrame para que solo contenga las columnas necesarias de admitidos
columnas_admitidos = ['CÓDIGO DE LA INSTITUCIÓN', 'ID MODALIDAD', 'ADMITIDOS', 'AÑO']

# Seleccionar solo las columnas que te interesan del DataFrame de admitidos
df_admitidos_2023 = df_admitidos_2023[columnas_admitidos]

# Asegurarse de que las columnas tienen los tipos de datos correctos
df_admitidos_2023['ADMITIDOS'] = df_admitidos_2023['ADMITIDOS'].astype(int)
df_admitidos_2023['ID MODALIDAD'] = df_admitidos_2023['ID MODALIDAD'].astype(int)
df_admitidos_2023['CÓDIGO DE LA INSTITUCIÓN'] = df_admitidos_2023['CÓDIGO DE LA INSTITUCIÓN'].astype(int)
df_admitidos_2023['AÑO'] = df_admitidos_2023['AÑO'].astype(int)

# Renombrar las columnas para que coincidan con los nombres que deseas insertar
df_admitidos_2023.rename(columns={
    'CÓDIGO DE LA INSTITUCIÓN': 'ID_INSTITUCION',
    'ID MODALIDAD': 'ID_MODALIDAD',
    'ADMITIDOS': 'ADMITIDOS',
    'AÑO': 'ANIO'
}, inplace=True)

# Mostrar el DataFrame para verificar
print(df_admitidos_2023)
# Llamar a la función para insertar el DataFrame de admitidos
base_datos.insert_snies_fact(df=df_admitidos_2023, columnas=df_admitidos_2023.columns)

#############################################################################################################################

# Filtrar el DataFrame para que contenga las columnas necesarias
columnas_graduados = ['GRADUADOS', 'CÓDIGO DE LA INSTITUCIÓN', 'CÓDIGO DEL DEPARTAMENTO (PROGRAMA)', 'CÓDIGO SNIES DEL PROGRAMA', 'AÑO']

# Seleccionar las columnas necesarias del DataFrame
df_graduados_2023 = df_graduados_2023[columnas_graduados]

# Asegurarse de que las columnas tienen los tipos de datos correctos
df_graduados_2023['GRADUADOS'] = df_graduados_2023['GRADUADOS'].astype(int)
df_graduados_2023['CÓDIGO DE LA INSTITUCIÓN'] = df_graduados_2023['CÓDIGO DE LA INSTITUCIÓN'].astype(int)
df_graduados_2023['CÓDIGO DEL DEPARTAMENTO (PROGRAMA)'] = df_graduados_2023['CÓDIGO DEL DEPARTAMENTO (PROGRAMA)'].astype(int)
df_graduados_2023['CÓDIGO SNIES DEL PROGRAMA'] = df_graduados_2023['CÓDIGO SNIES DEL PROGRAMA'].astype(int)
df_graduados_2023['AÑO'] = df_graduados_2023['AÑO'].astype(int)


# Renombrar las columnas para que coincidan con los nombres que deseas insertar
df_graduados_2023.rename(columns={
    'GRADUADOS': 'ID_GRADUADO',
    'AÑO': 'FECHA_GRADUACION',
    'CÓDIGO DE LA INSTITUCIÓN': 'ID_INSTITUCION',
    'CÓDIGO DEL DEPARTAMENTO (PROGRAMA)': 'ID_DEPARTAMENTO',
    'CÓDIGO SNIES DEL PROGRAMA': 'ID_ACREDITACION'
}, inplace=True)

# Mostrar el DataFrame para verificar
print(df_graduados_2023)
# Llamar a la función para insertar el DataFrame de graduados
base_datos.insert_graduados_fact(df=df_graduados_2023, columnas=df_graduados_2023.columns)

############################################################################################################################

# Filtrar el DataFrame para que contenga las columnas necesarias de inscritos
columnas_inscritos = ['INSCRITOS', 'ID SEXO', 'ID NIVEL DE FORMACIÓN', 'CÓDIGO SNIES DEL PROGRAMA', 'AÑO']

# Seleccionar solo las columnas necesarias del DataFrame
df_inscritos_2023 = df_inscritos_2023[columnas_inscritos]

# Asegurarse de que las columnas tengan los tipos de datos correctos
df_inscritos_2023['INSCRITOS'] = df_inscritos_2023['INSCRITOS'].astype(int)
df_inscritos_2023['ID SEXO'] = df_inscritos_2023['ID SEXO'].astype(int)
df_inscritos_2023['ID NIVEL DE FORMACIÓN'] = df_inscritos_2023['ID NIVEL DE FORMACIÓN'].astype(int)
df_inscritos_2023['CÓDIGO SNIES DEL PROGRAMA'] = df_inscritos_2023['CÓDIGO SNIES DEL PROGRAMA'].astype(int)
df_inscritos_2023['AÑO'] = df_inscritos_2023['AÑO'].astype(int)

# Renombrar las columnas para que coincidan con los nombres que deseas insertar
df_inscritos_2023.rename(columns={
    'INSCRITOS': 'ID_INSCRITOS',
    'AÑO': 'FECHA_INSCRIPCION',
    'ID SEXO': 'ID_SEXO',
    'ID NIVEL DE FORMACIÓNn': 'ID_FORMACION',
    'CÓDIGO SNIES DEL PROGRAMA': 'ID_PROGRAMA_ACADEMICO'
}, inplace=True)

# Mostrar el DataFrame para verificar
print(df_inscritos_2023)

# Llamar a la función para insertar el DataFrame de inscritos
base_datos.insert_inscritos_fact(df=df_inscritos_2023, columnas=df_inscritos_2023.columns)

#########################################################################################################################

# Filtrar el DataFrame para que contenga las columnas necesarias de matriculados
columnas_matriculados = ['MATRICULADOS', 'CÓDIGO SNIES DEL PROGRAMA', 'CÓDIGO DE LA INSTITUCIÓN', 'AÑO']

# Seleccionar solo las columnas necesarias del DataFrame
df_matriculados_2023 = df_matriculados_2023[columnas_matriculados]

# Asegurarse de que las columnas tengan los tipos de datos correctos
df_matriculados_2023['MATRICULADOS'] = df_matriculados_2023['MATRICULADOS'].astype(int)
df_matriculados_2023['CÓDIGO SNIES DEL PROGRAMA'] = df_matriculados_2023['CÓDIGO SNIES DEL PROGRAMA'].astype(int)
df_matriculados_2023['CÓDIGO DE LA INSTITUCIÓN'] = df_matriculados_2023['CÓDIGO DE LA INSTITUCIÓN'].astype(int)
df_matriculados_2023['AÑO'] = df_matriculados_2023['AÑO'].astype(int)

# Renombrar las columnas para que coincidan con los nombres que deseas insertar
df_matriculados_2023.rename(columns={
    'MATRICULADOS': 'ID_MATRICULADOS',
    'CÓDIGO SNIES DEL PROGRAMA': 'ID_PROGRAMA_ACADEMICO',
    'CÓDIGO DE LA INSTITUCIÓN': 'ID_INSTITUCION',
    'AÑO': 'ID_ANIO'
}, inplace=True)

# Mostrar el DataFrame para verificar
print(df_matriculados_2023)

# Llamar a la función para insertar el DataFrame de matriculados
base_datos.insert_matriculados_fact(df=df_matriculados_2023, columnas=df_matriculados_2023.columns)


