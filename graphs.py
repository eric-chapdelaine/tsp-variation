class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

    def getWeight(self):
        return self.weight

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def __repr__(self):
        return "Go from " + self.start.getName() + " to " + self.end.getName() + " (takes about " + str(self.weight) + ")."

# These are the machines (or the Nodes in the Graph). 
# You can add whatever fields/methods
class Vertex:
    def __init__(self, name):
        # For the use in Flask, these names must be unique
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self):
        return self.name

class Graph:
    def __init__(self, nodes, edges):
        self.edges = {}
        self.list_of_edges = []
        for fromVertex in nodes:
            cur = {}
            for toVertex in edges[fromVertex]:
                if (toVertex in nodes):
                    curWeight = edges[fromVertex][toVertex]
                    cur[toVertex] = curWeight 
                    self.list_of_edges.append(Edge(fromVertex, toVertex, curWeight))
            self.edges[fromVertex] = cur

        self.nodes = nodes

    def add_edge(self, node, edge):
        self.list_of_edges.append(edge)
        self.edges[node].append(edge)

    def add_node(self, node, dic):
        self.nodes.append(node)
        self.edges[node] = []
        for other in dic:
            e  = Edge(node, other, dic[other])
            self.edges[node].append(e)
            self.list_of_edges.append(e)

    def find(self, reps, node):
        if (reps[node] == node):
            return node
        else:
            return self.find(reps, reps[node])
    

    # Uses a modified version of Kruskal's algorithm to generate minimum spanning tree with no
    # nodes having two (or more) edges
    def create_min_spanning_tree(self):
        worklist = sorted(self.list_of_edges, key=lambda i: i.getWeight()) 
        output = {node: [] for node in self.nodes}

        reps = {node: node for node in self.nodes} 

        while (len(worklist) > 0):

            cur = worklist.pop(0)

            creates_cycle = self.find(reps, cur.getStart()) == self.find(reps, cur.getEnd())
            edge = max(len(output[cur.getStart()]), len(output[cur.getEnd()]))

            if (not creates_cycle and edge < 2):
                output[cur.getStart()].append(cur)
                # Assume that A->B takes the same amount of time as B->A
                output[cur.getEnd()].append(Edge(cur.getEnd(), cur.getStart(), cur.getWeight()))

            if (edge < 2):
                reps[self.find(reps, cur.getStart())] = self.find(reps, cur.getEnd())

        return output

    def get_total_time(self, dict):
        total = 0
        for edge in self.optimize_path(dict):
            total += edge.getWeight()
        return total

    def optimize_path(self, dict):

        output = []
        curVertex = None
        prevVertex = None
        for node in dict:
            if (len(dict[node]) == 1):
                output.append(dict[node][0])
                prevVertex = node
                curVertex = dict[node][0].getEnd()
                break
        
        while(len(dict[curVertex]) == 2):
            index = 0
            if (dict[curVertex][0].getEnd() == prevVertex):
                index = 1
            
            output.append(dict[curVertex][index])
            prevVertex = curVertex
            curVertex = dict[curVertex][index].getEnd()

        return output