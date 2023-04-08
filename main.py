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

def read_from_file():
    '''Arquivo deve ter o formato igual aos do diretorio test_files.
    Primeira linha: numero de vertices numero de arestas
    Segunda linha em diante sao as arestas no formato:
    vertice1 vertice2.'''
    # file_name = input("Nome do arquivo de input: ")

    is_directed_input = input("Grafo direcionado? (y/n): ")

    is_directed = True if is_directed_input == 'y' else False
    
    graph = Graph(is_directed)

    # with open(file_name, 'r') as f:
    with open('./test_files/test_1.txt', 'r') as f:
        num_vertices, num_edges = map(int, f.readline().split())

        for i in range(num_vertices):
            graph.add_vertex(i + 1)

        for i in range(num_edges):
            u, v = map(int, f.readline().split())
            graph.add_edge(u, v)

    print(graph)

# read_from_terminal()
read_from_file()