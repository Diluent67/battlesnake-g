import networkx as nx
import time


clock_in = time.time_ns()
graph: nx.Graph = nx.grid_2d_graph(11, 11)
graph: nx.Graph = nx.grid_2d_graph(11, 11)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

clock_in = time.time_ns()
G: nx.Graph = nx.grid_2d_graph(11, 11)
for i in range(6):
    G.remove_node((i, i))
    G.add_node((i, i))
    x, y = i, i
    possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for e in possible_edges:
        if e in G.nodes:
            G.add_edge(i, e)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

