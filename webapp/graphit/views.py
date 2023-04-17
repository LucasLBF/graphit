from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext

def index(request):
    
    return render(request, 'home/index.html')

def playground(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BasicForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            edges_form = []
            n_edges = range(int(form.cleaned_data['n_edges']))
            for i in n_edges:
                edge = EdgeForm(request.POST)
                edges_form.append(edge)
                

            # redirect to a new URL:
            return render(request, 'playground/index.html', {'form': form, 'edges_form': edges_form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BasicForm()

    return render(request, 'playground/index.html', {'form': form})


class BasicForm(forms.Form):
    n_vertices = forms.CharField(label='Id do Vertice', max_length=100, widget=forms.TextInput(attrs={'class': 'vertex_area'}))
    n_edges = forms.CharField(label='Numero de Arestas', max_length=100)
    is_directed = forms.BooleanField(label='Grafo direcionado (y/n)', required=False)

class EdgeForm(forms.Form):
    id = forms.CharField(label='Id do Vertice', max_length=100)
    v1 = forms.CharField(label='Vertice 1', max_length=100)
    v2 = forms.CharField(label='Vertice 2', max_length=100)
    weight = forms.CharField(label='Peso', max_length=100)

    def __init__(self, *args, **kwargs):
        super(EdgeForm, self).__init__(*args, **kwargs)
        # self.fields['id'].error_messages['required'] = ''