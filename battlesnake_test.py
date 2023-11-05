from snake_engine import *

game_state = {"game":{"id":"6f625f18-4bf4-49bc-9659-1df834a4c769","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"5af5fbcb-1f86-422d-96ab-833ec49e660b","name":"Rick4","latency":"0","health":100,"body":[{"x":1,"y":1},{"x":1,"y":1},{"x":1,"y":1}],"head":{"x":1,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"394e7449-3aae-4d0b-a85d-30dbe14dcc11","name":"Nightwing","latency":"0","health":100,"body":[{"x":1,"y":9},{"x":1,"y":9},{"x":1,"y":9}],"head":{"x":1,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"822dfa8a-7502-4dd6-8cdc-591c8ff0b405","name":"Rick","latency":"0","health":100,"body":[{"x":9,"y":1},{"x":9,"y":1},{"x":9,"y":1}],"head":{"x":9,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"9610c627-687f-4b76-a77b-cb8536eacce1","name":"JonK2","latency":"0","health":100,"body":[{"x":9,"y":9},{"x":9,"y":9},{"x":9,"y":9}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ed603536-f608-4398-8fb7-3ddd12867d73","name":"Rick2","latency":"0","health":100,"body":[{"x":5,"y":9},{"x":5,"y":9},{"x":5,"y":9}],"head":{"x":5,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"ac1f8550-deb5-4f9e-90f4-d1e2045e4030","name":"Rick3","latency":"0","health":100,"body":[{"x":5,"y":1},{"x":5,"y":1},{"x":5,"y":1}],"head":{"x":5,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"70f0fd83-753b-4cf4-8f4f-84f4f6679827","name":"JonK","latency":"0","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"85720c44-c37e-4300-a85a-c222d31178cc","name":"JonK3","latency":"0","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":2,"y":0},{"x":0,"y":8},{"x":8,"y":0},{"x":10,"y":8},{"x":4,"y":10},{"x":4,"y":0},{"x":0,"y":4},{"x":10,"y":4},{"x":5,"y":5}],"hazards":[]},"you":{"id":"9610c627-687f-4b76-a77b-cb8536eacce1","name":"JonK2","latency":"0","health":100,"body":[{"x":9,"y":9},{"x":9,"y":9},{"x":9,"y":9}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}

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
