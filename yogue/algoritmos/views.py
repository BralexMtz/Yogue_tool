from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .scripts import file
from .scripts import apriori_mod
from .scripts import metric_mod
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
    
    try:
        print(request.session['file_name'])
    except:
        print("file not uploaded")
    return render(request,"index.html")

def cluster_jerarquico(request):
    
    return render(request,"index.html")

def cluster_particional(request):
    
    return render(request,"index.html")

def clasif_rlog(request):
    
    return render(request,"index.html")

def a_pronostico(request):
    
    return render(request,"index.html")

def a_clasif(request):
    
    return render(request,"index.html")

