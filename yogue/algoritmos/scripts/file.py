import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib


def get_data(file_name):
    if file_name.endswith(".csv") :
        datos = pd.read_csv(file_name)
        columns=list(datos.columns)
        data_list=datos.values.tolist()
        data_list.insert(0,columns)
       
        return data_list
    else:
        print("NO ES UN ARCHIVO CSV")
        return None

def get_matriz_corr(file_name):
    if file_name.endswith(".csv") :
        datos = pd.read_csv(file_name)
        Matriz_corr=datos.corr(method='pearson')
        Matriz_corr=Matriz_corr.round(decimals=4 )
        #agregamos las columnas como indices en el cuerpo
        columns=list(Matriz_corr.columns)
        Matriz_corr.insert(loc=0,column="/",value=columns)
        #agregamos columnas en la lista
        columns=list(Matriz_corr.columns)
        data_list=Matriz_corr.values.tolist()
        data_list.insert(0,columns)

        return data_list
    else:
        print("NO ES UN ARCHIVO CSV")
        return None

def get_heatmap(file_name):
    if file_name.endswith(".csv") :
        datos = pd.read_csv(file_name)
        Matriz_corr=datos.corr(method='pearson')
        plt.figure(figsize=(14,12))
        MatrizInf = np.triu(Matriz_corr)
        sns.heatmap(Matriz_corr, cmap='RdBu_r', annot=True, mask=MatrizInf)
        url='heatmap.png'
        plt.savefig('algoritmos/static/assets/img/simulations/'+url)   # save the figure to file
        plt.close() 
        return url       

         
    else:
        print("NO ES UN ARCHIVO CSV")
        return None