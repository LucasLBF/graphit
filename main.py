from entities.Graph import Graph
from entities.Node import Node
from entities.Edge import Edge
from entities.Vertex import Vertex
from entities.DjkstraStrategy import DjkstraStrategy
from typing import Type, List, Union, Dict
from pyvis.network import Network
from util import archive

def read_from_terminal():
    is_directed_input = input("Grafo direcionado? (y/n): ")

    is_directed = True if is_directed_input == 'y' else False

    graph = Graph(is_directed)

    num_vertices = int(input("Numero de vertices: "))

    for i in range(num_vertices):
        graph.add_vertex(i + 1)

    num_edges = int(input("Numero de arestas: "))

    for i in range(num_edges):
        print(f"Informe os dois vertices da aresta {i + 1}")
        u, v = map(int, input().split())
        graph.add_edge(u, v)

    print(graph)

def read_from_file():
    '''Arquivo deve ter o formato igual aos do diretorio test_files.
    Primeira linha: numero de vertices numero de arestas
    Segunda linha em diante sao as arestas no formato:
    vertice1 vertice2.'''
    file_name = "graphFile2.txt"#input("Nome do arquivo de input: ")

    graph = archive.read_graph_file(file_name)
    # adicionar algoritmo de djkstra
    #graph.set_shortest_path_strategy(DjkstraStrategy(graph))

    graph.set_djkstra_strategy(DjkstraStrategy(graph))
    #print(graph)
    #x = graph.get_raio_diametro()
    #print(x)
    pyvis_visualization(graph)
    d = graph.get_vertex_degree(3)
    print()
    # pyvis_visualization_sssp(graph, 2, 6)
    # pyvis_visualization(graph)
    #pyvis_visualization_sssp(graph, 2, 6)
        
            
def pyvis_visualization(graph: Type[Graph]) -> None:
    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)

    for vertex in graph.get_vertices():
        n.add_node(vertex.id, label=str(vertex.id))
    
    for edge in graph.get_edges():
        n.add_edge(edge.first_vertex.id, edge.second_vertex.id, width=3)
    
    n.write_html("graph.html", open_browser=True)

def pyvis_visualization_sssp(graph: Type[Graph], src_id: int, dest_id: int) -> None:

    shortest_path = graph.get_shortest_path(src_id, dest_id)
    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)

    for vertex in graph.get_vertices():
        is_highlighted = vertex in shortest_path['vertices']
        n.add_node(vertex.id, label=str(vertex.id), color='#dc2f02' if is_highlighted else '#97c2fc')
    
    for edge in graph.get_edges():
        is_highlighted = edge in shortest_path['edges']
        n.add_edge(edge.first_vertex.id,
                    edge.second_vertex.id,
                    label=str(edge.weight),
                    color='#dc2f02' if is_highlighted else '#97c2fc',
                    width=5 if is_highlighted else 2)
    
    n.write_html("graph.html", open_browser=True)

# read_from_terminal()
read_from_file()