from snake_engine import *

game_state = {"game":{"id":"bf52fd8e-9cd7-4f9c-a328-db6d31f35a41","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":5,"board":{"height":11,"width":11,"snakes":[{"id":"e14a5103-3845-4fb3-81a2-3044fdf55502","name":"Matt","latency":"37","health":95,"body":[{"x":6,"y":1},{"x":5,"y":1},{"x":4,"y":1}],"head":{"x":6,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#1f9490","head":"default","tail":"default"}},{"id":"efc3da86-5096-427c-9636-3937aa87ac72","name":"Glynn","latency":"57","health":95,"body":[{"x":2,"y":7},{"x":2,"y":8},{"x":2,"y":9}],"head":{"x":2,"y":7},"length":3,"shout":"","squad":"","customizations":{"color":"#6600ff","head":"all-seeing","tail":"weight"}},{"id":"2bffd66d-5f1d-4351-af76-8346d74d540d","name":"Jesse","latency":"25","health":95,"body":[{"x":5,"y":8},{"x":6,"y":8},{"x":7,"y":8}],"head":{"x":5,"y":8},"length":3,"shout":"","squad":"","customizations":{"color":"#E04C07","head":"missile","tail":"nr-booster"}},{"id":"9f0e6b1e-3d0c-4cf9-903f-0c4b1a423090","name":"Rick3","latency":"169","health":99,"body":[{"x":10,"y":3},{"x":10,"y":2},{"x":9,"y":2},{"x":8,"y":2}],"head":{"x":10,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"e006161b-f590-41b0-a4bb-43e1ee8a9583","name":"Einar","latency":"101","health":99,"body":[{"x":0,"y":1},{"x":0,"y":2},{"x":0,"y":3},{"x":0,"y":4},{"x":1,"y":4}],"head":{"x":0,"y":1},"length":5,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}},{"id":"de4c5e43-836c-4a46-a463-2e13ec3a51e8","name":"Rick2","latency":"173","health":95,"body":[{"x":4,"y":5},{"x":4,"y":4},{"x":5,"y":4}],"head":{"x":4,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"963133d6-1d17-46b6-8a39-28a3cabbeeaf","name":"Nightwing","latency":"198","health":99,"body":[{"x":8,"y":9},{"x":8,"y":10},{"x":7,"y":10},{"x":6,"y":10},{"x":5,"y":10}],"head":{"x":8,"y":9},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"20d3fec3-679e-4a21-857b-769d3cc20619","name":"Rick","latency":"150","health":95,"body":[{"x":7,"y":6},{"x":6,"y":6},{"x":6,"y":5}],"head":{"x":7,"y":6},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":0,"y":8},{"x":4,"y":0},{"x":10,"y":6},{"x":5,"y":5}],"hazards":[]},"you":{"id":"9f0e6b1e-3d0c-4cf9-903f-0c4b1a423090","name":"Rick3","latency":"169","health":99,"body":[{"x":10,"y":3},{"x":10,"y":2},{"x":9,"y":2},{"x":8,"y":2}],"head":{"x":10,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}


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
