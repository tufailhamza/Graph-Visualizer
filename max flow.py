import matplotlib.pyplot as plt
import networkx as nx
import random
from matplotlib.widgets import Button

class GraphVisualization:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.visual = []
        self.pos = nx.spring_layout(graph)
        self.source = source
        self.sink = sink
        self.node_colors = ['yellow' if node == source else 'green' if node == sink else 'lightblue' for node in graph.nodes()]
        self.next_button = Button(plt.axes([0.81, 0.01, 0.1, 0.04]), 'Next')
        self.next_button.on_clicked(self.next_button_callback)

    def add_edge(self, a, b, flow, residual):
        edge = (a, b, {'flow': flow, 'residual': residual})
        self.visual.append(edge)

    def visualize(self, path, max_flow):
        plt.clf() 
        node_colors = [self.node_colors[node] for node in self.graph.nodes()]

        nx.draw(self.graph, self.pos, with_labels=True, font_weight='bold', node_color=node_colors)

        edge_labels = {}
        for u, v, data in self.visual:
            edge_labels[(u, v)] = f'({data["flow"]}, {data["residual"]})'

        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels)

        augmented_graph = nx.DiGraph()
        augmented_graph.add_edges_from(self.visual)

        highlighted_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(augmented_graph, self.pos, edgelist=highlighted_edges, edge_color='r', width=2)

        plt.title(f"Max Flow: {max_flow}")
        plt.text(0.5, 1.05, f"Max Flow: {max_flow}", transform=plt.gca().transAxes, fontsize=12, horizontalalignment='center')
        plt.show()

    def next_button_callback(self, event):
        plt.close()  

class Graph:
    def __init__(self, graph):
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(len(graph)))
        for u, row in enumerate(graph):
            for v, capacity in enumerate(row):
                if capacity > 0:
                    self.graph.add_edge(u, v, capacity=capacity)

    def searching_algo_BFS(self, s, t, parent):
        visited = [False] * len(self.graph.nodes())
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v, data in self.graph[u].items():
                if visited[v] == False and data['capacity'] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

        return True if visited[t] else False

    def ford_fulkerson_visualize(self, source, sink):
        parent = [-1] * len(self.graph.nodes())
        max_flow = 0

        visualization = GraphVisualization(self.graph, source, sink)

        while self.searching_algo_BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            path = [s]

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s]['capacity'])
                s = parent[s]
                path.append(s)

            path.reverse()

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
             
                if self.graph.has_edge(u, v):
                    self.graph[u][v]['capacity'] -= path_flow
                    visualization.add_edge(u, v, path_flow, self.graph[u][v]['capacity'])
                else:
                    self.graph[v][u]['capacity'] += path_flow
                    visualization.add_edge(v, u, path_flow, self.graph[v][u]['capacity'])
                v = parent[v]

  
            visualization.visualize(path, max_flow)
            print(f"Nodes Sequence in Final Path: {path}")
            print(f"Edges Involved in Final Path: {[(path[i], path[i + 1]) for i in range(len(path) - 1)]}")

        return max_flow

def generate_random_graph(nodes, max_capacity):
    graph = [[0] * nodes for _ in range(nodes)]
    for i in range(nodes):
        for _ in range(random.randint(1,5 )):
            j = random.randint(0,  nodes- 1)
            if i != j:
                graph[i][j] = random.randint(0, max_capacity)
    return graph

def main():
    
    num_nodes = 40
    max_capacity = 15
    graph = generate_random_graph(num_nodes, max_capacity)

 
    g = Graph(graph)
    source = 0
    sink = num_nodes-1

    print("Max Flow: %d " % g.ford_fulkerson_visualize(source, sink))

if __name__ == "__main__":
    main()
