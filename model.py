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
            ID_graduado INT PRIMARY KEY ,
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
            ID_Admitidos INT PRIMARY KEY ,
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
            ID_Inscritos INT PRIMARY KEY ,
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
            ID_Matriculados INT PRIMARY KEY,
            ID_Programa_Academico INT,
            ID_Institucion INT,
            ID_Año INT,
            FOREIGN KEY (ID_Programa_Academico) REFERENCES
            Dimension_Programa_Academico(ID_Programa_Academico),
            FOREIGN KEY (ID_Institucion) REFERENCES Dimension_Institucion(ID_Institucion)
            )
                            ''')
        self.conn.commit()

    def insert_programa(self, df,columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)
        df.rename(columns={columnas[0]: 'ID', columnas[1]: 'NOMBRE'}, inplace=True)
        df.to_sql('PROGRAMA', self.conn, if_exists='append', index=False)
        self.conn.commit()
    
    def insert_departamento(self, df, columnas):
        df = df[columnas].drop_duplicates()
        df[columnas[0]] = df[columnas[0]].astype(int)    
        df.rename(columns={columnas[0]: 'ID_Departamento', columnas[1]: 'Nombre_Departamento'}, inplace=True)   
        df.to_sql('Dimension_Departamento', self.conn, if_exists='append', index=False)  
        self.conn.commit()

    def insert_snies_fact(self, df,columnas):
        df.rename(columns={columnas[0]: 'ID_INSTITUCION', columnas[1]: 'ID_PROGRAMA', columnas[2]: 'ID_AREA', columnas[3]: 'ID_SEXO', columnas[4]: 'ANIO', columnas[5]: 'SEMESTRE', columnas[6]: 'ADMITIDOS', columnas[7]: 'MATRICULADOS'}, inplace=True)
        df.to_sql('SNIES_FACT', self.conn, if_exists='append', index=False)
        self.conn.commit()


class Cargue:

    def cargue_archivo(self, nombre_archivo, hoja, encabezado, codigo_institucion):
        df = pd.read_excel(nombre_archivo, sheet_name=hoja, header=encabezado)
        df = df[df['CÓDIGO DE LA INSTITUCIÓN'].isin(codigo_institucion)]        
        return df