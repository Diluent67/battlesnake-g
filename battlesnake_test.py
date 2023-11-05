from snake_engine import *

game_state = {"game":{"id":"bf4d28d9-e6ed-4fc2-9fda-b2d0d2ba71bb","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"c78cab2a-64ea-489d-b636-b8ec252d0a54","name":"JonK3","latency":"0","health":100,"body":[{"x":9,"y":1},{"x":9,"y":1},{"x":9,"y":1}],"head":{"x":9,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ffa97db9-8506-4ec0-a8b0-6efd806bde02","name":"Rick4","latency":"0","health":100,"body":[{"x":9,"y":9},{"x":9,"y":9},{"x":9,"y":9}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"7214b8d9-3cae-45e6-960d-ad301c5372b3","name":"Nightwing","latency":"0","health":100,"body":[{"x":1,"y":9},{"x":1,"y":9},{"x":1,"y":9}],"head":{"x":1,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"b96e70a5-1cf3-4908-9500-78bde2fcfa94","name":"Rick","latency":"0","health":100,"body":[{"x":1,"y":1},{"x":1,"y":1},{"x":1,"y":1}],"head":{"x":1,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"f8968b19-e26a-4415-b5ae-4f8f414d2564","name":"JonK2","latency":"0","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ab870d88-ba7c-4dbf-a127-6936703d28b5","name":"Rick2","latency":"0","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"80c3eee0-2e60-468c-994b-0f341b4f2d5a","name":"Rick3","latency":"0","health":100,"body":[{"x":5,"y":1},{"x":5,"y":1},{"x":5,"y":1}],"head":{"x":5,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"7c93176b-e9f4-4be7-b265-5ef292d41378","name":"JonK","latency":"0","health":100,"body":[{"x":5,"y":9},{"x":5,"y":9},{"x":5,"y":9}],"head":{"x":5,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":8,"y":0},{"x":8,"y":10},{"x":0,"y":8},{"x":0,"y":2},{"x":10,"y":6},{"x":0,"y":6},{"x":4,"y":0},{"x":4,"y":10},{"x":5,"y":5}],"hazards":[]},"you":{"id":"c78cab2a-64ea-489d-b636-b8ec252d0a54","name":"JonK3","latency":"0","health":100,"body":[{"x":9,"y":1},{"x":9,"y":1},{"x":9,"y":1}],"head":{"x":9,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}

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
