from flask import (
    Flask,
    render_template,
    request,
)

from graphs import (
    Vertex,
    Graph,
)

app = Flask(__name__)

@app.route('/')
def index():
    priority = sorted(all_units, key=lambda x: x.getDaysLeft())
    return render_template("index.html", units=priority)

@app.route("/create-path/<start>", methods=['GET', 'POST'])
def createPath(start):
    start_node = map_of_name[start]
    available_nodes = [node for node in all_units if node != start_node]
    if request.method == 'POST':
        requested_nodes = list(map(lambda x: map_of_name[x], request.form.getlist('check')))
        requested_nodes.append(start_node)
        if (len(requested_nodes) < 2):
            time = 0
            path = ["No path necessary"]
        else:
            graph = Graph(requested_nodes, distance_matrix)
            path = graph.optimize_path()
            time = graph.get_total_time()
            if (len(path) != len(requested_nodes) - 1):
                time = 0
                path = ["Could not complete path"]
        addition_of_others = {node: Graph([node] + requested_nodes, distance_matrix).get_total_time()-time for node in available_nodes}
    else:
        addition_of_others = {node: Graph([node, start_node], distance_matrix).get_total_time() for node in available_nodes}
        time = 0
        path=["Press the Update Path button for a solution."]
        requested_nodes = []
    sorted_by_distance = sorted(available_nodes, key=lambda x: addition_of_others[x]*x.getDaysLeft())
    return render_template('create-path.html', time_others=addition_of_others, start=start_node, units=sorted_by_distance, checked=requested_nodes, time=time, path=path)


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

    app.run(debug=True)