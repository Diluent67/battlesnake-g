from snake_engine import *

game_state = {"game":{"id":"2330697c-56d3-4425-8134-d6dea727a63f","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"72b6cff4-a25b-4ce0-90fd-c46b1ab13e55","name":"JonK","latency":"0","health":100,"body":[{"x":9,"y":9},{"x":9,"y":9},{"x":9,"y":9}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"4a3a6a07-42d2-433a-9038-e4f48310f3ef","name":"JonK3","latency":"0","health":100,"body":[{"x":1,"y":9},{"x":1,"y":9},{"x":1,"y":9}],"head":{"x":1,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"8a39a6b8-fac0-4857-874b-5c6f2178dfd6","name":"Rick4","latency":"0","health":100,"body":[{"x":1,"y":1},{"x":1,"y":1},{"x":1,"y":1}],"head":{"x":1,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"b495c904-08cd-4e7e-b992-d62b63b2ce28","name":"Nightwing","latency":"0","health":100,"body":[{"x":9,"y":1},{"x":9,"y":1},{"x":9,"y":1}],"head":{"x":9,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"8cf76313-34da-4ba1-b2d0-61669b3cae40","name":"Rick","latency":"0","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"1b6f4acd-e93b-4a4c-b37e-13d0d0d54f43","name":"JonK2","latency":"0","health":100,"body":[{"x":5,"y":9},{"x":5,"y":9},{"x":5,"y":9}],"head":{"x":5,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ca417f47-7779-457a-bde3-5c4f9ff5db86","name":"Rick2","latency":"0","health":100,"body":[{"x":5,"y":1},{"x":5,"y":1},{"x":5,"y":1}],"head":{"x":5,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"92bf5f45-9073-42d0-9dea-7b998fb23bf5","name":"Rick3","latency":"0","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":10,"y":8},{"x":0,"y":8},{"x":0,"y":2},{"x":10,"y":2},{"x":10,"y":6},{"x":4,"y":10},{"x":6,"y":0},{"x":0,"y":6},{"x":5,"y":5}],"hazards":[]},"you":{"id":"ca417f47-7779-457a-bde3-5c4f9ff5db86","name":"Rick2","latency":"0","health":100,"body":[{"x":5,"y":1},{"x":5,"y":1},{"x":5,"y":1}],"head":{"x":5,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}

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
