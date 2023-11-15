from snake_engine import *

game_state={"game":{"id":"d07d4832-3fbc-4df7-bc1f-84909baa01a2","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":8,"board":{"height":11,"width":11,"snakes":[{"id":"794984a9-316f-437a-a5e7-123afa1799b9","name":"Rick2","latency":"150","health":98,"body":[{"x":3,"y":1},{"x":2,"y":1},{"x":2,"y":0},{"x":1,"y":0}],"head":{"x":3,"y":1},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"a8d162b1-df10-4523-829b-6c751989810c","name":"Rick3","latency":"212","health":100,"body":[{"x":10,"y":6},{"x":10,"y":7},{"x":10,"y":8},{"x":10,"y":9},{"x":10,"y":9}],"head":{"x":10,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"c653eaec-5707-482a-abf2-702d6ba76fd7","name":"JonK","latency":"22","health":96,"body":[{"x":5,"y":1},{"x":4,"y":1},{"x":4,"y":0},{"x":5,"y":0},{"x":6,"y":0}],"head":{"x":5,"y":1},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"bbf93a5d-e566-49dd-81f6-3bea14ecc43e","name":"JonK3","latency":"21","health":98,"body":[{"x":0,"y":8},{"x":0,"y":9},{"x":1,"y":9},{"x":1,"y":8},{"x":2,"y":8}],"head":{"x":0,"y":8},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"5c1999e6-c1be-4593-839a-4c50cd971c20","name":"Rick4","latency":"199","health":100,"body":[{"x":5,"y":5},{"x":5,"y":4},{"x":5,"y":3},{"x":5,"y":3}],"head":{"x":5,"y":5},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"86b77068-eaf5-46ff-a934-be44318ca9ba","name":"Nightwing","latency":"480","health":94,"body":[{"x":7,"y":7},{"x":7,"y":8},{"x":8,"y":8},{"x":8,"y":9}],"head":{"x":7,"y":7},"length":4,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"d4972a83-7849-4d3f-be9b-1208252347df","name":"Rick","latency":"221","health":92,"body":[{"x":9,"y":5},{"x":9,"y":6},{"x":8,"y":6}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"f1a83c20-e9c4-4bec-9502-0290ad260bae","name":"JonK2","latency":"21","health":94,"body":[{"x":1,"y":3},{"x":1,"y":2},{"x":2,"y":2},{"x":2,"y":3}],"head":{"x":1,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":0,"y":5}],"hazards":[]},"you":{"id":"a8d162b1-df10-4523-829b-6c751989810c","name":"Rick3","latency":"212","health":100,"body":[{"x":10,"y":6},{"x":10,"y":7},{"x":10,"y":8},{"x":10,"y":9},{"x":10,"y":9}],"head":{"x":10,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
game_state = {"game":{"id":"1940ebec-c2f4-472e-96db-ad5e659b4f7d","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":14,"board":{"height":11,"width":11,"snakes":[{"id":"262d660a-3a3b-4e78-994f-5561814d9eb1","name":"ricksnek2","latency":"131","health":90,"body":[{"x":5,"y":3},{"x":6,"y":3},{"x":7,"y":3},{"x":7,"y":4}],"head":{"x":5,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"7bb6b728-6e52-45c9-adeb-fc103c09d5f7","name":"Nightwing","latency":"513","health":96,"body":[{"x":2,"y":4},{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":2,"y":4},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"d14b067d-9758-4a50-9f49-03af72175426","name":"ricksnek","latency":"119","health":88,"body":[{"x":5,"y":9},{"x":5,"y":8},{"x":6,"y":8},{"x":6,"y":7}],"head":{"x":5,"y":9},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}}],"food":[{"x":0,"y":9},{"x":8,"y":2}],"hazards":[]},"you":{"id":"7bb6b728-6e52-45c9-adeb-fc103c09d5f7","name":"Nightwing","latency":"513","health":96,"body":[{"x":2,"y":4},{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":2,"y":4},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}


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
