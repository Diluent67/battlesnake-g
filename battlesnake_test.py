from snake_engine import *

game_state = {"game":{"id":"5f48c478-724e-4b52-9c91-5404fe8d0be8","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"6214c1a1-0466-4f91-b4ac-54c272e3ed6d","name":"JonK","latency":"0","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"64b2fc68-6a13-4c08-9af9-8582c314da7b","name":"JonK3","latency":"0","health":100,"body":[{"x":5,"y":9},{"x":5,"y":9},{"x":5,"y":9}],"head":{"x":5,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"d9dc2f49-f7fe-4925-a288-b187c9d24501","name":"Rick4","latency":"0","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"8a1cf727-771b-440b-b184-7357ef44aa85","name":"Nightwing","latency":"0","health":100,"body":[{"x":5,"y":1},{"x":5,"y":1},{"x":5,"y":1}],"head":{"x":5,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"333787af-c69a-4591-bb4a-060e867dc1e6","name":"Rick","latency":"0","health":100,"body":[{"x":1,"y":9},{"x":1,"y":9},{"x":1,"y":9}],"head":{"x":1,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"2c1ab8d7-26d6-4e63-83e6-86ec85dd21d0","name":"JonK2","latency":"0","health":100,"body":[{"x":1,"y":1},{"x":1,"y":1},{"x":1,"y":1}],"head":{"x":1,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ced01f1e-7493-44a2-8816-446e83528422","name":"Rick2","latency":"0","health":100,"body":[{"x":9,"y":9},{"x":9,"y":9},{"x":9,"y":9}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"c71b5283-26d6-4077-ba2a-1b593564ae85","name":"Rick3","latency":"0","health":100,"body":[{"x":9,"y":1},{"x":9,"y":1},{"x":9,"y":1}],"head":{"x":9,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":10,"y":6},{"x":4,"y":10},{"x":0,"y":6},{"x":6,"y":0},{"x":0,"y":8},{"x":2,"y":0},{"x":10,"y":8},{"x":10,"y":2},{"x":5,"y":5}],"hazards":[]},"you":{"id":"2c1ab8d7-26d6-4e63-83e6-86ec85dd21d0","name":"JonK2","latency":"0","health":100,"body":[{"x":1,"y":1},{"x":1,"y":1},{"x":1,"y":1}],"head":{"x":1,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}

clock_in = time.time_ns()
game = Battlesnake(game_state, debugging=False)
print(game.optimal_move())
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")


import cProfile, pstats
profiler = cProfile.Profile()
profiler.enable()
game.optimal_move()
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()
print("\n\n")
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats()
# import timeit
# start = timeit.default_timer()
# print("The start time is :", start)
# next_move = game.flood_fill(game.my_id, confined_area="left")
# print("The difference of time is :",
#               timeit.default_timer() - start)
