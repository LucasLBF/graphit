from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
    
    return render(request, 'home/index.html')

def playground(request):
    
    return render(request, 'playground/index.html')
