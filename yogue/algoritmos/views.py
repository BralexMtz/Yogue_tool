from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .scripts import file
from .scripts import apriori_mod
from .scripts import metric_mod
from .scripts import clst_jrq_mod
from .scripts import clst_part_mod
from .scripts import clasif_rlog_mod
import os
from random import sample

# Create your views here.
def index(request):
    
    return render(request,"index.html")

def upload(request):
    if request.method == 'POST':
        
        if request.FILES.get('document') :
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                all_docs=Document.objects.all()
                for doc in all_docs:
                    try:
                        os.remove(doc.document.path)
                    except:
                        continue
                Document.objects.all().delete()
                form.save()
                all_docs = Document.objects.all()
                request.session['file_name']=all_docs[0].document.path

                return render(request, 'upload.html', {
                            'fileStatus': 'success',
                            'file_uploaded':os.path.basename(request.session['file_name']),
                            'data':file.get_data(request.session['file_name'])
                        })
            else:
                return render(request, 'upload.html', {
                    'fileStatus': 'fail',
                    'form': True
                })    
        elif request.POST.get('delete') :
            all_docs=Document.objects.all()
            for doc in all_docs:
                try:
                    os.remove(doc.document.path)
                except:
                    continue
            Document.objects.all().delete()
            del request.session['file_name']
            file_uploaded=False
            return render(request, 'upload.html',{
                'form': True,
                'file_uploaded':file_uploaded
            })
    else:
        file_uploaded= os.path.basename(request.session['file_name']) if 'file_name' in request.session.keys() else False
        data_param= file.get_data(request.session['file_name']) if request.session.get('file_name') else False
        return render(request, 'upload.html',{
                'form': True,
                'file_uploaded':file_uploaded,
                'data': data_param
            })

def apriori(request):
    if 'file_name' in request.session.keys():
        if request.method == 'POST':
            if request.POST.get('min_support') and request.POST.get('min_confidence') and request.POST.get('min_lift'):
                min_sup=float(request.POST['min_support'])
                min_conf=float(request.POST['min_confidence'])
                min_lif=float(request.POST['min_lift'])
                lista_rules=apriori_mod.get_rules(request.session['file_name'],min_sup,min_conf,min_lif)
            else:
                lista_rules=False
        else:
            lista_rules=False
        return render(request,"apriori.html",{
            'file_name':os.path.basename(request.session['file_name']),
            'data': sample(file.get_data(request.session['file_name']), 100),
            'frecuency_table': apriori_mod.frecuencia(request.session['file_name']),
            'image_frecuency_url': apriori_mod.bar_frecuency(request.session['file_name']),
            'lista_rules': lista_rules
        })


    else:
        print("file not uploaded")
        return render(request,"apriori.html")

def distancias(request):
    if 'file_name' in request.session.keys():
        if request.method == 'POST':
            if request.POST.get('metric'):
                metrica=request.POST['metric']
                matriz=metric_mod.get_matriz(request.session['file_name'],metrica)
                request.session['metrica']=metrica
                distancia2=False
                vector1=False
                vector2=False
            elif request.POST.get('vector1') and request.POST.get('vector2'):
                vector1=int(request.POST['vector1'])
                vector2=int(request.POST['vector2'])
                distancia2= metric_mod.get_single_distance(request.session['file_name'],vector1,vector2,request.session['metrica'])
                metrica=request.session['metrica']
                matriz=metric_mod.get_matriz(request.session['file_name'],metrica)
            else:
                vector1=False
                vector2=False
                distancia2=False
                metrica=False
                matriz=False
        else:
            vector1=False
            vector2=False
            distancia2=False
            metrica=False
            matriz=False
        return render(request,"metricas_distancias.html",{
            'file_name':os.path.basename(request.session['file_name']),
            'data': file.get_data(request.session['file_name'])[0:20],
            'dst_matrix': matriz,
            'metrica': metrica,
            'single_distance': distancia2,
            'vector1': vector1,
            'vector2': vector2
        })    
    else:
        return render(request,"metricas_distancias.html")    
    
def cluster_jerarquico(request):
    if 'file_name' in request.session.keys():
        if request.POST:
            if request.POST.get('predictoras'):
                request.session['column_list']=request.POST.getlist('predictoras')
                dendograma_url = clst_jrq_mod.get_dendograma_url(request.session['file_name'],request.session['column_list'])
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_jerarquico.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::],
                    'dendograma_url':dendograma_url
                })
            elif request.POST.get('numClusters'):
                numClusters=request.POST['numClusters']
                dataEtq,list_clusters=clst_jrq_mod.get_cluster_data(request.session['file_name'],request.session['column_list'],int(numClusters))

                dendograma_url = clst_jrq_mod.get_dendograma_url(request.session['file_name'],request.session['column_list'])
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_jerarquico.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::], #columnas posibles
                    'dendograma_url':dendograma_url,
                    'list_clusters': list_clusters,
                    'dataCluster': dataEtq
                })
            else:
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_jerarquico.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::]
                })
        else:
            M_corr=file.get_matriz_corr(request.session['file_name'])
            return render(request,"cluster_jerarquico.html",{
                'file_name':os.path.basename(request.session['file_name']),
                'data': file.get_data(request.session['file_name'])[0:20],
                'Matriz_corr': M_corr,
                'heatmap_url': file.get_heatmap(request.session['file_name']),
                'variables': M_corr[0][1::]
            })
    else:
        return render(request,"cluster_jerarquico.html")

