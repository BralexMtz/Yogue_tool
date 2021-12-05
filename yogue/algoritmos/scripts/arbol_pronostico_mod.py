import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import model_selection
from sklearn.tree import plot_tree
from joblib import dump, load



def get_model(file_name,list_x,val_y,test_size,max_deep,min_split,min_leaf):

    Data = pd.read_csv(file_name)
    X = np.array(Data[list_x])
    Y = np.array(Data[[val_y]])
    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, 
                                                                        test_size = test_size, #cuanto para validar el modelo.
                                                                        random_state = 1234,
                                                                        shuffle = True)
    PronosticoAD = DecisionTreeRegressor( max_depth=max_deep, min_samples_split=min_split,min_samples_leaf=min_leaf)
    PronosticoAD.fit(X_train, Y_train.ravel())
    Y_Pronostico = PronosticoAD.predict(X_test)

    Criterio=PronosticoAD.criterion
    MAE=mean_absolute_error(Y_test, Y_Pronostico)
    MSE=mean_squared_error(Y_test, Y_Pronostico)
    RMSE=mean_squared_error(Y_test, Y_Pronostico, squared=False)   #True devuelve MSE, False devuelve RMSE
    score=r2_score(Y_test, Y_Pronostico)
    Importancia = pd.DataFrame({'Variable': list(Data[list_x]),
                            'Importancia': PronosticoAD.feature_importances_}).sort_values('Importancia', ascending=False)
    Importancia=[Importancia.columns.tolist()] + Importancia.values.tolist()

    plt.figure(figsize=(16,16))  
    plot_tree(PronosticoAD, feature_names = list_x)
    url='ArbolP.png'
    plt.savefig('algoritmos/static/assets/img/simulations/'+url)   # save the figure to file
    plt.close() 
    dump(PronosticoAD, 'media/models/ModeloAP.joblib')
    return MAE,MSE,RMSE,score*100,Importancia,url


def predict(dict_data):
    
    PronosticoAD = load('media/models/ModeloAP.joblib')
    PacienteID1 = pd.DataFrame(dict_data)
    result= PronosticoAD.predict(PacienteID1)[0]
    return result