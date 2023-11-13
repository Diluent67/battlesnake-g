from snake_engine import Battlesnake
import time

# aggression
game_state={"game":{"id":"87e99a13-c0d5-46a3-a9d7-c23b52f95c9f","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":65,"board":{"height":11,"width":11,"snakes":[{"id":"23bcc71a-93d3-49f4-af51-5f8aaabc986c","name":"Rick2","latency":"141","health":76,"body":[{"x":8,"y":7},{"x":7,"y":7},{"x":6,"y":7},{"x":5,"y":7},{"x":4,"y":7},{"x":3,"y":7}],"head":{"x":8,"y":7},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"fe6848ff-7177-4baf-8579-0c07c8897da9","name":"Rick3","latency":"152","health":96,"body":[{"x":8,"y":5},{"x":8,"y":4},{"x":8,"y":3},{"x":9,"y":3},{"x":9,"y":4},{"x":9,"y":5},{"x":9,"y":6}],"head":{"x":8,"y":5},"length":7,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"d2aadc28-a140-486d-a250-1104ecfffb4f","name":"JonK","latency":"31","health":92,"body":[{"x":3,"y":6},{"x":2,"y":6},{"x":2,"y":5},{"x":2,"y":4},{"x":1,"y":4},{"x":1,"y":3},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1},{"x":1,"y":1},{"x":2,"y":1}],"head":{"x":3,"y":6},"length":11,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ef379848-fc61-4016-b3ac-f6bcdf81d78b","name":"Nightwing","latency":"166","health":82,"body":[{"x":6,"y":9},{"x":6,"y":8},{"x":5,"y":8},{"x":5,"y":9},{"x":4,"y":9},{"x":3,"y":9}],"head":{"x":6,"y":9},"length":6,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"1039847c-1003-41a6-82f6-a1b19d9313a5","name":"JonK2","latency":"27","health":85,"body":[{"x":7,"y":6},{"x":6,"y":6},{"x":6,"y":5},{"x":5,"y":5},{"x":5,"y":4},{"x":4,"y":4},{"x":4,"y":3},{"x":4,"y":2},{"x":4,"y":1}],"head":{"x":7,"y":6},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":10,"y":6},{"x":4,"y":10}],"hazards":[]},"you":{"id":"1039847c-1003-41a6-82f6-a1b19d9313a5","name":"JonK2","latency":"27","health":85,"body":[{"x":7,"y":6},{"x":6,"y":6},{"x":6,"y":5},{"x":5,"y":5},{"x":5,"y":4},{"x":4,"y":4},{"x":4,"y":3},{"x":4,"y":2},{"x":4,"y":1}],"head":{"x":7,"y":6},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
# additional kill
game_state = {"game":{"id":"ecc6480a-d6e0-4246-82b5-ecd0ddde42fe","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":78,"board":{"height":11,"width":11,"snakes":[{"id":"6e80bf06-2f23-42ef-8858-aa451e9bf985","name":"JonK","latency":"14","health":92,"body":[{"x":4,"y":6},{"x":5,"y":6},{"x":6,"y":6},{"x":7,"y":6},{"x":8,"y":6},{"x":9,"y":6},{"x":10,"y":6},{"x":10,"y":5},{"x":10,"y":4},{"x":9,"y":4},{"x":8,"y":4},{"x":7,"y":4},{"x":6,"y":4}],"head":{"x":4,"y":6},"length":13,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"33ba4cb1-96a5-428c-b60d-2007520f822c","name":"Nightwing","latency":"148","health":80,"body":[{"x":2,"y":6},{"x":3,"y":6},{"x":3,"y":7},{"x":3,"y":8},{"x":3,"y":9},{"x":4,"y":9},{"x":4,"y":8},{"x":4,"y":7}],"head":{"x":2,"y":6},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"0fcc483a-f94b-4288-8ba5-62cb7dace466","name":"Rick","latency":"108","health":88,"body":[{"x":4,"y":10},{"x":5,"y":10},{"x":5,"y":9},{"x":5,"y":8},{"x":6,"y":8},{"x":6,"y":9}],"head":{"x":4,"y":10},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":0,"y":6},{"x":1,"y":1},{"x":4,"y":1}],"hazards":[]},"you":{"id":"7c378bb2-2b43-4884-9add-1c356d38fb53","name":"Rick2","latency":"112","health":97,"body":[{"x":9,"y":6},{"x":8,"y":6},{"x":7,"y":6},{"x":6,"y":6},{"x":5,"y":6}],"head":{"x":9,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
game_state = {"game":{"id":"ecc6480a-d6e0-4246-82b5-ecd0ddde42fe","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":192,"board":{"height":11,"width":11,"snakes":[{"id":"6e80bf06-2f23-42ef-8858-aa451e9bf985","name":"JonK","latency":"16","health":91,"body":[{"x":9,"y":3},{"x":9,"y":4},{"x":8,"y":4},{"x":7,"y":4},{"x":7,"y":3},{"x":7,"y":2},{"x":6,"y":2},{"x":5,"y":2},{"x":5,"y":3},{"x":6,"y":3},{"x":6,"y":4},{"x":6,"y":5},{"x":5,"y":5},{"x":4,"y":5},{"x":3,"y":5},{"x":2,"y":5},{"x":2,"y":4},{"x":1,"y":4},{"x":1,"y":3},{"x":2,"y":3},{"x":3,"y":3},{"x":3,"y":4}],"head":{"x":9,"y":3},"length":22,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"33ba4cb1-96a5-428c-b60d-2007520f822c","name":"Nightwing","latency":"135","health":100,"body":[{"x":1,"y":7},{"x":2,"y":7},{"x":3,"y":7},{"x":3,"y":8},{"x":4,"y":8},{"x":4,"y":9},{"x":4,"y":10},{"x":5,"y":10},{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":8,"y":9},{"x":8,"y":8},{"x":8,"y":7},{"x":8,"y":6},{"x":8,"y":6}],"head":{"x":1,"y":7},"length":16,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}],"food":[{"x":5,"y":4}],"hazards":[]},"you":{"id":"33ba4cb1-96a5-428c-b60d-2007520f822c","name":"Nightwing","latency":"135","health":100,"body":[{"x":1,"y":7},{"x":2,"y":7},{"x":3,"y":7},{"x":3,"y":8},{"x":4,"y":8},{"x":4,"y":9},{"x":4,"y":10},{"x":5,"y":10},{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":8,"y":9},{"x":8,"y":8},{"x":8,"y":7},{"x":8,"y":6},{"x":8,"y":6}],"head":{"x":1,"y":7},"length":16,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
game_state = {"game":{"id":"ecc6480a-d6e0-4246-82b5-ecd0ddde42fe","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":246,"board":{"height":11,"width":11,"snakes":[{"id":"6e80bf06-2f23-42ef-8858-aa451e9bf985","name":"JonK","latency":"16","health":99,"body":[{"x":0,"y":10},{"x":1,"y":10},{"x":1,"y":9},{"x":1,"y":8},{"x":2,"y":8},{"x":3,"y":8},{"x":4,"y":8},{"x":5,"y":8},{"x":6,"y":8},{"x":6,"y":9},{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":8,"y":9},{"x":7,"y":9},{"x":7,"y":8},{"x":7,"y":7},{"x":8,"y":7},{"x":8,"y":8},{"x":9,"y":8},{"x":10,"y":8},{"x":10,"y":7},{"x":10,"y":6},{"x":10,"y":5},{"x":10,"y":4},{"x":10,"y":3},{"x":9,"y":3}],"head":{"x":0,"y":10},"length":27,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"33ba4cb1-96a5-428c-b60d-2007520f822c","name":"Nightwing","latency":"91","health":100,"body":[{"x":5,"y":7},{"x":5,"y":6},{"x":5,"y":5},{"x":5,"y":4},{"x":6,"y":4},{"x":6,"y":3},{"x":5,"y":3},{"x":4,"y":3},{"x":3,"y":3},{"x":2,"y":3},{"x":1,"y":3},{"x":1,"y":2},{"x":1,"y":1},{"x":2,"y":1},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":1},{"x":4,"y":1},{"x":4,"y":0},{"x":5,"y":0},{"x":5,"y":0}],"head":{"x":5,"y":7},"length":21,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}],"food":[{"x":0,"y":9}],"hazards":[]},"you":{"id":"7c378bb2-2b43-4884-9add-1c356d38fb53","name":"Rick2","latency":"112","health":97,"body":[{"x":9,"y":6},{"x":8,"y":6},{"x":7,"y":6},{"x":6,"y":6},{"x":5,"y":6}],"head":{"x":9,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}

# BROKE
game_state=None

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(f"\nBest move: {b.optimal_move()}")
print(f"Total time: {round((time.time_ns() - clock_in) / 1000000, 3)}")
