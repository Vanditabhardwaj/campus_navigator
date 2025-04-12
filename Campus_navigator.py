import networkx as nx
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Graph setup
campus = nx.Graph()
campus.add_edges_from([
    ('Library', 'Canteen', {'weight': 5}),
    ('Library', 'Admin Block', {'weight': 2}),
    ('Admin Block', 'Hostel', {'weight': 3}),
    ('Canteen', 'Hostel', {'weight': 6}),
    ('Hostel', 'Auditorium', {'weight': 8}),
    ('E-Block', 'Admin Block', {'weight': 4})
])

locations = list(campus.nodes)

def dfs_path(graph, start, goal):
    try:
        return list(nx.dfs_edges(graph, start))
    except Exception:
        return None

def bfs_path(graph, start, goal):
    try:
        return list(nx.bfs_edges(graph, start))
    except Exception:
        return None

def a_star_path(graph, start, goal):
    try:
        return nx.astar_path(graph, start, goal, weight='weight')
    except Exception:
        return None

# Placeholder AO* and Hill Climbing
def ao_star_path(graph, start, goal):
    # Custom implementation needed
    return nx.shortest_path(graph, start, goal, weight='weight')  # placeholder

def hill_climbing_path(graph, start, goal):
    try:
        # Greedy best-first based on direct edge weight (not optimal, but demo-friendly)
        current = start
        path = [current]
        visited = set()
        while current != goal:
            visited.add(current)
            neighbors = [(n, graph[current][n]['weight']) for n in graph.neighbors(current) if n not in visited]
            if not neighbors:
                return None
            current = min(neighbors, key=lambda x: x[1])[0]
            path.append(current)
        return path
    except Exception:
        return None

# Visualize the graph
def draw_graph(path=None):
    pos = nx.spring_layout(campus)
    edge_labels = nx.get_edge_attributes(campus, 'weight')

    plt.figure(figsize=(8, 6))
    nx.draw(campus, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(campus, pos, edge_labels=edge_labels)

    if path:
        edge_path = list(zip(path, path[1:]))
        nx.draw_networkx_edges(campus, pos, edgelist=edge_path, width=3, edge_color='red')
        nx.draw_networkx_nodes(campus, pos, nodelist=path, node_color='lime')

    plt.title("Campus Map with Path")
    plt.show()

# GUI setup
app = tk.Tk()
app.title("✨ Campus Navigator ✨")
app.geometry("430x370")
app.configure(bg="#F0F8FF")

title = tk.Label(app, text="Campus Navigator", font=("Arial", 20, "bold"), bg="#F0F8FF", fg="#4B0082")
title.pack(pady=10)

frame = tk.Frame(app, bg="#F0F8FF")
frame.pack(pady=10)

# Start location
tk.Label(frame, text="From:", font=("Arial", 12), bg="#F0F8FF").grid(row=0, column=0, padx=10, pady=5)
start_var = tk.StringVar()
start_dropdown = ttk.Combobox(frame, textvariable=start_var, values=locations, state="readonly")
start_dropdown.grid(row=0, column=1)

# End location
tk.Label(frame, text="To:", font=("Arial", 12), bg="#F0F8FF").grid(row=1, column=0, padx=10, pady=5)
end_var = tk.StringVar()
end_dropdown = ttk.Combobox(frame, textvariable=end_var, values=locations, state="readonly")
end_dropdown.grid(row=1, column=1)

# Algorithm selection
tk.Label(frame, text="Algorithm:", font=("Arial", 12), bg="#F0F8FF").grid(row=2, column=0, padx=10, pady=5)
algo_var = tk.StringVar()
algo_dropdown = ttk.Combobox(frame, textvariable=algo_var, values=["DFS", "BFS", "A*", "AO*", "Hill Climbing"], state="readonly")
algo_dropdown.grid(row=2, column=1)

# Result label
result_label = tk.Label(app, text="", font=("Arial", 12), wraplength=380, bg="#F0F8FF", fg="#333")
result_label.pack(pady=10)

def show_path():
    start = start_var.get()
    end = end_var.get()
    algo = algo_var.get()

    if not start or not end or not algo:
        messagebox.showwarning("Input Missing", "Please select all options!")
        return

    if start == end:
        messagebox.showinfo("Same Locations", "Start and destination are the same!")
        return

    if algo == "DFS":
        edges = dfs_path(campus, start, end)
        path = [start]
        for u, v in edges:
            if v == end:
                path.append(v)
                break
            if v not in path:
                path.append(v)
    elif algo == "BFS":
        edges = bfs_path(campus, start, end)
        path = [start]
        for u, v in edges:
            if v == end:
                path.append(v)
                break
            if v not in path:
                path.append(v)
    elif algo == "A*":
        path = a_star_path(campus, start, end)
    elif algo == "AO*":
        path = ao_star_path(campus, start, end)
    elif algo == "Hill Climbing":
        path = hill_climbing_path(campus, start, end)
    else:
        path = None

    if path:
        distance = 0
        try:
            distance = sum([campus[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)])
        except:
            pass
        result_label.config(text=f"Path: {' → '.join(path)}\nTotal Distance: {distance} units")
        draw_graph(path)
    else:
        messagebox.showerror("No Path", f"No path found using {algo} algorithm!")

# Button
find_btn = tk.Button(app, text="Find Path", command=show_path, bg="#9370DB", fg="white", font=("Arial", 12), relief="raised")
find_btn.pack(pady=10)

app.mainloop()



"""
tnr- font

title - 14 +bold
all other text - 12
heading - 12 + bold
layout margin - standard
page no. - right bottom
alignment - title(center)   text(justified)
paragraph - line spacing (1.5) others (0)  space after(6 )
"""