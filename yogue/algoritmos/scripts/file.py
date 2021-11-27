import pandas as pd                 # Para la manipulación y análisis de los datos



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