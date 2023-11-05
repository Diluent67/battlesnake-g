from snake_engine import *

# Not as aggressive
game_state={"game":{"id":"38cb46fb-3c5a-4f92-800e-24684f6b4f39","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":40,"board":{"height":11,"width":11,"snakes":[{"id":"c35066f9-3923-468a-8e56-c44521afb489","name":"Nightwing","latency":"48","health":93,"body":[{"x":8,"y":10},{"x":9,"y":10},{"x":10,"y":10},{"x":10,"y":9},{"x":9,"y":9},{"x":9,"y":8},{"x":10,"y":8},{"x":10,"y":7},{"x":9,"y":7}],"head":{"x":8,"y":10},"length":9,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"e5d82f57-ed33-44db-92e4-de9f0e5db477","name":"Rick","latency":"135","health":66,"body":[{"x":1,"y":7},{"x":1,"y":6},{"x":1,"y":5},{"x":1,"y":4},{"x":2,"y":4}],"head":{"x":1,"y":7},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"401ae866-9969-481e-bae2-edd3b3050409","name":"JonK2","latency":"29","health":90,"body":[{"x":6,"y":10},{"x":5,"y":10},{"x":4,"y":10},{"x":4,"y":9},{"x":5,"y":9},{"x":5,"y":8},{"x":6,"y":8},{"x":6,"y":7}],"head":{"x":6,"y":10},"length":8,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"f8805a6d-e396-4044-9a27-d990860374ae","name":"Rick3","latency":"117","health":60,"body":[{"x":6,"y":2},{"x":5,"y":2},{"x":4,"y":2}],"head":{"x":6,"y":2},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"c9dda990-15bd-43ec-82b0-12a25546967c","name":"JonK","latency":"45","health":96,"body":[{"x":2,"y":8},{"x":2,"y":9},{"x":2,"y":10},{"x":3,"y":10},{"x":3,"y":9},{"x":3,"y":8},{"x":3,"y":7}],"head":{"x":2,"y":8},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ac0ce56b-2def-460f-be0f-3b4578cc1238","name":"JonK3","latency":"30","health":100,"body":[{"x":4,"y":6},{"x":5,"y":6},{"x":5,"y":5},{"x":6,"y":5},{"x":6,"y":5}],"head":{"x":4,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":7,"y":3}],"hazards":[]},"you":{"id":"e230991a-cf3e-4057-9730-8670cfa349e8","name":"Rick2","latency":"271","health":92,"body":[{"x":7,"y":5},{"x":7,"y":6},{"x":7,"y":7}],"head":{"x":7,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}

clock_in = time.time_ns()
game = Battlesnake(game_state, debugging=True)
print(game.optimal_move())
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")


# import cProfile, pstats
# profiler = cProfile.Profile()
# profiler.enable()
# game.optimal_move()
# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats('tottime')
# stats.print_stats()

# import timeit
# start = timeit.default_timer()
# print("The start time is :", start)
# next_move = game.flood_fill(game.my_id, confined_area="left")
# print("The difference of time is :",
#               timeit.default_timer() - start)
