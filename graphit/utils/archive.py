from graphit.entities.graph import Graph

def read_graph_file(fileName:str) -> Graph:
        graph = None
        with open("test_files/"+fileName, 'r') as file:
                directed = False
                valued_graph = False

                lines = file.readlines()

                graph_start = 0
                vertex_start = -1;

                for line in lines:
                        line = line.strip().upper()

                        if line.startswith('#') or line.strip() == "":
                                continue

                        if line.find("DIRECTED") != -1:
                                directed = line.split(':')[1].strip()

                        elif line.find("VALUED GRAPH") != -1:
                                valued_graph = line.split(':')[1].strip()

                        elif line.find("VERTEXS") != -1:
                                vertex_start = lines.index(line+"\n")+1;

                        elif line.find("GRAPH") != -1:
                                graph_start = lines.index(line+"\n")+1;
                                break
                
                graph = Graph(True if directed == "TRUE" else False)

                if (vertex_start != -1):
                        for line in lines[vertex_start:graph_start-1]:
                                line = line.strip()
                                if(not(line == "") and not line.startswith('#')): 
                                        graph.add_vertex(line.strip())

                                elif line == "":
                                        break

                for line in lines[graph_start:]:
                        line = line.strip()

                        if line.startswith('#'):
                                continue

                        if (valued_graph == "TRUE"):
                                
                                vertex1, vertex2, weight = list(map(lambda x: x.strip(), line.split(';')))
                                graph.add_edge(vertex1, vertex2, int(weight))
                        else:
                                vertex1, vertex2 = list(map(lambda x: x.strip(), line.split(';')))
                                graph.add_edge(vertex1, vertex2)

        return graph

def read_graph_uploaded_file(file: object) -> Graph:
        graph = None
        lines = ["\n".join(line.decode("utf-8").splitlines()) for line in file.readlines()]
        directed = False
        valued_graph = False

        graph_start = 0
        vertex_start = -1;

        for line in lines:
                line = line.strip().upper()

                if line.startswith('#') or line.strip() == "":
                        continue

                if line.find("DIRECTED") != -1:
                        directed = line.split(':')[1].strip()

                elif line.find("VALUED GRAPH") != -1:
                        valued_graph = line.split(':')[1].strip()

                elif line.find("VERTEXS") != -1:
                        vertex_start = lines.index(line)+1;

                elif line.find("GRAPH") != -1:
                        graph_start = lines.index(line)+1;
                        break
                
        graph = Graph(True if directed == "TRUE" else False)

        if (vertex_start != -1):
                for line in lines[vertex_start:graph_start-1]:
                        line = line.strip()
                        if(not(line == "") and not line.startswith('#')): 
                                graph.add_vertex(line.strip())

                        elif line == "":
                                break

        for line in lines[graph_start:]:
                line = line.strip()

                if line.startswith('#'):
                        continue

                if (valued_graph == "TRUE"):
                                
                        vertex1, vertex2, weight = list(map(lambda x: x.strip(), line.split(';')))
                        graph.add_edge(vertex1, vertex2, int(weight))
                else:
                        vertex1, vertex2 = list(map(lambda x: x.strip(), line.split(';')))
                        graph.add_edge(vertex1, vertex2)

        return graph