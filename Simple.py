import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def is_valid_degree_sequence_havel_hakimi(deg_sequence):
    step = 0
    steps_info = []

    while deg_sequence:
        step += 1
        steps_info.append(f"Step {step}: Degree sequence: {deg_sequence}")

        if deg_sequence[0] < 0:
            return False, steps_info  

        if deg_sequence[0] == 0:
            deg_sequence.pop(0)  
        else:
            k = deg_sequence[0]
            if len(deg_sequence) < k + 1:
                return False, steps_info  
            for i in range(1, k + 1):
                deg_sequence[i] -= 1
            deg_sequence.pop(0)  

        deg_sequence = sorted(deg_sequence, reverse=True)

    return True, steps_info  

class GraphDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Drawer")

        self.G = nx.Graph()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.add_edge_button = tk.Button(root, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(side=tk.BOTTOM)

        self.submit_button = tk.Button(root, text="Submit", command=self.show_info)
        self.submit_button.pack(side=tk.BOTTOM)

        self.apply_havel_button = tk.Button(root, text="Apply Havel–Hakimi", command=self.apply_havel)
        self.apply_havel_button.pack(side=tk.BOTTOM)
        
        self.start_node = None
        self.add_edge_mode = False

        self.draw_graph()

    def on_click(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            if not self.add_edge_mode:
                node_label = len(self.G.nodes) + 1
                self.G.add_node(node_label, pos=(x, y))
                self.draw_graph()

    def add_edge(self):
        if len(self.G.nodes) < 2:
            messagebox.showwarning("Warning", "You need at least two nodes to add an edge.")
            return

        if not self.add_edge_mode:
            self.add_edge_mode = True
            messagebox.showinfo("Info", "Click on two nodes to add an edge.")
            self.canvas.mpl_disconnect('button_press_event')
            self.canvas.mpl_connect('button_press_event', self.on_click_edge)

    def on_click_edge(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            node = self.find_nearest_node((x, y))
            if node is not None:
                if self.start_node is None:
                    self.start_node = node
                else:
                    if self.start_node != node: 
                        self.G.add_edge(self.start_node, node)
                        self.start_node = None
                        self.draw_graph()
                    else:
                        messagebox.showwarning("Warning", "You cannot add a loop (edge connecting a node to itself).")


    def find_nearest_node(self, target_point):
        distances = [(node, (pos[0] - target_point[0])**2 + (pos[1] - target_point[1])**2) for node, pos in self.G.nodes(data='pos')]
        if distances:
            min_distance_node = min(distances, key=lambda x: x[1])[0]
            return min_distance_node
        return None

    def show_info(self):
        edges = list(self.G.edges())
        degree_sequence = list(dict(self.G.degree()).values())
        info_message = f"The edges are: {edges}\nDegree sequence: {degree_sequence}"
        messagebox.showinfo("Edges and Degree Sequence", info_message)

    def apply_havel(self):
        degree_sequence = list(dict(self.G.degree()).values())

        is_valid, steps_info = is_valid_degree_sequence_havel_hakimi(degree_sequence)
        steps_message = "\n\n".join(steps_info)
        if is_valid:
            messagebox.showinfo("Havel–Hakimi", f"The degree sequence is valid for a simple graph.\n\n{steps_message}")
        else:
            messagebox.showinfo("Havel–Hakimi", f"The degree sequence is not valid for a simple graph.\n\n{steps_message}")

    def apply_sorted_havel(self):
        degree_sequence = list(dict(self.G.degree()).values())
        sorted_degree_sequence = sorted(degree_sequence, reverse=True)

        is_valid, steps_info = is_valid_degree_sequence_havel_hakimi(sorted_degree_sequence)
        steps_message = "\n\n".join(steps_info)
        if is_valid:
            messagebox.showinfo("Sorted Havel–Hakimi", f"The sorted degree sequence is valid for a simple graph.\n\n{steps_message}")
        else:
            messagebox.showinfo("Sorted Havel–Hakimi", f"The sorted degree sequence is not valid for a simple graph.\n\n{steps_message}")

    def draw_graph(self):
        self.ax.clear()

        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw(self.G, pos, with_labels=True, node_size=700, font_size=10, font_color='black', font_weight='bold')

        self.ax.set_title("Graph")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawer(root)
    root.mainloop()
