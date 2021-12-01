import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
from scipy.spatial.distance import cdist
from scipy.spatial import distance


def get_matriz(file_name,metric_method):
    DataF = pd.read_csv(file_name)
    Distancias = cdist(DataF,DataF,metric=metric_method)
    MatrizDF = pd.DataFrame(Distancias)
    MatrizResult=MatrizDF.round(3) 
    columns=list(MatrizResult.columns)
    data_list=MatrizResult.values.tolist()
    data_list.insert(0,columns)
    return data_list

def get_single_distance(file_name ,vec1,vec2,metrica):

    DataF = pd.read_csv(file_name)
    Objeto1 = DataF.iloc[vec1]
    Objeto2 = DataF.iloc[vec2]
    if metrica == "euclidean":
        distancia = distance.euclidean(Objeto1,Objeto2)
    elif metrica == "chebyshev":
        distancia = distance.chebyshev(Objeto1,Objeto2)
    elif metrica == "cityblock":
        distancia = distance.cityblock(Objeto1,Objeto2)
    elif metrica == "minkowski":
        distancia = distance.minkowski(Objeto1,Objeto2)
    else: 
        return None
    return distancia