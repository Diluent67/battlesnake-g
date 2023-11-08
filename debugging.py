from snake_engine import Battlesnake
import time

# aggression
game_state = {"game":{"id":"656aba8e-4590-447a-b4c7-7d0aaeb6a159","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":47,"board":{"height":11,"width":11,"snakes":[{"id":"1680f1d9-27d5-4cb5-bb97-79b329af1f41","name":"Nightwing","latency":"139","health":85,"body":[{"x":3,"y":8},{"x":3,"y":7},{"x":4,"y":7},{"x":4,"y":6},{"x":4,"y":5},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":3,"y":8},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"29a0ffdf-17b7-4f79-983a-d3c1b3885946","name":"Einar","latency":"88","health":100,"body":[{"x":1,"y":10},{"x":0,"y":10},{"x":0,"y":9},{"x":0,"y":8},{"x":0,"y":7},{"x":0,"y":7}],"head":{"x":1,"y":10},"length":6,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}}],"food":[{"x":9,"y":5},{"x":7,"y":1},{"x":1,"y":3}],"hazards":[]},"you":{"id":"8befe153-78b8-4eb8-8606-f562694f66aa","name":"JonK","latency":"24","health":97,"body":[{"x":5,"y":4},{"x":4,"y":4},{"x":4,"y":5},{"x":3,"y":5},{"x":3,"y":4},{"x":3,"y":3},{"x":4,"y":3}],"head":{"x":5,"y":4},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
