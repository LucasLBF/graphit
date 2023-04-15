from typing import Dict, List, Type, Union
from entities.Graph import Graph
from entities.Node import Node
from entities.Vertex import Vertex


class DjkstraStrategy():
    def __init__(self, graph: Type[Graph]):
        self.graph = graph


    def execute(self, vertex_src: int, vertex_dest: int, print_output: bool = False) -> Dict:
        '''Metodo de execucao do algoritmo'''
        return self.get_shortest_path_djkstra(vertex_src, vertex_dest)

    def node_in(self, lista: List[Type[Node]], vertex: Type[Vertex]) -> List[Union[bool, Type[Node]]]:
        '''Recebe uma lista de nodes e um vertice, retorna se o vertice esta na lista'''
        end = [False, None]
        for node in lista:
            if node.get_vertex() == vertex:
                end = [True, node]
                break
        return end
            
    def dijkstra_undirected(self, vertex_src: int, print_output: bool = False) -> List[Type[Node]]:
        '''Recebe o grafo e o vertice de origem, retorna o 
        menor caminho de cada vertice em relacao a origem'''
        num_vertices = self.graph.get_order()
        nodes_with_cost = []
        node_src = Node(self.graph.check_if_vertex_exists(vertex_src), 999, None, False)
        nodes_with_cost.append(node_src)

        node_src.set_cost(0)
        node_src.set_prev_node(None)

        for c in range(num_vertices):
            node_src = nodes_with_cost[c]
            edge_adj = self.graph.get_neighbors_edges(node_src.get_vertex())

            for i in range(len(edge_adj)):
                vertex_s = edge_adj[i].get_neighbor_vertex(node_src.get_vertex())
                aux = self.node_in(nodes_with_cost, vertex_s)

                if aux[0] == True and aux[1].get_is_closed() == True: 
                    continue
                elif aux[0] == True:
                    node_sec = aux[1]
                else: 
                    node_sec = Node(vertex_s, 999, node_src, False)
                    nodes_with_cost.append(node_sec)

                total_cost = node_src.get_cost() + edge_adj[i].get_weight()
                if (total_cost < node_sec.get_cost()):
                    node_sec.set_cost(total_cost)
                    node_sec.set_prev_node(node_src)

            node_src.set_closed_status(True)

            if print_output == True:
                for node in nodes_with_cost:
                    print(node.get_vertex(), end=' ')
                    print(node.get_cost(), end=' ')
                    print(node.get_vertex() if not node.prev_node else node.prev_node.get_vertex(), end=' ')
                    print(node.get_is_closed(), end=' ')
                    print()
                print()
        return nodes_with_cost
    
    def dijkstra_directed(self, vertex_src: int, print_output: bool = True) -> List[Type[Node]]:
        raise NotImplementedError

    def get_shortest_path_djkstra(self, src_id: int, dest_id: int) -> Dict:
        if self.graph.is_directed:
            nodes_with_cost = self.dijkstra_directed(src_id, False)
        else:
            nodes_with_cost = self.dijkstra_undirected(src_id, False)

        vertices = []
        edges = []
        tmp = dest_id

        for node in nodes_with_cost:
            if node.vertex.id == dest_id:
                tmp = node
                cost = node.get_cost()
                break
            
        while tmp.prev_node:
            edges.insert(0, self.graph.get_edge(tmp.vertex, tmp.prev_node.vertex))
            vertices.insert(0, tmp.vertex)
            tmp = tmp.prev_node
            if not tmp.prev_node:
                vertices.insert(0, tmp.vertex)

        result = {'edges': edges, 'vertices': vertices, 'cost': cost}
        return result
