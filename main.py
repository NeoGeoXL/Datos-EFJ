from data_processing import *
import data_processing

year='2022-01-01'

##### TODOS LOS ESTUDIANTES REGISTRADOS #########

#Obtencion de datos
data= data_processing.get_data()
#data_etnics = data_processing.get_data_etnics()


#Filtrado de datos por fecha
year_filtered_data = data_processing.filter_by_date(data,year)

#Formateo de tipos de datos
format_data = data_processing.change_format(year_filtered_data)

#Procesamiento de datos que requiere alaU
data_with_age = data_processing.add_age(format_data)
data_with_attendance = data_processing.add_attendance(data_with_age)
data_with_actives = data_processing.add_active_students(data_with_attendance)
data_with_practice_mean = data_processing.add_practice_mean(data_with_actives)
data_with_approved_modules = data_processing.add_approved_by_module(data_with_practice_mean)
data_with_final_label = data_processing.add_final_label(data_with_approved_modules)
sort_data = data_processing.sort_columns(data_with_final_label)
#sort_data['CI'] = sort_data['CI'].astype('object')

#Agregar datos de etnias al dataset

#data_with_etnics = data_processing.add_merge_data_etnics(sort_data,data_etnics)

sort_data.to_csv('.\output data\aprobados_limpios.csv',index=False)

