import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

NODES = 30

class GraphEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.calculate_button = tk.Button(root, text="Calculate SCCs", command=self.calculate_scc)
        self.calculate_button.pack(pady=10)

        self.generate_random_graph()
        self.draw_graph()

    def generate_random_graph(self):
        global NODES
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(NODES))

        for i in range(NODES):
            for _ in range(random.randint(1,3 )):  
                j = random.randint(0, NODES - 1)
                while i == j or self.graph.has_edge(i, j):  
                    j = random.randint(0, NODES - 1)
                self.graph.add_edge(i, j)

    def draw_graph(self):
        self.figure, self.ax = plt.subplots()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_color="gray", ax=self.ax)
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax)
        nx.draw_networkx_labels(self.graph, pos, ax=self.ax)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=tk.YES, fill=tk.BOTH)

    def draw_graph_with_colors(self, color_map):
            self.ax.clear()
            pos = nx.spring_layout(self.graph)
            nx.draw_networkx_nodes(self.graph, pos, node_color=color_map, ax=self.ax, cmap=plt.cm.rainbow)
            nx.draw_networkx_edges(self.graph, pos, ax=self.ax, edge_color='black')  # Change edge color to black
            nx.draw_networkx_labels(self.graph, pos, ax=self.ax)
            self.canvas.draw()


    def calculate_scc(self):
        sccs = self.tarjan_algorithm()
        print("Strongly Connected Components:", sccs)


        color_map = [-1] * NODES
        for i, scc in enumerate(sccs):
            for node in scc:
                color_map[node] = i + 1  #

        self.draw_graph_with_colors(color_map)

    def tarjan_algorithm(self):
        disc = [-1] * NODES
        low = [-1] * NODES
        stk_item = [False] * NODES
        stk = []
        sccs = []

        def find_component(u):
            nonlocal time
            time += 1
            disc[u] = low[u] = time
            stk.append(u)
            stk_item[u] = True

            for v in range(NODES):
                if self.graph.has_edge(u, v):
                    if disc[v] == -1:
                        find_component(v)
                        low[u] = min(low[u], low[v])
                    elif stk_item[v]:
                        low[u] = min(low[u], disc[v])

            popped_item = 0
            if low[u] == disc[u]:
                scc = []
                while stk[-1] != u:
                    popped_item = stk[-1]
                    scc.append(popped_item)
                    stk_item[popped_item] = False
                    stk.pop()
                popped_item = stk[-1]
                scc.append(popped_item)
                stk_item[popped_item] = False
                stk.pop()
                sccs.append(scc)

        time = 0
        for i in range(NODES):
            if disc[i] == -1:
                find_component(i)

        return sccs

if __name__ == "__main__":
    root = tk.Tk()
    graph_editor = GraphEditor(root)
    root.mainloop()
