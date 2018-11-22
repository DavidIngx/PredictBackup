from django.http import HttpResponse
from django.shortcuts import loader, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'load_dataset.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'load_dataset.html')


def read_file(request):
    dataframe = pd.read_excel("/media/oracle.xlsx")
    return render(request, 'showfile.html', {
    'make_list': dataframe
})


def prueba(response):
    pruebax = loader.get_template("simple_upload.html")


    return HttpResponse (pruebax.render())



def load_dataset(request):
    url = request.POST["url"]


    return render(request, "prueba.html",{"url":url})
