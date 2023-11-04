import networkx as nx
import time


clock_in = time.time_ns()
graph: nx.Graph = nx.grid_2d_graph(13, 13)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

clock_in = time.time_ns()
for i in range(9):
    graph.remove_node((i, i))
    graph.add_node((i, i))
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")