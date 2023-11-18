import networkx as nx
import time


clock_in = time.time_ns()
graph: nx.Graph = nx.grid_2d_graph(11, 11)
graph: nx.Graph = nx.grid_2d_graph(11, 11)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

clock_in = time.time_ns()
graph: nx.Graph = nx.grid_2d_graph(11, 11)
graph2 = graph.copy()
for i in range(6):
    graph2.remove_node((i, i))
    graph2.add_node((i, i))
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")