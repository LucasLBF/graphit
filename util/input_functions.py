import sys
import time
from typing import Type
from util.pyvis_visualization import pyvis_visualization_sssp
from util.archive import read_graph_file
from entities.DjkstraStrategy import DjkstraStrategy
from entities.Graph import Graph

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

def test_files_from_terminal():
    print("1 - Test all files")
    print("2 - Test individual file")
    option = int(input(">> "))

    if option == 1:
        test_all_files()
    elif option == 2:
        print("Enter graphFile number: ")
        file_num = input(">> ")
        test_file(f"graphFile{file_num}.txt")


def test_file(file_name: str):
    '''Arquivo deve ter o formato igual aos do diretorio test_files.
    Primeira linha: numero de vertices numero de arestas
    Segunda linha em diante sao as arestas no formato:
    vertice1 vertice2.'''

    print("---------------------------------------------------")
    print(f"------------  {file_name.upper()} ------------")
    print("---------------------------------------------------")

    graph = read_graph_file(file_name)
    graph.set_djkstra_strategy(DjkstraStrategy(graph))

    print_all_options(graph)


def test_all_files():
    for i in range(8):
        try:
            file_name = f"graphFile{i + 1}.txt"

            print("---------------------------------------------------")
            print(f"------------  {file_name.upper()} ------------")
            print("---------------------------------------------------")

            graph = read_graph_file(file_name)
            graph.set_djkstra_strategy(DjkstraStrategy(graph))

            print_all_options(graph)

        except Exception as e:
            print(e)
            continue

        finally:
            time.sleep(1)

def print_all_options(graph: Type[Graph]):
    print(graph)
    print("Ordem do grafo:", graph.get_order())
    print("Tamanho do grafo:", graph.get_size())
    neighbors = graph.get_neighbors(graph.check_if_vertex_exists("D"),
                                    in_neighbors=True,
                                    out_neighbors=True)
    if graph.is_directed:
        print("Vizinhanca de entrada de D:", neighbors["in_neighbors"]["vertices"])
        print("Vizinhanca de saida de D:", neighbors["out_neighbors"]["vertices"])
    else: 
        print("Vertices adjacentes de D:", neighbors["neighbors"]["vertices"])

    vertex_degree = graph.get_vertex_degree("A")
    if graph.is_directed:
        print("Grau de entrada do vertice A:", vertex_degree["in_degree"])
        print("Grau de saida do vertice A:", vertex_degree["out_degree"])
    else: 
        print("Grau do vertice A:", vertex_degree["degree"])

    print("Vertices D e E sao adjacentes?", graph.are_vertices_adjacent("D", "E"))

    radius_diameter = graph.get_radius_diameter()
    radius = radius_diameter['radius'] 
    diameter = radius_diameter['diameter']
    print(f"Raio: {radius if radius != sys.maxsize else 'Infinito'} | Diametro: {diameter if diameter != sys.maxsize else 'Infinito'}", )

    pyvis_visualization_sssp(graph, "A", "C")
    print()