def cluster_particional(request):
    if 'file_name' in request.session.keys():
        if request.POST:
            if request.POST.get('predictoras'):
                request.session['column_list']=request.POST.getlist('predictoras')
                best_n = clst_part_mod.get_best_n_cluster(request.session['file_name'],request.session['column_list'])
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_particional.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::],
                    'best_n': best_n
                })
            elif request.POST.get('numClusters'):
                numClusters=request.POST['numClusters']
                dataEtq,list_clusters=clst_part_mod.get_cluster_data(request.session['file_name'],request.session['column_list'],int(numClusters))

                best_n = clst_part_mod.get_best_n_cluster(request.session['file_name'],request.session['column_list'])
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_particional.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::], #columnas posibles
                    'best_n': best_n,
                    'list_clusters': list_clusters,
                    'dataCluster': dataEtq
                })
            else:
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"cluster_particional.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': M_corr[0][1::]
                })
        else:
            M_corr=file.get_matriz_corr(request.session['file_name'])
            return render(request,"cluster_particional.html",{
                'file_name':os.path.basename(request.session['file_name']),
                'data': file.get_data(request.session['file_name'])[0:20],
                'Matriz_corr': M_corr,
                'heatmap_url': file.get_heatmap(request.session['file_name']),
                'variables': M_corr[0][1::]
            })
    else:
        return render(request,"cluster_particional.html")

def clasif_rlog(request):
    if 'file_name' in request.session.keys():    
        if request.POST:
            if request.POST.get('predictoras') and request.POST.get('clase') and request.POST.get('test-size'):
                request.session['column_list']=request.POST.getlist('predictoras')
                request.session['predictora']=request.POST['clase']
                request.session['test-size']=request.POST['test-size']
                score,Matriz_Clasificacion,report,ecuacion= clasif_rlog_mod.get_model(request.session['file_name'],request.session['column_list'],request.session['predictora'],float(request.session['test-size']))
                M_corr=file.get_matriz_corr(request.session['file_name'])
                return render(request,"clasif_r_log.html",{
                    'file_name':os.path.basename(request.session['file_name']),
                    'data': file.get_data(request.session['file_name'])[0:20],
                    'Matriz_corr': M_corr,
                    'heatmap_url': file.get_heatmap(request.session['file_name']),
                    'variables': file.get_data(request.session['file_name'])[0][::],
                    'score':score,
                    'Matriz_Clasificacion': Matriz_Clasificacion,
                    'reporte':report,
                    'ecuacion':ecuacion
                })
        else:
            M_corr=file.get_matriz_corr(request.session['file_name'])
            return render(request,"clasif_r_log.html",{
                'file_name':os.path.basename(request.session['file_name']),
                'data': file.get_data(request.session['file_name'])[0:20],
                'Matriz_corr': M_corr,
                'heatmap_url': file.get_heatmap(request.session['file_name']),
                'variables': file.get_data(request.session['file_name'])[0][::]
            })
    else:
        return render(request,"clasif_r_log.html")

def a_pronostico(request):
    if 'file_name' in request.session.keys():
        # hacer post y entrenamiento

        M_corr=file.get_matriz_corr(request.session['file_name'])
        return render(request,"arboles_pronostico.html",{
            'file_name':os.path.basename(request.session['file_name']),
            'data': file.get_data(request.session['file_name'])[0:20],
            'Matriz_corr': M_corr,
            'heatmap_url': file.get_heatmap(request.session['file_name']),
            'variables': file.get_data(request.session['file_name'])[0][::]
        })    
    else:
        return render(request,"arboles_pronostico.html")

def a_clasif(request):
    if 'file_name' in request.session.keys():    
        next
    else:
        return render(request,"index.html")

def prediccion(request):
    if all(x in request.session.keys() for x in ['file_name','column_list', 'predictora','test-size']): 
        #modelo Clasif. R Logistica
        if request.POST:
            if all(x in request.POST for x in request.session['column_list']):
                variables= {}
                for key,value in list(request.POST.items()):
                    if key in request.session['column_list']:
                        variables[key]=[float(value)]
                resultado=clasif_rlog_mod.predict(request.session['file_name'],request.session['column_list'],request.session['predictora'],float(request.session['test-size']),variables)
                #resultado= "Maligno" if resultado=="M" else "Benigno"
                return render(request,"prediccion.html",{
                'vars':  request.session['column_list'],
                'result': resultado
                })
        else:

            return render(request,"prediccion.html",{
            'vars':  request.session['column_list']
            })
    else:
        return render(request,"prediccion.html")
