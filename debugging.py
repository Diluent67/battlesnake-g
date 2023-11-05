from snake_engine import Battlesnake
import time

game_state = {"game":{"id":"5f48c478-724e-4b52-9c91-5404fe8d0be8","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":226,"board":{"height":11,"width":11,"snakes":[{"id":"8a1cf727-771b-440b-b184-7357ef44aa85","name":"Nightwing","latency":"182","health":96,"body":[{"x":1,"y":7},{"x":2,"y":7},{"x":2,"y":8},{"x":2,"y":9},{"x":2,"y":10},{"x":3,"y":10},{"x":3,"y":9},{"x":4,"y":9},{"x":5,"y":9},{"x":5,"y":10},{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":9,"y":10}],"head":{"x":1,"y":7},"length":14,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"ced01f1e-7493-44a2-8816-446e83528422","name":"Rick2","latency":"124","health":95,"body":[{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5},{"x":6,"y":5},{"x":6,"y":6},{"x":7,"y":6},{"x":8,"y":6},{"x":9,"y":6},{"x":9,"y":5},{"x":9,"y":4},{"x":10,"y":4},{"x":10,"y":3},{"x":9,"y":3},{"x":9,"y":2},{"x":9,"y":1},{"x":8,"y":1},{"x":7,"y":1},{"x":6,"y":1}],"head":{"x":4,"y":4},"length":18,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":3,"y":3},{"x":8,"y":2},{"x":5,"y":1}],"hazards":[]},"you":{"id":"c71b5283-26d6-4077-ba2a-1b593564ae85","name":"Rick3","latency":"171","health":74,"body":[{"x":0,"y":6},{"x":0,"y":7},{"x":0,"y":8},{"x":0,"y":9}],"head":{"x":0,"y":6},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
