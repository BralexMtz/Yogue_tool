from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

app_name='algoritmos'

urlpatterns=[
    path('',views.index,name='index'),
    path('apriori',views.apriori,name='apriori'),
    path('distancias',views.distancias,name='distancias'),
    path('clustering-jerarquico',views.cluster_jerarquico,name='cluster_jerarquico'),
    path('clustering-particional',views.cluster_particional,name='cluster_particional'),
    path('clasificacion-regresion-logistica',views.clasif_rlog,name='clasif_rlog'),
    path('arboles-de-pronostico',views.a_pronostico,name='a_pronostico'),
    path('arboles-de-clasificacion',views.a_clasif,name='a_clasif'),
    path('upload-files',views.upload,name='upload'),
]