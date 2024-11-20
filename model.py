import sqlite3
import pandas as pd


class Database:
    def __init__(self, nombre_base_datos):
        self.conn = sqlite3.connect(nombre_base_datos)
        self.cursor = self.conn.cursor()

    def create_table_Departamento(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Departamento (
            ID_Departamento INT PRIMARY KEY,
            Nombre_Departamento VARCHAR(100)
            )
                            ''')
        self.conn.commit()
    
    def create_table_acreditacion(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Acreditacion (
            ID_Acreditacion INT PRIMARY KEY ,
            Estado_Acreditacion VARCHAR(50)
            )
                            ''')
        self.conn.commit()

    def create_table_institucion(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Institucion (
            ID_Institucion INT PRIMARY KEY ,
            Nombre_Institucion VARCHAR(100)
            )

                            ''')
        self.conn.commit()

    def create_table_metodologia(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Metodologia (
            ID_Metodologia INT PRIMARY KEY ,
            Tipo_Metodologia VARCHAR(50)
            )
                            ''')
        self.conn.commit()

    def create_table_programa(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Programa_Academico (
            ID_Programa_Academico INT PRIMARY KEY ,
            Nombre_Programa_Academico VARCHAR(100)
            )
                            ''')
        self.conn.commit()
    
    def create_table_sexo(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Sexo (
            ID_Sexo INT PRIMARY KEY ,
            Sexo VARCHAR(10)
            )
                            ''')
        self.conn.commit()

    def create_table_formacion(self):
        self.cursor.execute('''
            CREATE TABLE Dimension_Formacion (
            ID_Formacion INT PRIMARY KEY ,
            Formacion VARCHAR(50)
            )
                            ''')
        self.conn.commit()

    def create_table_graduados(self):
        self.cursor.execute('''
            CREATE TABLE Tabla_Graduados (
            ID INTEGER PRIMARY KEY,
            ID_graduado INTEGER ,
            Fecha_Graduacion DATE,
            ID_Institucion INT,
            ID_Departamento INT,
            ID_Acreditacion INT,
            FOREIGN KEY (ID_Institucion) REFERENCES Dimension_Institucion(ID_Institucion),
            FOREIGN KEY (ID_Departamento) REFERENCES Dimension_Departamento(ID_Departamento),
            FOREIGN KEY (ID_Acreditacion) REFERENCES Dimension_Acreditacion(ID_Acreditacion)
            )
                            ''')
        self.conn.commit()
    
    def create_table_admitidos(self):
        self.cursor.execute('''
            CREATE TABLE Tabla_Admitidos (
            ID INTEGER PRIMARY KEY ,
            ID_ADMITIDOS INTEGER,
            Fecha_Admitidos DATE,
            ID_Institucion INT,
            ID_Metodologia INT,
            FOREIGN KEY (ID_Institucion) REFERENCES Dimension_Institucion(ID_Institucion),
            FOREIGN KEY (ID_Metodologia) REFERENCES Dimension_Metodologia(ID_Metodologia)
            )
                            ''')
        self.conn.commit()

    def create_table_inscritos(self):
        self.cursor.execute('''
            CREATE TABLE Tabla_Inscritos (
            ID INTEGER PRIMARY KEY,
            ID_Inscritos INT,
            Fecha_Inscripcion DATE,
            ID_Sexo INT,
            ID_Formacion INT,
            ID_Programa_Academico INT,
            FOREIGN KEY (ID_Sexo) REFERENCES Dimension_Sexo(ID_Sexo),
            FOREIGN KEY (ID_Formacion) REFERENCES Dimension_Formacion(ID_Formacion),
            FOREIGN KEY (ID_Programa_Academico) REFERENCES
            Dimension_Programa_Academico(ID_Programa_Academico)
            )
                            ''')
        self.conn.commit()

    def create_table_matriculados(self):
        self.cursor.execute('''
            CREATE TABLE Tabla_Matriculados (
            ID INTEGER PRIMARY KEY,
            ID_Matriculados INT ,
            ID_Programa_Academico INT,
            ID_Institucion INT,
            ID_Año INT,
            FOREIGN KEY (ID_Programa_Academico) REFERENCES
            Dimension_Programa_Academico(ID_Programa_Academico),
            FOREIGN KEY (ID_Institucion) REFERENCES Dimension_Institucion(ID_Institucion)
            )
                            ''')
        self.conn.commit()
   
    def insert_departamento(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Departamento', columnas[1]: 'Nombre_Departamento'}, inplace=True)   
        df.to_sql('Dimension_Departamento', self.conn, if_exists='append', index=False)  
        self.conn.commit()

    def insert_acreditacion(self, df, columna_estado):
        df = df[columna_estado].drop_duplicates()
        df[columna_estado[0]] = pd.to_numeric(df[columna_estado[0]], errors='coerce').fillna(0).astype(int)
        df.rename(columns={columna_estado[0]: 'ID_Acreditacion', columna_estado[1]: 'Estado_Acreditacion'}, inplace=True)   
        df.to_sql('Dimension_Acreditacion', self.conn, if_exists='append', index=False)
        self.conn.commit()

    def insert_institucion(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Institucion', columnas[1]: 'Nombre_Institucion'}, inplace=True)   
        df.to_sql('Dimension_Institucion', self.conn, if_exists='append', index=False)  
        self.conn.commit()

    def insert_metodologia(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Metodologia', columnas[1]: 'Tipo_Metodologia'}, inplace=True)   
        df.to_sql('Dimension_Metodologia', self.conn, if_exists='append', index=False)  
        self.conn.commit()

    def insert_programa_academico(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Programa_Academico', columnas[1]: 'Nombre_Programa_Academico'}, inplace=True)   
        df.to_sql('Dimension_Academico', self.conn, if_exists='append', index=False)  
        self.conn.commit()
    
    def insert_sexo(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_sexo', columnas[1]: 'Sexo'}, inplace=True)   
        df.to_sql('Dimension_Sexo', self.conn, if_exists='append', index=False)  
        self.conn.commit()

    def insert_formacion(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Formacion', columnas[1]: 'Formacion'}, inplace=True)   
        df.to_sql('Dimension_Formacion', self.conn, if_exists='append', index=False)  
        self.conn.commit()
    
    def insert_snies_fact(self, df, columnas):
    # Renombrar las columnas para que coincidan con los nombres esperados en la base de datos
        df.rename(columns={
            columnas[0]: 'ID_Admitidos',
            columnas[1]: 'Fecha_Admitidos',
            columnas[2]: 'ID_Institucion',
            columnas[3]: 'ID_Metodologia'
        }, inplace=True)
        
        # Insertar los datos en la base de datos en la tabla SNIES_FACT
        df.to_sql('Tabla_Admitidos', self.conn, if_exists='append', index=False)
        
        # Confirmar los cambios en la base de datos
        self.conn.commit()

    def insert_graduados_fact(self, df, columnas):
        # Renombrar las columnas para que coincidan con los nombres esperados en la base de datos
        df.rename(columns={
            columnas[0]: 'ID_GRADUADO',
            columnas[1]: 'FECHA_GRADUACION',
            columnas[2]: 'ID_INSTITUCION',
            columnas[3]: 'ID_DEPARTAMENTO',
            columnas[4]: 'ID_ACREDITACION',
        }, inplace=True)

        # Insertar los datos en la base de datos en la tabla de graduados
        df.to_sql('Tabla_Graduados', self.conn, if_exists='append', index=False)

        # Confirmar los cambios en la base de datos
        self.conn.commit()

    def insert_inscritos_fact(self, df, columnas):
    # Renombrar las columnas para que coincidan con los nombres esperados en la base de datos
        df.rename(columns={
            columnas[0]: 'ID_INSCRITOS',
            columnas[1]: 'FECHA_INSCRIPCION',
            columnas[2]: 'ID_SEXO',
            columnas[3]: 'ID_FORMACION',
            columnas[4]: 'ID_PROGRAMA_ACADEMICO'
        }, inplace=True)

        # Insertar los datos en la base de datos en la tabla INSCRITOS_FACT
        df.to_sql('Tabla_Inscritos', self.conn, if_exists='append', index=False)

        # Confirmar los cambios en la base de datos
        self.conn.commit()
    
    def insert_matriculados_fact(self, df, columnas):
    # Renombrar las columnas para que coincidan con los nombres esperados en la base de datos
        df.rename(columns={
            columnas[0]: 'ID_MATRICULADOS',
            columnas[1]: 'ID_PROGRAMA_ACADEMICO',
            columnas[2]: 'ID_INSTITUCION',
            columnas[3]: 'ID_Año'
        }, inplace=True)

        # Insertar los datos en la base de datos en la tabla MATRICULADOS_FACT
        df.to_sql('Tabla_Matriculados', self.conn, if_exists='append', index=False)

        # Confirmar los cambios en la base de datos
        self.conn.commit()




class Cargue:

    def cargue_archivo(self, nombre_archivo, hoja, encabezado, codigo_institucion):
        df = pd.read_excel(nombre_archivo, sheet_name=hoja, header=encabezado)
        df = df[df['CÓDIGO DE LA INSTITUCIÓN'].isin(codigo_institucion)]        
        return df