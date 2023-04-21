from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
import glob, os

def index(request):
    
    return render(request, 'home/index.html')

def playground(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GraphForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            n_vertices = form.cleaned_data['n_vertices']
            n_edges = form.cleaned_data['n_edges']
            is_directed = form.cleaned_data['is_directed']
            ids = form.cleaned_data['ids']
            vertices_1 = form.cleaned_data['vertices_1']
            vertices_2 = form.cleaned_data['vertices_2']
            weights = form.cleaned_data['weights']

            t_ids, t_vertices_1, t_vertices_2, t_weights = input_treatment(ids, vertices_1, vertices_2, weights)
            ###################################
            # IMPLEMENT GRAPH ALGORITHMS CODE #
            ###################################

            graph_generated = None
            # find all .html files inside de templates graph folder
            graph_html_path = glob.glob(os.path.join(settings.BASE_DIR, 'templates/graph/*.html'))
            # check if any file is found
            if graph_html_path:
                # render the .html file to string
                graph_generated = render_to_string(graph_html_path[0])
                # remove generated graph html file
                os.remove(graph_html_path.pop())

            # redirect to a new URL:
            return render(request, 'playground/index.html', {'form': form, 'graph': graph_generated})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GraphForm()

    return render(request, 'playground/index.html', {'form': form})


class GraphForm(forms.Form):
    is_directed = forms.BooleanField(label='Graph is Directed (y/n)', required=False)
    n_vertices = forms.CharField(label='Vertices Quantity', max_length=100, widget=forms.TextInput(attrs={'class': 'vertex_area'}))
    n_edges = forms.CharField(label='Edges Quantity', max_length=100)
    ids = forms.CharField(label='Ids do Vertice', max_length=100)
    vertices_1 = forms.CharField(label='Vertices 1', max_length=100)
    vertices_2 = forms.CharField(label='Vertices 2', max_length=100)
    weights = forms.CharField(label='Weight (optional)', max_length=100, required=False)

def input_treatment(ids, vertices_1, vertices_2, weights):
    t_ids = ids.replace(" ", "").split(",")
    t_vertices_1 = vertices_1.replace(" ", "").split(",")
    t_vertices_2 = vertices_2.replace(" ", "").split(",")
    t_weights = weights.replace(" ", "").split(",")

    return t_ids, t_vertices_1, t_vertices_2, t_weights
