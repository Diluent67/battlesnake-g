from snake_engine import Battlesnake
import time

# aggression
game_state = {"game":{"id":"60e1b749-34f3-4558-9940-5a9f0e48a6cd","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":221,"board":{"height":11,"width":11,"snakes":[{"id":"2698362f-d048-48ac-9606-ca78e22e4099","name":"Einar","latency":"92","health":90,"body":[{"x":2,"y":5},{"x":3,"y":5},{"x":3,"y":4},{"x":3,"y":3},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":4,"y":6},{"x":4,"y":7},{"x":4,"y":8},{"x":4,"y":9},{"x":3,"y":9},{"x":2,"y":9},{"x":1,"y":9},{"x":0,"y":9},{"x":0,"y":8},{"x":0,"y":7},{"x":0,"y":6},{"x":0,"y":5},{"x":0,"y":4},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1}],"head":{"x":2,"y":5},"length":23,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}},{"id":"70356921-27a0-4af4-8281-6eb38e35b574","name":"Nightwing","latency":"140","health":80,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":5,"y":2},{"x":6,"y":2},{"x":6,"y":3},{"x":5,"y":3},{"x":5,"y":4},{"x":5,"y":5},{"x":6,"y":5},{"x":7,"y":5},{"x":7,"y":6},{"x":8,"y":6},{"x":8,"y":7},{"x":9,"y":7},{"x":9,"y":6},{"x":9,"y":5},{"x":9,"y":4},{"x":9,"y":3}],"head":{"x":3,"y":2},"length":18,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}],"food":[{"x":1,"y":5}],"hazards":[]},"you":{"id":"11937642-f2c6-49f2-a135-fdd78d4aa332","name":"Jesse","latency":"31","health":94,"body":[{"x":3,"y":3},{"x":3,"y":4},{"x":3,"y":3}],"head":{"x":3,"y":3},"length":3,"shout":"","squad":"","customizations":{"color":"#E04C07","head":"missile","tail":"nr-booster"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
