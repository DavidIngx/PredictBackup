from django.http import HttpResponse
from django.shortcuts import loader, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os

def simple_upload(request):
    os.chdir("/media/linux")
    drives = os.popen("ls","r")
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)



        return render(request, 'load_dataset.html', {
            'uploaded_file_url': uploaded_file_url

        })
    return render(request, 'load_dataset.html',{
    'drives':drives,})


def read_file(request):
    dataframe = pd.read_excel("http://localhost:8000/media/oracle_GKKqFRM.xlsx")
    prueba = dataframe["dos"]
    return render(request, 'showfile.html', {
    'make_list': prueba
})

def read_disk(request):
    p = os.popen("tree /home/linux/PredictBackup/ -D  -f -s -i","r")
    return render(request, 'showfile.html', {'make_list': p})

def prueba(response):
    pruebax = loader.get_template("simple_upload.html")


    return HttpResponse (pruebax.render())



def load_dataset(request):
    url = request.POST["url"]


    return render(request, "prueba.html",{"url":url})
