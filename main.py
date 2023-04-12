from entities.Graph import Graph
from typing import Type

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
    '''
    #print(graph)
    neighbors = graph.get_neighbors(graph.check_if_vertex_exists(4))
    for k in neighbors.items():
        n_list = k[1]
    for c in range(0, len(n_list)):
        print(n_list[c], graph.get_neighbors_undirected(n_list[c]))

    edges = graph.get_edges()
    print(len(edges), end='\n\n')

    for c in range(0, len(edges)):
        print(edges[c].get_vertex(), end=' ')
        print("Weight: " + str(edges[c].get_weight()))'''
    
    '''Algoritimo fake'''
    indSrc = -1
    v = graph.get_vertices()
    e = graph.get_edges()

    for c in range(0, len(v)):
        if 3 == v[c].getID():
            indSrc = c
            break

    # Cria a tabela dos vertices
    vFechado = [False] * graph.get_order()
    vCusto = [0] * graph.get_order()
    vAnterior = ['null'] * graph.get_order()

    #Passo 1
    print(v[indSrc])
    vCusto[indSrc] = 0
    vAnterior[indSrc] = str(v[indSrc].getID())
    eAdj = graph.get_neighbors_edges(v[indSrc]) 

    print(graph.get_neighbors_undirected(v[indSrc]))
    
    print('P1')
    print(vCusto)
    print(vAnterior)
    print(vFechado) 

    #Passo 2 
    # vAdj[0].get_neighbor_vertex(v[indSrc])
    for c in range(0, len(eAdj)):
        vSec = eAdj[c].get_neighbor_vertex(v[indSrc])

        indSec = -1
        for i in range(0, len(v)):
            if vSec.getID() == v[i].getID():
                indSec = i
                break
        
        vCusto[indSec] = eAdj[c].get_weight() + vCusto[indSrc]
        vAnterior[indSec] = str(v[indSrc].getID())
    vFechado[indSrc] = True

    print('\nP2')
    print(vCusto)
    print(vAnterior)
    print(vFechado)
    



# read_from_terminal()
read_from_file()