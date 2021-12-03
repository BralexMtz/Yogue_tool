import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt
from scipy import cluster   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

def get_dendograma_url(file_name,columns_list):
    datos = pd.read_csv(file_name)
    Matriz_pre = np.array(datos[columns_list])
    estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler(con media y desv estandar) o MinMaxScaler(entre 0 y 1)si hay outlayers, provoca sesgo 
    MEstandarizada = estandarizar.fit_transform(Matriz_pre)   # Se calculan la media y desviación y se escalan los datos    
    plt.figure(figsize=(10, 7))
    plt.title("Casos de hipoteca")
    plt.xlabel('Hipoteca')
    plt.ylabel('Distancia')
    Arbol = shc.dendrogram(shc.linkage(MEstandarizada, method='complete', metric='euclidean'))
    url='dendograma.png'
    plt.savefig('algoritmos/static/assets/img/simulations/'+url)   # save the figure to file
    plt.close() 

    return url  

def get_cluster_data(file_name,columns_list,num_clusters):
    datos = pd.read_csv(file_name)
    Matriz_pre = np.array(datos[columns_list])
    estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler(con media y desv estandar) o MinMaxScaler(entre 0 y 1)si hay outlayers, provoca sesgo 
    MEstandarizada = estandarizar.fit_transform(Matriz_pre)   # Se calculan la media y desviación y se escalan los datos    
    #se crea modelo
    MJerarquico = AgglomerativeClustering(n_clusters=num_clusters, linkage='complete', affinity='euclidean')
    MJerarquico.fit_predict(MEstandarizada)
    # Agregamos etiqueta a los resultados
    datosEtq = datos.copy()
    datosEtq['clusterH'] = MJerarquico.labels_ #agregar las etiquetas
    # obtenemos numero de registros
    num_cluster=datosEtq.groupby(['clusterH'])['clusterH'].count()
    CentroidesH = datosEtq.groupby('clusterH').mean()
    CentroidesHC= CentroidesH.round(2)
    
    cluster_data=[]
    for c in range(0,num_clusters):
        cluster_info={}
        cluster_info["ClusterID"]=c
        cluster_info["numElementos"]=num_cluster[c]
        Centroides=CentroidesHC.loc[c]
        promedios={}
        for column in list(CentroidesHC.columns):
            promedios[column]=Centroides[column]
            
        cluster_info["promedios"]=promedios

        cluster_data.append(cluster_info)
    # data to list
    columns=list(datosEtq.columns)
    datosEtq=datosEtq.values.tolist()
    datosEtq.insert(0,columns)

    return datosEtq,cluster_data