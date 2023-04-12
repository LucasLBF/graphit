from entities.Vertex import Vertex
from entities.Edge import Edge
from entities.errors import GraphCycleError, MultiEdgeError
from typing import Optional, Dict, List, Type

class Graph():
    def __init__(self, is_directed):
        self.is_directed = is_directed
        self.vertices = []
        self.edges = []

    def get_edges(self) -> List[Type[Edge]]:
        '''Informa todas as arestas do grafo'''

        return self.edges
    
    def get_vertices(self) -> List[Type[Vertex]]:
        '''Informa todos os vertices do grafo'''

        return self.vertices
    
    def get_order(self) -> int:
        '''Informa a ordem do grafo'''

        return len(self.vertices)
    
    def get_size(self) -> int:
        '''Informa o tamanho do grafo'''

        return len(self.edges)

    def add_vertex(self, id: int) -> object:
        '''Dado um id, cria um vertice e o adiciona no grafo.'''
        new_vertex = Vertex(id)
        self.vertices.append(new_vertex)
        return new_vertex

    def check_if_vertex_exists(self, vertex_id: int) -> Optional[Type[Vertex]]:
        '''Dado um id, checar se o vertice ja existe no grafo'''
        
        for vertex in self.vertices:
            if vertex.id == vertex_id:
                return vertex


    def add_edge(self,
                vertex_1: int,
                vertex_2: int,
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
                raise MultiEdgeError("O grafo deve ser simples. Retire a aresta paralela e tente novamente")
    
    def get_neighbors(self,
                    vertex: Type[Vertex],
                    in_neighbors: bool = False,
                    out_neighbors: bool = False) -> Dict[str, List[Type[Vertex]]]:
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
        in_neighbors = []
        for edge in self.edges:
            if edge.is_directed and edge.second_vertex == vertex:
                in_neighbors.append(edge.get_neighbor_vertex(vertex))
        return in_neighbors

    def get_out_neighbors(self, vertex: Type[Vertex]) -> List[Type[Vertex]]:
        '''Retorna uma lista de vizinhança de saida (grafos direcionados)'''
        out_neighbors = []
        for edge in self.edges:
            if edge.is_directed and edge.first_vertex == vertex:
                out_neighbors.append(edge.get_neighbor_vertex(vertex))
        return out_neighbors
    
    def get_neighbors_undirected(self, vertex: Type[Vertex]) -> List[Type[Vertex]]:
        '''Retorna uma lista de vizinhança (grafos nao direcionados)'''
        neighbors = []
        for edge in self.edges:
            if edge.check_if_vertex_exists(vertex):
                neighbors.append(edge.get_neighbor_vertex(vertex))
        return neighbors
    
    def get_neighbors_edges(self, vertex: Type) -> List[Type[Edge]]:
        neighbors = []
        for edge in self.edges:
            if edge.check_if_vertex_exists(vertex):
                neighbors.append(edge)
        return neighbors

    def __repr__(self) -> str:
        '''Mostra o grafo como uma matrix de adjacencia usando o print().
        Por enquanto so funciona com grafos nao direcionados.'''
        adjacency_matrix = []
        sorted_vertices = sorted(self.vertices)
        if self.is_directed:
            for row in sorted_vertices:
                vertex_edges = []
                vertex_neighbors = self.get_neighbors(row, out_neighbors=True)
                for column in sorted_vertices:
                    vertex_edges.append(1 if column in vertex_neighbors['out_neighbors'] else 0)
                adjacency_matrix.append(vertex_edges)
        else:
            for row in sorted_vertices:
                vertex_edges = []
                vertex_neighbors = self.get_neighbors(row)
                for column in sorted_vertices:
                    vertex_edges.append(1 if column in vertex_neighbors['neighbors'] else 0)
                adjacency_matrix.append(vertex_edges)
            
        matrix_string = ""
        for i in range(len(adjacency_matrix)): 
            matrix_string += str(sorted_vertices[i]) + "\t" + "  ".join(str(n) for n in adjacency_matrix[i]) + "\n"

        return matrix_string
