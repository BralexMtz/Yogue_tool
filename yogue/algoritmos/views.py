from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .scripts import algs
import os

# Create your views here.
def index(request):
    
    return render(request,"index.html")

def upload(request):
    if request.method == 'POST':
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
                        'fileStatus': 'success'
                    })
        else:
            form = DocumentForm()
            return render(request, 'upload.html', {
                'fileStatus': 'fail',
                'form': form
            })    
    else:
        form = DocumentForm()
        return render(request, 'upload.html',{
            'form': form
        })
def apriori(request):
    try:
        print(request.session['file_name'])
        algs.alg_apriori(request.session['file_name'])
    except:
        print("file not uploaded")
    return render(request,"index.html")

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

