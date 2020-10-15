from django.shortcuts import render
from django.http import HttpResponse

def etude1 (resquest):
    return render(resquest, "Exemple_Etude/exemple.html") 