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

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        requested_nodes = list(map(lambda x: map_of_name[x], request.form.getlist('check')))
        if (len(requested_nodes) < 2):
            time = 0
            path = ["No path necessary"]
        else:
            graph = Graph(requested_nodes, edges)
            min_spanning = graph.create_min_spanning_tree()

            time = graph.get_total_time(min_spanning)
            path = graph.optimize_path(min_spanning)
            if (len(path) != len(requested_nodes) - 1):
                time = 0
                path = ["Could not complete path"]
        
        return render_template('index.html', units=all_units, checked=requested_nodes, time=time, path=path)
    return render_template('index.html', units=all_units, checked=[], time=0, path=["Press the Update Path button for a solution."])

if __name__ == "__main__":
    v1 = Vertex("Location 1")
    v2 = Vertex("Location 2")
    v3 = Vertex("Location 3")
    v4 = Vertex("Location 4")
    v5 = Vertex("Location 5")
    v6 = Vertex("Location 6")
    all_units = [v1, v2, v3, v4, v5, v6]
    map_of_name = {node.getName(): node for node in all_units}
    edges = {
        v1: {v2: 2, v3: 1, v4: 7, v5: 3, v6: 6},
        v2: {v3:4, v4: 5, v5: 4, v6: 7},
        v3: {v4: 6, v5: 2, v6: 8},
        v4: {v5: 11, v6: 5},
        v5: {v6: 2},
        v6: {}
    }

    app.run(debug=True)
