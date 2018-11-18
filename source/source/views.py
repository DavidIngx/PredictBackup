from django.http import HttpResponse
from django.shortcuts import loader


def prueba(response):
    pruebax = loader.get_template("base.html")

    
    return HttpResponse (pruebax.render())
