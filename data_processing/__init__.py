import numpy as np
import time
import pandas as pd
from datetime import datetime, date 
pd.options.mode.chained_assignment = None 
import pathlib


def get_data():
    data=pd.read_csv(r'.\data\aprobados_crudos.csv', delimiter=',', error_bad_lines=False,encoding='latin-1') 
    data['documentoIdentificacion']=data['documentoIdentificacion'].astype('object')
    return data

def filter_by_date(data,year):  #date='2022-01-01'
    data['Fecha de Inicio'] = data[' fechaInscripcion'].astype('string').str.strip()
    data['Fecha de Inicio'] = pd.to_datetime(data['Fecha de Inicio'], format='%d-%m-%Y',exact='strict')
    year_filtered_data =data.loc[(data['Fecha de Inicio'] >= year)]
    return year_filtered_data

def filter_by_certificate_date(data,year):  #date='2022-01-01'
    data[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes']=data[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes'].apply(pd.to_numeric, errors='coerce', axis=1)
    print(data.dtypes)
    data_filtered =data[data[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes-fecha']>=0]
    print(data_filtered)
    data['Fecha de Certificacion'] = data[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes-fecha'].astype('string').str.strip()
    data['Fecha de Certificacion'] = pd.to_datetime(data['Fecha de Certificacion'], format='%d-%m-%Y',exact='strict')
    year_filtered_data =data.loc[(data['Fecha de Certificacion'] >= year)]
    return year_filtered_data



def change_format(year_filtered_data): 

    numeric_col=['documentoIdentificacion',
       ' Bienvenida(lecciones)', ' Bienvenida(practica)',
       ' Bienvenida(Evaluación de Diagnóstico)',
       ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(lecciones)',
       ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(practica)',
       ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(lecciones)',
       ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(practica)',
       ' Módulo 3: Ahorro y consumo responsable.(lecciones)',
       ' Módulo 3: Ahorro y consumo responsable.(practica)',
       ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(lecciones)',
       ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(practica)',
       ' Clases en Vivo(lecciones)', ' Clases en Vivo(practica)',
       ' Examen de Certificación | Curso Online Educación Financiera para Jóvenes']

    strings_col=[' nombre', ' email', ' sexo', ' pais', ' ciudad']

    year_filtered_data[numeric_col]=year_filtered_data[numeric_col].apply(pd.to_numeric, errors='coerce', axis=1)
    year_filtered_data[strings_col]=year_filtered_data[strings_col].apply(lambda x: x.astype('string'))
    year_filtered_data[' fechaNacimiento'] = pd.to_datetime(year_filtered_data[' fechaNacimiento'], errors='coerce')
    #year_filtered_data['Fecha de Certificación'] = year_filtered_data[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes-fecha'].astype('string').str.strip()
    #year_filtered_data['Fecha de Certificación'] = pd.to_datetime(year_filtered_data['Fecha de Certificación'], format='%d-%m-%Y',exact='strict')
    #year_filtered_data.to_csv(r'./data/format_data.csv', index=False)
    return year_filtered_data

def add_age(format_data):
    def calculate_age(born):
        today = date.today()
        age = (today.year - born.year)
        return age

    format_data['Edad'] = format_data[' fechaNacimiento'].apply(calculate_age)
    format_data['Edad']=format_data['Edad'].astype('Int64')

    return format_data

def add_attendance(data):

    df_lecciones = data[[' Bienvenida(lecciones)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(lecciones)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(lecciones)',
    ' Módulo 3: Ahorro y consumo responsable.(lecciones)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(lecciones)']]


    #Se pasa a numpy array por reemplazo facil de los valores NaN como el "-"
    df_np=df_lecciones.to_numpy()
    df= np.where(df_np==' -',0,df_np)       #Reemplazo
    df1=df.astype(np.int64)               #Cambio de tipo
    suma=np.sum(df1,axis=1)               #Suma de actividades por alumno

    total_actividades=48                   #Actividades totales en el Curso de Educacion Financiera para Jovenes
    asistencia=(suma/total_actividades)*100   #Calculo de asistencia
    data['Porcentaje Asistencia']=asistencia
    #data = pd.DataFrame(data)
    data['Porcentaje Asistencia']=data['Porcentaje Asistencia'].where(data['Porcentaje Asistencia'] > 0 , 0)

    return data



def add_active_students(data):
    
    global etiqueta 
    def etiquetas_activo(asistencia): 
        if asistencia < 5.00:
            etiqueta='Inactivo'
        elif asistencia >= 5.00 and asistencia <= 200.00:
            etiqueta='Activo'
        else: 
            etiqueta='Inactivo'
        return etiqueta

    data['Activo']=data['Porcentaje Asistencia'].apply(etiquetas_activo)

    return data

def add_practice_mean(data):
    df_practicas = data[[' Bienvenida(practica)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(practica)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(practica)',
    ' Módulo 3: Ahorro y consumo responsable.(practica)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(practica)']]

    df_np=df_practicas.to_numpy()
    df= np.where(df_np==np.NaN,0,df_np)       
    df[np.isnan(df)]  = 0
    df1=df.astype(np.int64)               
    mean=np.mean(df1,axis=1)               

    data['Promedio de practicas']=mean
    return data

def add_approved_by_module(data):
    df_lecciones= data[[' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(lecciones)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(lecciones)',
    ' Módulo 3: Ahorro y consumo responsable.(lecciones)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(lecciones)']]

    df_lecciones.columns=['Modulo 1','Modulo 2','Modulo 3','Modulo 4']

    data['Aprobados Modulo 1'] =df_lecciones['Modulo 1'].apply(lambda x: 'Aprobo módulo 1' if x >= 1 else 'No aprobo módulo 1') 
    data['Aprobados Modulo 2'] =df_lecciones['Modulo 2'].apply(lambda x: 'Aprobo módulo 2' if x >= 1 else 'No aprobo módulo 2') 
    data['Aprobados Modulo 3'] =df_lecciones['Modulo 3'].apply(lambda x: 'Aprobo módulo 3' if x >= 1 else 'No aprobo módulo 3') 
    data['Aprobados Modulo 4'] =df_lecciones['Modulo 4'].apply(lambda x: 'Aprobo módulo 4' if x >= 1 else 'No aprobo módulo 4') 

    return data

def add_final_label(data):
    df_lecciones= data[[' Examen de Certificación | Curso Online Educación Financiera para Jóvenes']]
    df_lecciones.columns=['Examen']


    def estudiante_aprobado(examen):
        if examen >= 8:
            estado='Aprobado'
        elif examen >= 1 and examen < 8:
            estado='Egresado'
        else:
            estado='No culminado'
        return estado

    aprobados=df_lecciones['Examen'].apply(estudiante_aprobado)

    data['Etiqueta Estudiante']=aprobados
    return data

def sort_columns(data):
    datos_limpios=data[['documentoIdentificacion',' nombre',' sexo',' fechaNacimiento','Edad',' pais',' ciudad',' telefono',' email',' fechaInscripcion',
    ' Examen de Certificación | Curso Online Educación Financiera para Jóvenes-fecha',' Bienvenida(lecciones)',
    ' Bienvenida(practica)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(lecciones)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(practica)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(lecciones)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(practica)',
    ' Módulo 3: Ahorro y consumo responsable.(lecciones)',
    ' Módulo 3: Ahorro y consumo responsable.(practica)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(lecciones)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(practica)',
    ' Examen de Certificación | Curso Online Educación Financiera para Jóvenes',
    'Porcentaje Asistencia',
    'Activo',
    'Promedio de practicas',
    'Aprobados Modulo 1',
    'Aprobados Modulo 2',
    'Aprobados Modulo 3',
    'Aprobados Modulo 4',
    'Etiqueta Estudiante']]

    datos_limpios.columns=['CI','Nombres y Apellidos','Género','Fecha de Nacimiento','Edad','País','Ciudad','Teléfono','Email','Fecha de Inicio','Fecha de Finalización',
    ' Bienvenida(lecciones)',
    ' Bienvenida(practica)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(lecciones)',
    ' Módulo 1: La importancia de la Educación Financiera ¿cómo influye en tu futuro y felicidad?(practica)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(lecciones)',
    ' Módulo 2: Conozcamos el funcionamiento del Sistema Financiero.(practica)',
    ' Módulo 3: Ahorro y consumo responsable.(lecciones)',
    ' Módulo 3: Ahorro y consumo responsable.(practica)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(lecciones)',
    ' Módulo 4: ¿Cómo hago lo que quiero controlando mi dinero y mis recursos?(practica)',
    ' Examen de Certificación',
    'Porcentaje de Asistencia',
    'Estudiante Activo',
    'Promedio de prácticas',
    'Aprobados Modulo 1',
    'Aprobados Modulo 2',
    'Aprobados Modulo 3',
    'Aprobados Modulo 4',
    'Etiqueta Estudiante']

    return datos_limpios

def add_merge_data_etnics(sort_data,data_etnics):
    data_with_etnics = pd.merge(sort_data, data_etnics, on='CI')
    data_with_etnics.drop_duplicates(subset='CI', keep='first', inplace=True)
    data_with_etnics.reset_index(drop=True, inplace=True)
    return data_with_etnics
