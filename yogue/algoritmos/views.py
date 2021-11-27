from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .scripts import file
from .scripts import apriori_mod
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
    
        return render(request, 'upload.html',{
                'form': True,
                'file_uploaded':file_uploaded,
                'data':file.get_data(request.session['file_name'])
            })

def apriori(request):
    if 'file_name' in request.session.keys():
        return render(request,"apriori.html",{
            'file_name':os.path.basename(request.session['file_name']),
            'data': sample(file.get_data(request.session['file_name']), 100),
            'frecuency_table': apriori_mod.frecuencia(request.session['file_name']),
            'image_frecuency_url': apriori_mod.bar_frecuency(request.session['file_name'])
        })


    else:
        print("file not uploaded")
        return render(request,"apriori.html")

def distancias(request):
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

