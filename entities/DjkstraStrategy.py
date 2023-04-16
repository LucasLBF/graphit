from typing import Dict, List, Type, Union
from entities.Graph import Graph
from entities.Node import Node
from entities.Vertex import Vertex
import sys
from heapq import heapify, heappush, heappop


class DjkstraStrategy():
    def __init__(self, graph: Type[Graph]):
        self.graph = graph


    def execute(self, vertex_src: int, vertex_dest: int) -> Dict:
        '''Metodo de execucao do algoritmo'''
        nodes_with_cost = self.djkstra_algorithm(vertex_src)
        dest_node = nodes_with_cost[vertex_dest]

        if not dest_node.is_connected:
            return {}
        else:
            return {'edges': dest_node.prev_edges, 'vertices': [node.vertex for node in dest_node.prev_nodes] + [dest_node.vertex], 'cost': dest_node.cost}
        # return self.get_shortest_path_djkstra(vertex_src, vertex_dest)

    def node_in(self, lista: List[Type[Node]], vertex: Type[Vertex]) -> List[Union[bool, Type[Node]]]:
        '''Recebe uma lista de nodes e um vertice, retorna se o vertice esta na lista'''
        end = [False, None]
        for node in lista:
            if node.get_vertex() == vertex:
                end = [True, node]
                break
        return end
            
    def djkstra_undirected(self, vertex_src: int, print_output: bool = False) -> List[Type[Node]]:
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
    
    def djkstra_algorithm(self, vertex_src: int) -> Dict[int, Type[Node]]:
        '''Recebe um vertice de partida e calcula a sua distancia para todos os outros vertices do grafo'''
        MAX_COST = sys.maxsize
        vertices = self.graph.get_vertices()
        TOTAL_VERTICES = len(vertices)
        nodes: Dict[int, Type[Node]] = {}
        closed_nodes: Dict[int, Type[Node]] = {}

        for vertex in vertices:
            new_node = Node(vertex, MAX_COST, [], [])
            nodes[vertex.id] = new_node

        curr_node = nodes[vertex_src]
        curr_node.cost = 0
        curr_node.is_connected = True
        heap = []

        while len(closed_nodes) != TOTAL_VERTICES:
            if self.graph.is_directed:
                adj_edges = self.graph.get_neighbors(curr_node.vertex, out_neighbors=True)['out_neighbors']['edges']
            else:
                adj_edges = self.graph.get_neighbors(curr_node.vertex)['neighbors']['edges']

            if curr_node.vertex.id not in closed_nodes:
                closed_nodes[curr_node.vertex.id] = curr_node
            for edge in adj_edges:
                neighbor_vertex_id = edge.get_neighbor_vertex(curr_node.vertex).id
                if neighbor_vertex_id not in closed_nodes:
                    if nodes[neighbor_vertex_id].cost > curr_node.cost + edge.weight:
                        neighbor = nodes[neighbor_vertex_id]
                        neighbor.cost = curr_node.cost + edge.weight
                        neighbor.prev_nodes = curr_node.prev_nodes + [curr_node]
                        neighbor.prev_edges = curr_node.prev_edges + [edge]
                    if not nodes[neighbor_vertex_id].is_in_heap:
                        heappush(heap, (nodes[neighbor_vertex_id].cost, nodes[neighbor_vertex_id]))
                        nodes[neighbor_vertex_id].is_in_heap = True
                        nodes[neighbor_vertex_id].is_connected = True
                
            heapify(heap)

            if len(closed_nodes) == TOTAL_VERTICES:
                continue

            if len(heap) == 0 and len(closed_nodes) != TOTAL_VERTICES:
                break

            min_cost_neighbor = heap[0][1]
            heappop(heap)
            curr_node = min_cost_neighbor

        return nodes
