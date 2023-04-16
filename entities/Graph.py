from entities.Vertex import Vertex
from entities.Edge import Edge
from entities.errors import GraphCycleError, MultiEdgeError
from typing import Optional, Dict, List, Type
from entities.Node import Node
class Graph():
    def __init__(self, is_directed):
        self.is_directed = is_directed
        self.vertices = []
        self.edges = []

    # def set_shortest_path_strategy(self, strategy: object) -> None:
    #     '''Determina qual algoritmo de menor caminho sera utilizado pelo grafo.
    #     Aceita um objeto Strategy'''
    #     self.strategy = strategy

    def set_djkstra_strategy(self, djkstra) -> None:
        self.djkstra_strategy = djkstra
    
    def get_shortest_path(self, src_vertex: int, dest_vertex: int) -> Dict:
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
                    # out_neighbors: bool = False) -> Dict[str, List[Type[Vertex]]]:
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
        # neighbors = []
        neighbors = {'vertices': [], 'edges': []}
        for edge in self.edges:
            if edge.check_if_vertex_exists(vertex):
                neighbors['vertices'].append(edge.get_neighbor_vertex(vertex))
                neighbors['edges'].append(edge)
        return neighbors
                
    def get_vertex_degree(self, vertex_id:int) -> Dict:
        neighbors = self.get_neighbors(self.check_if_vertex_exists(vertex_id), True, True)

        if self.is_directed:
            return {"in_degree": len(neighbors.get("in_neighbors")),
                    "out_degree": len(neighbors.get("out_neighbors"))}
        
        return {"degree": len(neighbors.get("neighbors"))}
            
    def is_vertexs_adjacent(self, vertex_id_1:int, vertex_id_2:int) -> bool:
        neighbors = self.get_neighbors(self.check_if_vertex_exists(vertex_id_1), True, True)
        vertex_2 = self.check_if_vertex_exists(vertex_id_2)

        if self.is_directed:
            neighbors_in = neighbors.get("in_neighbors")
            neighbors_out = neighbors.get("out_neighbors")
            return (vertex_2 in neighbors_in) or (vertex_2 in neighbors_out)
        
        return vertex_2 in neighbors.get("neighbors")
        
    
    def get_neighbors_edges(self, vertex: Type[Vertex]) -> List[Type[Edge]]:
        neighbors = []
        for edge in self.edges:
            if edge.check_if_vertex_exists(vertex):
                neighbors.append(edge)
        
        return neighbors

    
    def excentricidade(self, vertex_src: Vertex) -> int:
        '''Recebe o vertice o qual se deseja a excentricidade'''
        biggest_path = -1

        djkstra: List[Type[Node]] = self.djkstra_strategy.djkstra_undirected(vertex_src.get_id())

        biggest_path = sorted(djkstra)[-1].get_cost()
        
        return biggest_path

    def get_raio_diametro(self) -> Dict:
        '''Retorna um dicionario contendo o raio e o diametro do grafo'''
        raio = -1
        diametro = -1

        exentricidades = list(map(lambda vertex_src: self.excentricidade(vertex_src), self.get_vertices()))

        exentricidades.sort()

        raio = exentricidades[0]
        diametro = exentricidades[-1]

        result = {"raio": raio, "diametro": diametro}
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
