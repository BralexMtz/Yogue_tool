import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


def get_model(file_name,list_x,val_y,test_size):
    BCancer = pd.read_csv(file_name)
    X = np.array(BCancer[list_x])
    Y = np.array(BCancer[[val_y]])
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                                test_size = test_size, #cuanto para validar el modelo.
                                                                                random_state = 1234,
                                                                                shuffle = True)
    Clasificacion = linear_model.LogisticRegression()
    Clasificacion.fit(X_train, Y_train.ravel())
    score=Clasificacion.score(X_validation, Y_validation)
    Y_Clasificacion = Clasificacion.predict(X_validation)
    Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                    Y_Clasificacion, 
                                    rownames=['Real'], 
                                    colnames=['Clasificación']) 
    columns= [Matriz_Clasificacion.columns.tolist()]
    columns[0].insert(0," ")
    Matriz_Clasificacion_list=columns + Matriz_Clasificacion.reset_index().values.tolist()
    ecuacion=""+str(Clasificacion.intercept_[0])
    for i in range(0,len(list_x)):
        if int(Clasificacion.coef_[0][i]) >0:
            sign=" + "
        else:
            sign=" - "
        ecuacion+=sign+str(Clasificacion.coef_[0][i])+list_x[i]

    return score*100,Matriz_Clasificacion_list,classification_report(Y_validation, Y_Clasificacion),ecuacion

