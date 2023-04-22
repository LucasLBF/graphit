from django.db import models
from abc import ABC, abstractmethod

from graphit.entities.vertex import Vertex
from graphit.entities.edge import Edge
from graphit.entities.errors import GraphCycleError, MultiEdgeError
from typing import Optional, Dict, List, Type
from graphit.entities.node import Node


class Graph():
    def __init__(self, is_directed):
        self.is_directed = is_directed
        self.vertices = []
        self.edges = []

    def set_djkstra_strategy(self, djkstra) -> None:
        self.djkstra_strategy = djkstra
    
    def get_shortest_path(self, src_vertex: str, dest_vertex: str) -> Dict:
        return self.djkstra_strategy.execute(src_vertex, dest_vertex)

    def get_edges(self) -> List[Type[Edge]]:
        '''Informa todas as arestas do grafo'''

        return self.edges
    
    def get_edge(self, dest_vertex: Type[Vertex], src_vertex: Type[Vertex]) -> Type[Edge]:
        '''Informa a aresta dados dois vertices. Primeiro vertice e o de destino,
        e o segundo e o de origem'''
        if self.is_directed:
            for edge in self.edges:
                    if (edge.second_vertex == dest_vertex and
                         edge.first_vertex == src_vertex):
                        return edge
        else:
            for edge in self.edges:
                if (edge.check_if_vertex_exists(src_vertex) and
                    edge.check_if_vertex_exists(dest_vertex)):
                    return edge

    
    def get_vertices(self) -> List[Type[Vertex]]:
        '''Informa todos os vertices do grafo'''

        return self.vertices
    
    def get_order(self) -> int:
        '''Informa a ordem do grafo'''

        return len(self.vertices)
    
    def get_size(self) -> int:
        '''Informa o tamanho do grafo'''

        return len(self.edges)

    def add_vertex(self, id: str) -> object:
        '''Dado um id, cria um vertice e o adiciona no grafo.'''
        new_vertex = Vertex(id)
        self.vertices.append(new_vertex)
        return new_vertex

    def check_if_vertex_exists(self, vertex_id: str) -> Optional[Type[Vertex]]:
        '''Dado um id, checar se o vertice ja existe no grafo'''
        
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex


    def add_edge(self,
                vertex_1: str,
                vertex_2: str,
                weight: int = 1) -> None:
        '''Adicionar uma aresta ao grafo. Essa classe foi escrita de forma que
        os vertices nao precisam ser adicionados individualmente, eles sao criados a medida
        que as arestas sao informadas. Ex.: a aresta (1 3) informada pelo usuario 
        cria os vertices 1 e 3 automaticamente se elas sao ja existirem no grafo'''

        if vertex_1 == vertex_2:
            raise GraphCycleError("O grafo deve ser simples. Retire o ciclo do grafo e tente novamente.")

        first_vertex = self.check_if_vertex_exists(vertex_1)
        second_vertex = self.check_if_vertex_exists(vertex_2)

        if not first_vertex:
            first_vertex = self.add_vertex(vertex_1)
        if not second_vertex:
            second_vertex = self.add_vertex(vertex_2)

        new_edge = Edge(first_vertex, second_vertex, self.is_directed, weight)
        self.validate_edge(new_edge)
        self.edges.append(new_edge)

    def validate_edge(self, new_edge: Type[Edge]) -> None:
        for edge in self.edges:
            if edge.is_parallel_edge(new_edge):
                raise MultiEdgeError(f"O grafo deve ser simples. Retire a aresta paralela {new_edge} e tente novamente")
    
    def get_neighbors(self,
                    vertex: Type[Vertex],
                    in_neighbors: bool = False,
                    out_neighbors: bool = False) -> Dict[str, Dict[str, List[object]]]:
        result = {}

        if self.is_directed:
            if in_neighbors:
                result['in_neighbors'] = self.get_in_neighbors(vertex)
            if out_neighbors:
                result['out_neighbors'] = self.get_out_neighbors(vertex)
            return result
        else:
            result['neighbors'] = self.get_neighbors_undirected(vertex)
        return result

    def get_in_neighbors(self, vertex: Type[Vertex]) -> List[Type[Vertex]]:
        '''Retorna uma lista de vizinhança de entrada (grafos direcionados)'''
        in_neighbors = {'vertices': [], 'edges': []}
        for edge in self.edges:
            if edge.is_directed and edge.second_vertex == vertex:
                in_neighbors["vertices"].append(edge.get_neighbor_vertex(vertex))
                in_neighbors["edges"].append(edge)
        return in_neighbors

    def get_out_neighbors(self, vertex: Type[Vertex]) -> Dict:
        '''Retorna uma lista de vizinhança de saida (grafos direcionados)'''
        out_neighbors = {'vertices': [], 'edges': []}
        for edge in self.edges:
            if edge.is_directed and edge.first_vertex == vertex:
                out_neighbors["vertices"].append(edge.get_neighbor_vertex(vertex))
                out_neighbors["edges"].append(edge)
        return out_neighbors
    
    def get_neighbors_undirected(self, vertex: Type[Vertex]) -> Dict:
        '''Retorna uma lista de vizinhança (grafos nao direcionados)'''
        neighbors = {'vertices': [], 'edges': []}
        for edge in self.edges:
            if edge.check_if_vertex_exists(vertex):
                neighbors['vertices'].append(edge.get_neighbor_vertex(vertex))
                neighbors['edges'].append(edge)
        return neighbors
                
    def get_vertex_degree(self, vertex_id: str) -> Dict:
        neighbors = self.get_neighbors(self.check_if_vertex_exists(vertex_id), True, True)

        if self.is_directed:
            return {"in_degree": len(neighbors["in_neighbors"]["vertices"]),
                    "out_degree": len(neighbors["out_neighbors"]["vertices"])}
        
        return {"degree": len(neighbors["neighbors"]["vertices"])}
            
    def are_vertices_adjacent(self, vertex_id_1: str, vertex_id_2: str) -> bool:
        neighbors = self.get_neighbors(self.check_if_vertex_exists(vertex_id_1), True, True)
        vertex_2 = self.check_if_vertex_exists(vertex_id_2)

        if self.is_directed:
            neighbors_in = neighbors["in_neighbors"]["vertices"]
            neighbors_out = neighbors["out_neighbors"]["vertices"]
            return (vertex_2 in neighbors_in) or (vertex_2 in neighbors_out)
        
        return vertex_2 in neighbors["neighbors"]["vertices"]
        
    
    # def get_neighbors_edges(self, vertex: Type[Vertex]) -> List[Type[Edge]]:
    #     neighbors = []
    #     for edge in self.edges:
    #         if edge.check_if_vertex_exists(vertex):
    #             neighbors.append(edge)
        
    #     return neighbors

    def eccentricity(self, vertex_src: Type[Vertex]) -> int:
        '''Recebe o vertice o qual se deseja a excentricidade'''
        djkstra_costs = [node.cost for _, node in self.djkstra_strategy.djkstra_algorithm(vertex_src.id).items()]

        biggest_path = sorted(djkstra_costs)[-1]
        
        return biggest_path

    def get_radius_diameter(self) -> Dict:
        '''Retorna um dicionario contendo o raio e o diametro do grafo'''
        eccentricities = list(map(lambda vertex_src: self.eccentricity(vertex_src), self.get_vertices()))

        eccentricities.sort()

        radius = eccentricities[0]
        diameter = eccentricities[-1]

        result = {"radius": radius, "diameter": diameter}
        return result

    def __repr__(self) -> str:
        '''Mostra o grafo como uma matrix de adjacencia usando o print().
        Por enquanto so funciona com grafos nao direcionados.'''
        adjacency_matrix = []
        sorted_vertices = sorted(self.vertices)
        if self.is_directed:
            for row in sorted_vertices:
                vertex_edges = []
                vertex_neighbors = self.get_neighbors(row, out_neighbors=True)['out_neighbors']['vertices']
                for column in sorted_vertices:
                    vertex_edges.append(1 if column in vertex_neighbors else 0)
                adjacency_matrix.append(vertex_edges)
        else:
            for row in sorted_vertices:
                vertex_edges = []
                vertex_neighbors = self.get_neighbors(row)['neighbors']['vertices']
                for column in sorted_vertices:
                    vertex_edges.append(1 if column in vertex_neighbors else 0)
                adjacency_matrix.append(vertex_edges)
            
        matrix_string = ""
        for i in range(len(adjacency_matrix)): 
            matrix_string += str(sorted_vertices[i]) + "\t" + "  ".join(str(n) for n in adjacency_matrix[i]) + "\n"

        return matrix_string
