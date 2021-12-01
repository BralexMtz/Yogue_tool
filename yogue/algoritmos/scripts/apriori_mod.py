import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
from apyori import apriori

def get_pandas_frecuency(fname):
    Datos = pd.read_csv(fname, header=None)
    #Se incluyen todas las transacciones en una sola lista
    Transacciones = Datos.values.reshape(-1).tolist() #-1 significa 'dimensión desconocida'

    #Se crea una matriz (dataframe) usando la lista y se incluye una columna 'Frecuencia'
    Lista = pd.DataFrame(Transacciones)
    Lista['Frecuencia'] = 0 # se agrega una columna y rellena con 0 cada renglon de frecuencia.

    #Se agrupa los elementos     , sin nombre en el indice, se agrupan y cuentan los valores.(en el caso de frecuencua se suma) 
    Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
    Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
    Lista = Lista.rename(columns={0 : 'Item'}) # ponerle nombre a la columna
    return Lista

def frecuencia(file_name):
    Lista=get_pandas_frecuency(file_name)
    columns=list(Lista.columns)
    data_list=Lista.values.tolist()
    data_list.insert(0,columns)
    return data_list

def bar_frecuency(file_name):
    Lista=get_pandas_frecuency(file_name)
    plt.figure(figsize=(12,20), dpi=300)
    plt.ylabel('Item')
    plt.xlabel('Frecuencia')
    plt.barh(Lista['Item'], width=Lista['Frecuencia'], color='#16ACC0')
    url='bar_frecuency.png'
    plt.savefig('algoritmos/static/assets/img/simulations/'+url)   # save the figure to file
    plt.close() 
    return url

def get_rules(file_name,min_support_v,min_confidence_v,min_lift_v):
    Datos = pd.read_csv(file_name, header=None)
    DatosLista = Datos.stack().groupby(level=0).apply(list).tolist()
    DatosLista 
    ReglasC1 = apriori(DatosLista, 
                   min_support=min_support_v, 
                   min_confidence=min_confidence_v, 
                   min_lift=min_lift_v)
    ResultadosC1 = list(ReglasC1)
    Rules_res=[]
    for item in ResultadosC1:
        #El primer índice de la lista
        Emparejar = item[0]
        items = [x for x in Emparejar]
        Rules_res.append({
            "regla":str(items) ,
            "soporte": str(round(item[1],4)) ,
            "confianza": str(round(item[2][0][2],4)) ,
            "lift": str(round(item[2][0][3],4))
            })
    return Rules_res
        
    