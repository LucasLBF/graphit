from typing import Dict, List, Type, Union
from entities import Graph
from entities.Node import Node
from entities.Vertex import Vertex


#class DjkstraStrategy():
    # def __init__(self, graph: Type[Graph]):
    #     self.graph = graph


# def execute(graph:Graph, vertex_src: int, vertex_dest: int, print_output: bool = False) -> Dict:
#     '''Metodo de execucao do algoritmo'''
#     if graph.is_directed:
#         nodes_with_cost = graph.dijkstra_directed(vertex_src)
            
#     else:
#         nodes_with_cost = graph.dijkstra_undirected(vertex_src)
def execute(graph:Graph, vertex_src: int, print_output: bool = False) -> Dict:
    '''Metodo de execucao do algoritmo'''
    nodes_with_cost = None
    if graph.is_directed:
        nodes_with_cost = dijkstra_directed(graph, vertex_src, print_output)
            
    else:
        nodes_with_cost = dijkstra_undirected(graph, vertex_src, print_output)
        
    return  nodes_with_cost

def node_in(lista: List[Type[Node]], vertex: Type[Vertex]) -> List[Union[bool, Type[Node]]]:
    '''Recebe uma lista de nodes e um vertice, retorna se o vertice esta na lista'''
    end = [False, None]
    for node in lista:
        if node.get_vertex() == vertex:
            end = [True, node]
            break
    return end
            
def dijkstra_undirected(graph: Graph, vertex_src: int, print_output: bool = True) -> List[Type[Node]]:
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

        if print_output == True:
            for node in ordem_vertices:
                print(node.get_vertex(), end=' ')
                print(node.get_cost(), end=' ')
                # print(node.get_vertex_ant(), end=' ')
                print(node.get_vertex() if not node.prev_node else node.prev_node.get_vertex(), end=' ')
                print(node.get_is_closed(), end=' ')
                print()
            print()
    return ordem_vertices
    
def dijkstra_directed(graph:Graph, vertex_src: int, print_output: bool = True) -> List[Type[Node]]:
    pass
