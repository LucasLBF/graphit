from entities.Graph import Graph

def readGraphFile(fileName:str) -> Graph:
        with open(fileName, 'r') as file:
                directed = False
                valuedGraph = False
                vertexAmount = 0;

                lines = file.readlines()
                graphStart = 0
                for line in lines:
                        line = line.strip().upper()

                        if line.startswith('#'):
                                continue

                        if line.find("VERTEX") != -1:
                                vertexAmount = int(line.split(':')[1].strip())

                        elif line.find("DIRECTED") != -1:
                                directed = line.split(':')[1].strip()

                        elif line.find("VALUED GRAPH") != -1:
                                edgesAmount = line.split(':')[1].strip()

                        elif line.find("GRAPH") != -1:
                                graphStart = lines.index(line);
                                break
                
                graph = Graph(directed)
                for line in lines[graphStart:]:
                        if line.startswith('#'):
                                continue

                        vertex1, vertex2, weight = 0

                        if (valuedGraph):
                                vertex1, vertex2, weight = line.split("       ")
                                graph.add_edge(vertex1, vertex2, weight)
                        else:
                                vertex1, vertex2 = line.split("       ")
                                graph.add_edge(vertex1, vertex2)

                        

                        

                        




