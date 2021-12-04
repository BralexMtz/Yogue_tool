from sklearn.preprocessing import StandardScaler, MinMaxScaler  
import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator

def get_best_n_cluster(file_name,columns_list,max_iter=17):
    datos = pd.read_csv(file_name)
    Matriz_pre = np.array(datos[columns_list])
    estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler(con media y desv estandar) o MinMaxScaler(entre 0 y 1)si hay outlayers, provoca sesgo 
    MEstandarizada = estandarizar.fit_transform(Matriz_pre)   # Se calculan la media y desviación y se escalan los datos    
    #Definición de k clusters para K-means
    #Se utiliza random_state para inicializar el generador interno de números aleatorios
    SSE = []
    for i in range(2, max_iter):
        km = KMeans(n_clusters=i, random_state=0)
        km.fit(MEstandarizada)
        #inertia es igual a SSE
        SSE.append(km.inertia_) #se asigna SSE de cada alg al arreglo 
    kl = KneeLocator(range(2, max_iter), SSE, curve="convex", direction="decreasing")
    return kl.elbow #devuelve el valor adecuado para el codo

def get_cluster_data(file_name,columns_list,num_clusters):
    datos = pd.read_csv(file_name)
    Matriz_pre = np.array(datos[columns_list])
    estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler(con media y desv estandar) o MinMaxScaler(entre 0 y 1)si hay outlayers, provoca sesgo 
    MEstandarizada = estandarizar.fit_transform(Matriz_pre)   # Se calculan la media y desviación y se escalan los datos    
    #se crea modelo
    MParticional = KMeans(n_clusters=num_clusters, random_state=0).fit(MEstandarizada)
    MParticional.predict(MEstandarizada)
    # Agregamos etiqueta a los resultados
    datosEtq = datos.copy()
    datosEtq['cluster'] = MParticional.labels_ #agregar las etiquetas
    # obtenemos numero de registros
    num_cluster=datosEtq.groupby(['cluster'])['cluster'].count()
    CentroidesH = datosEtq.groupby('cluster').mean()
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