from django.urls.resolvers import URLPattern
from . import views
from django.urls import path, include

app_name='algoritmos'

urlpatterns=[
    path('',views.index,name='index'),
]