class Edge():
    def __init__(self, vertex_1, vertex_2, is_directed = False , weight = 1):
        self.is_directed = is_directed
        self.first_vertex = vertex_1
        self.second_vertex = vertex_2
        self.weight = weight
    
    def check_if_vertex_exists(self, vertex) -> bool:
        '''Dado um vertice, verifica se ele esta incluso nessa aresta'''
        return vertex == self.first_vertex or vertex == self.second_vertex
    
    def get_neighbor_vertex(self, vertex):
        '''Dado um vertice, retorna o outro vertice que 
        compartilha essa aresta'''
        if vertex == self.first_vertex:
            return self.second_vertex
        elif vertex == self.second_vertex:
            return self.first_vertex