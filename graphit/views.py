from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from graphit.entities.graph import Graph
from graphit.entities.djkstra_strategy import DjkstraStrategy
from graphit.utils.pyvis_visualization import pyvis_visualization, pyvis_visualization_sssp
from graphit.utils.archive import read_graph_uploaded_file
import glob, os, sys

def index(request):
    
    return render(request, 'home/index.html')

def playground(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GraphForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            is_directed = form.cleaned_data['is_directed']
            ids = form.cleaned_data['ids']
            vertices_1 = form.cleaned_data['vertices_1']
            vertices_2 = form.cleaned_data['vertices_2']
            weights = form.cleaned_data['weights']
            file = form.cleaned_data['file']

            order = form.cleaned_data['order']
            size = form.cleaned_data['size']
            neighbors = form.cleaned_data['neighbors']
            degree = form.cleaned_data['degree']
            adjacent = form.cleaned_data['adjacent']
            radius = form.cleaned_data['radius']
            diameter = form.cleaned_data['diameter']
            shortest_path = form.cleaned_data['shortest_path']


            if file:
                graph = read_graph_uploaded_file(file)
                graph.set_djkstra_strategy(DjkstraStrategy(graph))
            
            else: 
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
                results['graph_size'] = graph.get_size()

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
            graph_html_path = glob.glob(os.path.join(settings.BASE_DIR, 'templates/graph/*.html'))
            if graph_html_path:
                graph_generated = render_to_string(graph_html_path[0])

            context = {'form': form, 'graph': graph_generated, 'results': results}

            return render(request, 'playground/index.html', context)

    else:
        form = GraphForm()


    return render(request, 'playground/index.html', {'form': form})


class GraphForm(forms.Form):
    is_directed = forms.BooleanField(label='O grafo é direcionado? (y/n)', required=False)
    ids = forms.CharField(label='Ids dos Vértices', max_length=100, required=False)
    vertices_1 = forms.CharField(label='Vertices 1', max_length=100, required=False)
    vertices_2 = forms.CharField(label='Vertices 2', max_length=100, required=False)

    weights = forms.CharField(label='Pesos (opcional)', max_length=100, required=False)
    order = forms.BooleanField(label='Ordem do grafo', required=False)
    size = forms.BooleanField(label='Tamanho do grafo', required=False)
    neighbors = forms.CharField(label='Checar vizinhança de vértices', max_length=100, required=False)
    degree = forms.CharField(label='Checar grau do vértice', max_length=100, required=False)
    adjacent = forms.CharField(label='Checar vértices adjacentes', max_length=100, required=False)
    radius = forms.BooleanField(label='Raio do grafo', required=False)
    diameter = forms.BooleanField(label='Diâmetro do grafo', required=False)
    shortest_path = forms.CharField(label='Menor caminho entre vértices', max_length=100, required=False)
    file = forms.FileField(label="Arquivo graphFile", required=False)



def input_treatment(ids, vertices_1, vertices_2, weights):
    t_ids = ids.replace(" ", "").split(",")
    t_vertices_1 = vertices_1.replace(" ", "").split(",")
    t_vertices_2 = vertices_2.replace(" ", "").split(",")
    t_weights = weights.replace(" ", "").split(",")

    t_weights = t_weights if t_weights[0] != "" else None
    if t_weights:
        t_weights = list(map(lambda weight: int(weight), t_weights))

    return t_ids, t_vertices_1, t_vertices_2, t_weights
