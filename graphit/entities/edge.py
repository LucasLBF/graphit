from typing import Type
from graphit.entities.vertex import Vertex
from typing import Optional, Dict, List, Type

class Edge():
    '''Quando a aresta e direcionada (arco), first_vertex e o vertice de
    partida e second_vertex e o vertice de entrada'''
    def __init__(self,
                vertex_1: Type[Vertex],
                vertex_2: Type[Vertex],
                is_directed: bool = False,
                weight: int = 1):
        self.is_directed = is_directed
        self.first_vertex = vertex_1
        self.second_vertex = vertex_2
        self.weight = weight
    
    def get_weight(self) -> int:
        '''Retorna o peso da aresta'''
       
        return self.weight
    
    def get_vertex(self) -> List[Type[Vertex]]:
        '''Retorna a lista dos dois vertices da aresta'''
        return [self.first_vertex, self.second_vertex]

    def check_if_vertex_exists(self, vertex: Type[Vertex]) -> bool:
        '''Dado um vertice, verifica se ele esta incluso nessa aresta'''
        return vertex == self.first_vertex or vertex == self.second_vertex
    
    def get_neighbor_vertex(self, vertex: Type[Vertex]) -> Type[Vertex]:
        '''Dado um vertice, retorna o outro vertice que 
        compartilha essa aresta'''
        if vertex == self.first_vertex:
            return self.second_vertex
        elif vertex == self.second_vertex:
            return self.first_vertex
    
    def is_parallel_edge(self, new_edge: 'Edge') -> bool:
        if self.is_directed:
            if (self.first_vertex == new_edge.first_vertex and 
                self.second_vertex == new_edge.second_vertex):
                return True
        else:
            if (self.check_if_vertex_exists(new_edge.first_vertex) and
                self.check_if_vertex_exists(new_edge.second_vertex)):
                return True
        
        return False
    
    def __repr__(self):
        if self.is_directed:
            return f"(Aresta {self.first_vertex} -> {self.second_vertex})"
        else:
            return f"(Aresta {self.first_vertex} - {self.second_vertex})"