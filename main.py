from entities.Graph import Graph
from entities.Node import Node
from entities.Edge import Edge
from entities.Vertex import Vertex
from typing import Type, List, Union, Dict
from pyvis.network import Network

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
    with open('./test_files/test_4.txt', 'r') as f:
        num_vertices, num_edges = map(int, f.readline().split())

        for i in range(num_vertices):
            graph.add_vertex(i + 1)

        for i in range(num_edges):
            u, v = map(int, f.readline().split())
            graph.add_edge(u, v)

    # Teste lendo o test_4
    #dijkstra_undirected(graph, 1)
    # menor_caminho(3, 6, graph)
    # pyvis_visualization(graph)
    pyvis_visualization_sssp(graph, 1, 6)
    # get_shortest_path(graph, 3, 6)
        
            
def node_in(lista: List[Type[Node]], vertex: Type[Vertex]) -> List[Union[bool, Type[Node]]]:
    '''Recebe um node e um vertice, retorna se o veritce é 
    do node recebido, se sim retorna True e o Node'''
    end = [False, None]
    for node in lista:
        if node.get_vertex() == vertex:
            end = [True, node]
            break
    return end


def dijkstra_undirected(graph: Type[Graph], vertex_src: int, print: bool = True) -> List[Type[Node]]:
    '''Recebe o grafo e o vertice de origem, retorna o 
    menor caminho de cada vertice em relacao a origem'''
    num_vertices = graph.get_order()
    ordem_vertices = []
    node_src = Node(graph.check_if_vertex_exists(vertex_src), 999, None, False)
    ordem_vertices.append(node_src)

    node_src.set_cost(0)
    # node_src.set_vertex_a(node_src.get_vertex())
    node_src.set_prev_node(None)
    
    for c in range(num_vertices):
        node_src = ordem_vertices[c]
        edge_adj = graph.get_neighbors_edges(node_src.get_vertex())

        for i in range(len(edge_adj)):
            vertex_s = edge_adj[i].get_neighbor_vertex(node_src.get_vertex())
            aux = node_in(ordem_vertices, vertex_s)
            
            if aux[0] == True and aux[1].get_is_closed() == True: 
                continue
            elif aux[0] == True:
                node_sec = aux[1]
            else: 
                # node_sec = Node(vertex_s, 999, node_src.get_vertex(), False)
                node_sec = Node(vertex_s, 999, node_src, False)
                ordem_vertices.append(node_sec)

            soma = node_src.get_cost() + edge_adj[i].get_weight()
            if (soma < node_sec.get_cost()):
                node_sec.set_cost(soma)
                # node_sec.set_vertex_a(node_src.get_vertex())
                node_sec.set_prev_node(node_src)

        node_src.set_closed_status(True)

        if print == True:
            for node in ordem_vertices:
                print(node.get_vertex(), end=' ')
                print(node.get_cost(), end=' ')
                # print(node.get_vertex_ant(), end=' ')
                # print(node.prev_node.get_vertex(), end=' ')
                print(node.get_is_closed(), end=' ')
                print()
            print()
    return ordem_vertices


def menor_caminho(v1: int, v2: int, graph: Type[Graph]):
    min_cost_nodes = dijkstra_undirected(graph, v1, False)
    c = 0
    vertex = graph.check_if_vertex_exists(v2)

    while True:
        for nodes in min_cost_nodes:
            if nodes.get_vertex() == vertex:
                print(f'{nodes.get_vertex()} | Cost {nodes.get_cost()}')
                break

        if vertex == graph.check_if_vertex_exists(v1):
            break 
        vertex = nodes.get_vertex_ant()

def pyvis_visualization(graph: Type[Graph]) -> None:
    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)

    for vertex in graph.get_vertices():
        n.add_node(vertex.id, label=str(vertex.id))
    
    for edge in graph.get_edges():
        n.add_edge(edge.first_vertex.id, edge.second_vertex.id, color='red', width=5)
    
    n.write_html("graph.html", open_browser=True)

def get_shortest_path(graph: Type[Graph], src_id: int, dest_id: int) -> Dict:
    nodes_with_cost = dijkstra_undirected(graph, src_id, False)
    vertices = []
    edges = []
    tmp = dest_id

    for node in nodes_with_cost:
        if node.vertex.id == dest_id:
            tmp = node
            break
    
    while tmp.prev_node:
        edges.insert(0, graph.get_edge(tmp.vertex, tmp.prev_node.vertex))
        vertices.insert(0, tmp.vertex)
        tmp = tmp.prev_node
        if not tmp.prev_node:
            vertices.insert(0, tmp.vertex)

    result = {'edges': edges, 'vertices': vertices}
    return result

def pyvis_visualization_sssp(graph: Type[Graph], src_id: int, dest_id: int) -> None:

    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)
    shortest_path = get_shortest_path(graph, src_id, dest_id)

    for vertex in graph.get_vertices():
        is_highlighted = vertex in shortest_path['vertices']
        n.add_node(vertex.id, label=str(vertex.id), color='red' if is_highlighted else '#97c2fc')
    
    for edge in graph.get_edges():
        is_highlighted = edge in shortest_path['edges']
        n.add_edge(edge.first_vertex.id,
                    edge.second_vertex.id,
                    label=str(edge.weight),
                    color='red' if is_highlighted else '#97c2fc',
                    width=5 if is_highlighted else 2)
    
    n.write_html("graph.html", open_browser=True)


# read_from_terminal()
read_from_file()

