from entities.Graph import Graph
from entities.Node import Node
from entities.Edge import Edge
from entities.Vertex import Vertex
from typing import Type, List, Union


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
    # file_name = input("Nome do arquivo de input: ")

    #is_directed_input = input("Grafo direcionado? (y/n): ")
    #is_directed = True if is_directed_input == 'y' else False
    is_directed = False

    graph = Graph(is_directed)

    # with open(file_name, 'r') as f:
    with open('./test_files/test_1.txt', 'r') as f:
        num_vertices, num_edges = map(int, f.readline().split())

        for i in range(num_vertices):
            graph.add_vertex(i + 1)

        for i in range(num_edges):
            u, v = map(int, f.readline().split())
            graph.add_edge(u, v)
    
    '''Algoritimo fake'''
    ordem_vertices = []
    node_src = Node(graph.check_if_vertex_exists(3), 999, None, False)
    ordem_vertices.append(node_src)

    #Inicia o vertice original
    node_src.set_cost(0)
    node_src.set_vertex_a(node_src.get_vertex())
    
    for c in range(num_vertices):
        node_src = ordem_vertices[c]
        edge_adj = graph.get_neighbors_edges(node_src.get_vertex())

        for i in range(len(edge_adj)):
            node_sec = Type[Node]
            vertex_s = edge_adj[i].get_neighbor_vertex(node_src.get_vertex())
            aux = node_in(ordem_vertices, vertex_s)
            
            if aux[0] == True and aux[1].get_is_closed() == True: 
                continue
            elif aux[0] == True:
                node_sec = aux[1]
            else: 
                node_sec = Node(vertex_s, 999, node_src.get_vertex(), False)
                ordem_vertices.append(node_sec)

            soma = node_src.get_cost() + edge_adj[i].get_weight()
            if (soma < node_sec.get_cost()):
                node_sec.set_cost(soma)
                node_sec.set_vertex_a(node_src.get_vertex())

        node_src.set_closed_status(True)

        for node in ordem_vertices:
            print(node.get_vertex(), end=' ')
            print(node.get_cost(), end=' ')
            print(node.get_vertex_ant(), end=' ')
            print(node.get_is_closed(), end=' ')
            print()
        print()
            
                
            
def node_in(lista: List[Type[Node]], vertex: Type[Vertex]) -> List[Union[bool, Type[Node]]]:
    end = [False, None]
    for node in lista:
        if node.get_vertex() == vertex:
            end = [True, node]
            break
    return end


# read_from_terminal()
read_from_file()

