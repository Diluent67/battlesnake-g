import networkx as nx
import time
import cProfile, pstats

# game.optimal_move()
#
# print("\n\n")
# stats = pstats.Stats(profiler).sort_stats('cumtime')
# stats.print_stats()

n = 0
t = [(2,2), (3,3)]
for (x,y) in t:
    if (n := x - n) > 0:
        print(n)
        print("+")
    else:
        print(n)


graph: nx.Graph = nx.grid_2d_graph(11,11)
profiler = cProfile.Profile()
profiler.enable()
for i in range(1000):
    for x in range(3):
        for y in range(3):
            graph.remove_node((x,y))
            if not graph.has_node((x,y)):
                possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for e in possible_edges:
                    if graph.has_node(e):
                        graph.add_edge((x,y), e)
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()


graph: nx.Graph = nx.grid_2d_graph(3, 3)
profiler = cProfile.Profile()
profiler.enable()
for i in range(1000):
    for x in range(3):
        for y in range(3):
            graph.remove_node((x,y))
            possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for e in possible_edges:
                if graph.has_node(e):
                    graph.add_edge((x,y), e)
            lena = graph.number_of_nodes()
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()





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

