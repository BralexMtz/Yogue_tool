import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn import model_selection
from sklearn.tree import plot_tree
from joblib import dump, load

def get_model(file_name,list_x,val_y,test_size,max_deep,min_split,min_leaf):

    Data = pd.read_csv(file_name)
    X = np.array(Data[list_x])
    Y = np.array(Data[[val_y]])
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                        test_size = test_size, #cuanto para validar el modelo.
                                                                        random_state = 1234,
                                                                        shuffle = True)
    ClasificacionAD = DecisionTreeClassifier( max_depth=max_deep, min_samples_split=min_split,min_samples_leaf=min_leaf)
    ClasificacionAD.fit(X_train, Y_train.ravel())
    Y_Clasificacion = ClasificacionAD.predict(X_validation)
    if Y_Clasificacion.dtype == "int64":
       Y_Clasificacion_class_names=np.array( [str(x) for x in Y_Clasificacion ])
    else:
        Y_Clasificacion_class_names=Y_Clasificacion
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                    Y_Clasificacion, 
                                    rownames=['Real'], 
                                    colnames=['Clasificación']) 
    columns= [Matriz_Clasificacion.columns.tolist()]
    columns[0].insert(0," ")
    Matriz_Clasificacion_list=columns + Matriz_Clasificacion.reset_index().values.tolist()
    score=ClasificacionAD.score(X_validation,Y_validation)
    reporte= classification_report(Y_validation,Y_Clasificacion)
    Importancia = pd.DataFrame({'Variable': list(Data[list_x]),
                            'Importancia': ClasificacionAD.feature_importances_}).sort_values('Importancia', ascending=False)
    Importancia=[Importancia.columns.tolist()] + Importancia.values.tolist()

    plt.figure(figsize=(16,16))  
    plot_tree(ClasificacionAD, 
            feature_names = list_x,
            class_names = Y_Clasificacion_class_names)
    url='ArbolC.png'
    plt.savefig('algoritmos/static/assets/img/simulations/'+url)   # save the figure to file
    plt.close() 
    dump(ClasificacionAD, 'media/models/ModeloAC.joblib')

    return score*100,reporte,Matriz_Clasificacion_list,Importancia,url

def predict(dict_data):
    ClasificacionAD = load('media/models/ModeloAC.joblib')
    PacienteID1 = pd.DataFrame(dict_data)
    result= ClasificacionAD.predict(PacienteID1)[0]
    return result