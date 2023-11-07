from snake_engine import Battlesnake
import time

game_state ={"game":{"id":"f522977f-e085-44fc-9ce4-1b69bfed5b76","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":42,"board":{"height":11,"width":11,"snakes":[{"id":"a2528539-8d81-4ed3-8eda-1d39bc9e3898","name":"Glynn","latency":"25","health":58,"body":[{"x":7,"y":5},{"x":7,"y":4},{"x":7,"y":3}],"head":{"x":7,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#6600ff","head":"all-seeing","tail":"weight"}},{"id":"774d49b9-c27a-457d-b7a2-21179bfce6db","name":"JonK","latency":"22","health":99,"body":[{"x":5,"y":9},{"x":5,"y":10},{"x":4,"y":10},{"x":3,"y":10},{"x":2,"y":10},{"x":1,"y":10},{"x":1,"y":9}],"head":{"x":5,"y":9},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"e2734d0f-e7b9-48b1-a7ae-b4058b4bdf23","name":"Einar","latency":"89","health":76,"body":[{"x":6,"y":0},{"x":7,"y":0},{"x":8,"y":0},{"x":8,"y":1},{"x":9,"y":1}],"head":{"x":6,"y":0},"length":5,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}},{"id":"12d299be-2a62-46db-95b2-dada57044950","name":"JonK2","latency":"20","health":91,"body":[{"x":3,"y":3},{"x":3,"y":4},{"x":4,"y":4},{"x":4,"y":3},{"x":5,"y":3},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":3,"y":3},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"9b97622f-a4d4-4e47-841b-d0fae7c5cab9","name":"Nightwing","latency":"318","health":60,"body":[{"x":4,"y":2},{"x":3,"y":2},{"x":2,"y":2},{"x":2,"y":1}],"head":{"x":4,"y":2},"length":4,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"d2d3dd4b-cbe4-452c-9eaf-492055c98708","name":"Rick","latency":"121","health":98,"body":[{"x":9,"y":7},{"x":9,"y":8},{"x":9,"y":9},{"x":8,"y":9},{"x":8,"y":8}],"head":{"x":9,"y":7},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":5,"y":2}],"hazards":[]},"you":{"id":"e2734d0f-e7b9-48b1-a7ae-b4058b4bdf23","name":"Einar","latency":"89","health":76,"body":[{"x":6,"y":0},{"x":7,"y":0},{"x":8,"y":0},{"x":8,"y":1},{"x":9,"y":1}],"head":{"x":6,"y":0},"length":5,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
