from typing import Dict, List, Type, Union
from graphit.entities.graph import Graph
from graphit.entities.node import Node
from graphit.entities.vertex import Vertex
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

    def djkstra_algorithm(self, vertex_src: int) -> Dict[int, Type[Node]]:
        '''Recebe um vertice de partida e calcula a sua distancia para todos os outros vertices do grafo'''
        MAX_COST = sys.maxsize
        vertices = self.graph.get_vertices()
        TOTAL_VERTICES = len(vertices)
        nodes: Dict[int, Type[Node]] = {}
        closed_nodes: Dict[str, Type[Node]] = {}

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
