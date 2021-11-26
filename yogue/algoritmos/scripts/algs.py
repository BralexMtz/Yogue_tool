import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
from apyori import apriori


def alg_apriori(file_name):
    if file_name.endswith(".csv") :
        datos = pd.read_csv(file_name)
        print(datos.columns)
    else:
        print("NO ES UN ARCHIVO CSV")