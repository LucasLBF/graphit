from entities.Graph import Graph
from pyvis.network import Network
from typing import Type

def pyvis_visualization(graph: Type[Graph]) -> None:
    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)

    for vertex in graph.get_vertices():
        n.add_node(vertex.id, label=vertex.id)
    
    for edge in graph.get_edges():
        n.add_edge(edge.first_vertex.id, edge.second_vertex.id, width=3, label=str(edge.weight) if edge.weight > 1 else None)
    
    n.write_html("graph.html", open_browser=True)


def pyvis_visualization_sssp(graph: Type[Graph], src_id: str, dest_id: str) -> None:

    shortest_path = graph.get_shortest_path(src_id, dest_id)

    n = Network(height="100vh", width="100%", bgcolor="#222222", font_color="white", directed=graph.is_directed)

    if not shortest_path:
        src_vertex = graph.check_if_vertex_exists(src_id)
        dest_vertex = graph.check_if_vertex_exists(dest_id)

        print(f"Nao existe caminho valido entre os vertices {src_vertex} e {dest_vertex}")
        for vertex in graph.get_vertices():
            is_highlighted = vertex.id in [src_id, dest_id]  
            n.add_node(vertex.id, label=vertex.id, color='#dc2f02' if is_highlighted else '#97c2fc')
    
        for edge in graph.get_edges():
            n.add_edge(edge.first_vertex.id,
                        edge.second_vertex.id,
                        color='#97c2fc',
                        label=str(edge.weight) if edge.weight > 1 else None)

    else:
        print("Menor caminho:", shortest_path["vertices"])
        print("Custo do menor caminho:", shortest_path["cost"])

        for vertex in graph.get_vertices():
            is_highlighted = vertex in shortest_path['vertices']
            n.add_node(vertex.id, label=str(vertex.id), color='#dc2f02' if is_highlighted else '#97c2fc')
    
        for edge in graph.get_edges():
            is_highlighted = edge in shortest_path['edges']
            n.add_edge(edge.first_vertex.id,
                        edge.second_vertex.id,
                        label=str(edge.weight) if edge.weight > 1 else None,
                        color='#dc2f02' if is_highlighted else '#97c2fc',
                        width=5 if is_highlighted else 2)
    

    n.write_html("graph.html", open_browser=True)