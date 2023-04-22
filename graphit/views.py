from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from graphit.entities.graph import Graph
from graphit.entities.djkstra_strategy import DjkstraStrategy
from graphit.utils.pyvis_visualization import pyvis_visualization, pyvis_visualization_sssp
import glob, os, sys

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
            is_directed = form.cleaned_data['is_directed']
            ids = form.cleaned_data['ids']
            vertices_1 = form.cleaned_data['vertices_1']
            vertices_2 = form.cleaned_data['vertices_2']
            weights = form.cleaned_data['weights']

            order = form.cleaned_data['order']
            size = form.cleaned_data['size']
            neighbors = form.cleaned_data['neighbors']
            degree = form.cleaned_data['degree']
            adjacent = form.cleaned_data['adjacent']
            radius = form.cleaned_data['radius']
            diameter = form.cleaned_data['diameter']
            shortest_path = form.cleaned_data['shortest_path']

            t_ids, t_vertices_1, t_vertices_2, t_weights = input_treatment(ids, vertices_1, vertices_2, weights)

            graph = Graph(is_directed)
            graph.set_djkstra_strategy(DjkstraStrategy(graph))

            for curr_id in t_ids:
                graph.add_vertex(curr_id)
            
            for index in range(len(t_vertices_1)):
                if t_weights:
                    graph.add_edge(t_vertices_1[index], t_vertices_2[index], t_weights[index])
                else:
                    graph.add_edge(t_vertices_1[index], t_vertices_2[index])

            results = {}

            if len(shortest_path) > 0:
                vertex_a, vertex_b = shortest_path.split(',')
                cost = pyvis_visualization_sssp(graph, vertex_a, vertex_b, os.path.join(settings.BASE_DIR, 'templates/graph/generated_graph.html'))
                results['shortest_path'] = {'vertex_a': vertex_a, 'vertex_b': vertex_b, 'value': cost}
            else:
                pyvis_visualization(graph, os.path.join(settings.BASE_DIR, 'templates/graph/generated_graph.html'))

            if order:
                results['graph_order'] = graph.get_order()
            if size:
                results['graph_size'] = graph.get_order()

            if len(neighbors) > 0:
                vertex_neighbors = graph.get_neighbors(graph.check_if_vertex_exists(neighbors), in_neighbors=True, out_neighbors=True)
                if graph.is_directed:
                    results['vertex_neighbors'] = { 'vertex': neighbors, 'in_neighbors' : vertex_neighbors['in_neighbors']['vertices'], 'out_neighbors': vertex_neighbors['out_neighbors']['vertices'], 'is_directed': graph.is_directed}
                else:
                    results['vertex_neighbors'] = { 'vertex': neighbors,  'neighbors': vertex_neighbors['neighbors']['vertices'], 'is_directed': graph.is_directed}
            
            if len(degree) > 0:
                vertex_degree = graph.get_vertex_degree(degree)
                if graph.is_directed:
                    results['vertex_degree'] = {'vertex': degree, 'in_degree' : vertex_degree['in_degree'], 'out_degree': vertex_degree['out_degree'], 'is_directed': graph.is_directed}
                else:
                    results['vertex_degree'] = {'vertex': degree, 'degree' : vertex_degree['degree'], 'is_directed': graph.is_directed}
                
            if len(adjacent) > 0:
                vertex_a, vertex_b = adjacent.split(',')
                check_adjacent = graph.are_vertices_adjacent(vertex_a, vertex_b)
                results['adjacent_vertices'] = {'vertex_a': vertex_a, 'vertex_b': vertex_b, 'answer': 'Sim' if check_adjacent else 'Não'}
            
            if radius or diameter:
                radius_diameter = graph.get_radius_diameter()
            if diameter:
                vertex_diameter = radius_diameter['diameter']
                results['diameter'] = vertex_diameter if vertex_diameter != sys.maxsize else 'Infinito'
            if radius:
                vertex_radius = radius_diameter['radius']
                results['radius'] = vertex_radius if vertex_radius != sys.maxsize else 'Infinito'



            graph_generated = None
            # find all .html files inside de templates graph folder
            graph_html_path = glob.glob(os.path.join(settings.BASE_DIR, 'templates/graph/*.html'))
            # check if any file is found
            if graph_html_path:
                # render the .html file to string
                graph_generated = render_to_string(graph_html_path[0])
                # remove generated graph html file
                # os.remove(graph_html_path.pop())

            context = {'form': form, 'graph': graph_generated, 'results': results}
            # redirect to a new URL:
            return render(request, 'playground/index.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GraphForm()


    return render(request, 'playground/index.html', {'form': form})


class GraphForm(forms.Form):
    is_directed = forms.BooleanField(label='Graph is Directed (y/n)', required=False)
    ids = forms.CharField(label='Ids do Vertice', max_length=100)
    vertices_1 = forms.CharField(label='Vertices 1', max_length=100)
    vertices_2 = forms.CharField(label='Vertices 2', max_length=100)

    weights = forms.CharField(label='Weight (optional)', max_length=100, required=False)
    order = forms.BooleanField(label='Graph Order', required=False)
    size = forms.BooleanField(label='Graph Size', required=False)
    neighbors = forms.CharField(label='Vertex neighbors', max_length=100, required=False)
    degree = forms.CharField(label='Vertex degree', max_length=100, required=False)
    adjacent = forms.CharField(label='Adjacent vertices', max_length=100, required=False)
    radius = forms.BooleanField(label='Graph radius', required=False)
    diameter = forms.BooleanField(label='Graph diameter', required=False)
    shortest_path = forms.CharField(label='Shortest path', max_length=100, required=False)



def input_treatment(ids, vertices_1, vertices_2, weights):
    t_ids = ids.replace(" ", "").split(",")
    t_vertices_1 = vertices_1.replace(" ", "").split(",")
    t_vertices_2 = vertices_2.replace(" ", "").split(",")
    t_weights = weights.replace(" ", "").split(",")

    t_weights = t_weights if t_weights[0] != "" else None
    if t_weights:
        t_weights = list(map(lambda weight: int(weight), t_weights))

    return t_ids, t_vertices_1, t_vertices_2, t_weights
