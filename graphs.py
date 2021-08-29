class Edge:
    def __init__(self, start, end, time):
        self.start = start
        self.end = end
        self.time = time 
    
    def getTime(self):
        return self.time

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def __repr__(self):
                return "Go from " + self.start.getName() + " to " + self.end.getName() + " (takes about " + str(self.getTime()) + ")."

# These are the machines (or the Nodes in the Graph). 
# You can add whatever fields/methods
class Vertex:
    def __init__(self, name, days_left):
        # For the use in Flask, these names must be unique
        self.name = name
        self.days_left = days_left

    def __repr__(self):
        return self.name

    def getName(self):
        return self.name

    def getDaysLeft(self):
        return self.days_left

class Graph:
    def __init__(self, nodes, edges):
        self.edges = {node: [] for node in nodes}
        self.list_of_edges = []
        for fromVertex in nodes:
            for toVertex in edges[fromVertex]:
                if (toVertex in nodes):
                    self.edges[fromVertex].append(Edge(fromVertex, toVertex, edges[fromVertex][toVertex]))
                    self.list_of_edges.append(Edge(fromVertex, toVertex, edges[fromVertex][toVertex]))

                    self.edges[toVertex].append(Edge(toVertex, fromVertex, edges[fromVertex][toVertex]))
                    self.list_of_edges.append(Edge(toVertex, toVertex, edges[fromVertex][toVertex]))

        self.nodes = nodes
        self.min_tree = self.kruskals()

    def find(self, reps, node):
        if (reps[node] == node):
            return node
        else:
            return self.find(reps, reps[node])

    # TODO: The below algorithm is okay, but it would be a lot better if you used a modified k-opt approach. 
    # (I didn't have time to implement it, however).

    # Creates a min spanning tree according to a modified Kruskals algorithm that doesn't allow for
    # one edge to have more than 2 edges.
    def kruskals(self):
        worklist = sorted(self.list_of_edges, key=lambda i: i.getTime()) 
        output = {node: [] for node in self.nodes}

        reps = {node: node for node in self.nodes} 

        while (len(worklist) > 0):

            cur = worklist.pop(0)

            creates_cycle = self.find(reps, cur.getStart()) == self.find(reps, cur.getEnd())
            edge = max(len(output[cur.getStart()]), len(output[cur.getEnd()]))

            if (not creates_cycle and edge < 2):
                output[cur.getStart()].append(cur)
                # Assume that A->B takes the same amount of time as B->A
                output[cur.getEnd()].append(Edge(cur.getEnd(), cur.getStart(), cur.getTime()))

            if (edge < 2):
                reps[self.find(reps, cur.getStart())] = self.find(reps, cur.getEnd())
        return output
    
    def get_total_time(self):
        total = 0
        for edge in self.optimize_path():
            total += edge.getTime()
        return total

    def optimize_path(self):
        output = []
        curVertex = None
        prevVertex = None
        for node in self.min_tree:
            if (len(self.min_tree[node]) == 1):
                output.append(self.min_tree[node][0])
                prevVertex = node
                curVertex = self.min_tree[node][0].getEnd()
                break
        
        while(len(self.min_tree[curVertex]) == 2):
            index = 0
            if (self.min_tree[curVertex][0].getEnd() == prevVertex):
                index = 1
            
            output.append(self.min_tree[curVertex][index])
            prevVertex = curVertex
            curVertex = self.min_tree[curVertex][index].getEnd()

        return output

if __name__ == "__main__":
    v1 = Vertex("Location 1", 5)
    v2 = Vertex("Location 2", 15)
    v3 = Vertex("Location 3", 20)
    v4 = Vertex("Location 4", 3)
    v5 = Vertex("Location 5", 7)
    v6 = Vertex("Location 6", 8)
    all_units = [v1, v2, v3, v4, v5, v6]
    map_of_name = {node.getName(): node for node in all_units}
    distance_matrix = {
        v1: {v2: 1, v3: 4, v4: 1, v5: 3, v6: 6},
        v2: {v3:3, v4: 2, v5: 2, v6: 7},
        v3: {v4: 3, v5: 2, v6: 6},
        v4: {v5: 1, v6: 6},
        v5: {v6: 5},
        v6: {}
    }

    print(Graph(all_units, distance_matrix).get_total_time())