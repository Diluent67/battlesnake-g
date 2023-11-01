from snake_engine import Battlesnake
import time


# Common sense
game_state = {"game":{"id":"7b0452d3-a738-4e19-be93-da148e2a1e53","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":18,"board":{"height":11,"width":11,"snakes":[{"id":"23a550b8-8365-41c3-a50c-ab311f034748","name":"Nightwing","latency":"514","health":84,"body":[{"x":7,"y":3},{"x":6,"y":3},{"x":5,"y":3},{"x":4,"y":3}],"head":{"x":7,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"12a17dfe-093f-4e94-9308-e115daf95fad","name":"JonK2","latency":"15","health":88,"body":[{"x":6,"y":4},{"x":7,"y":4},{"x":8,"y":4},{"x":8,"y":3},{"x":9,"y":3}],"head":{"x":6,"y":4},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"e11cc612-fe9a-44ae-8e11-e1d53db78d49","name":"Rick2","latency":"116","health":92,"body":[{"x":7,"y":7},{"x":7,"y":6},{"x":8,"y":6},{"x":8,"y":7},{"x":9,"y":7}],"head":{"x":7,"y":7},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"61a555e3-c09f-424b-b132-706eff747d2c","name":"Rick3","latency":"146","health":82,"body":[{"x":9,"y":9},{"x":9,"y":8},{"x":10,"y":8}],"head":{"x":9,"y":9},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"dd064945-98bf-4b08-8b27-7fd2d1c94e88","name":"JonK","latency":"31","health":86,"body":[{"x":5,"y":5},{"x":5,"y":6},{"x":5,"y":7},{"x":5,"y":8},{"x":5,"y":9}],"head":{"x":5,"y":5},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"ed3bda6b-5d39-4a18-9a2c-acd51ab70092","name":"JonK3","latency":"44","health":90,"body":[{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":8,"y":9},{"x":7,"y":9}],"head":{"x":6,"y":10},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":6,"y":5}],"hazards":[]},"you":{"id":"dd064945-98bf-4b08-8b27-7fd2d1c94e88","name":"JonK","latency":"31","health":86,"body":[{"x":5,"y":5},{"x":5,"y":6},{"x":5,"y":7},{"x":5,"y":8},{"x":5,"y":9}],"head":{"x":5,"y":5},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["down"]

# Should've got food
game_state = {"game":{"id":"8533c7c3-8372-4d85-acc4-4954d5c0aa4b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":178,"board":{"height":11,"width":11,"snakes":[{"id":"30b31eb5-c9cf-48e7-9c40-b3824fff2cc3","name":"Nightwing","latency":"351","health":100,"body":[{"x":6,"y":8},{"x":5,"y":8},{"x":4,"y":8},{"x":3,"y":8},{"x":3,"y":7},{"x":2,"y":7},{"x":1,"y":7},{"x":0,"y":7},{"x":0,"y":6},{"x":0,"y":5},{"x":0,"y":4},{"x":0,"y":3},{"x":0,"y":2},{"x":1,"y":2},{"x":1,"y":3},{"x":1,"y":3}],"head":{"x":6,"y":8},"length":16,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"46b6ee1d-6ed1-472b-ab03-53fff9c83431","name":"JonK","latency":"23","health":96,"body":[{"x":9,"y":3},{"x":9,"y":2},{"x":9,"y":1},{"x":10,"y":1},{"x":10,"y":0},{"x":9,"y":0},{"x":8,"y":0},{"x":7,"y":0},{"x":6,"y":0},{"x":5,"y":0},{"x":4,"y":0},{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3},{"x":4,"y":4},{"x":5,"y":4},{"x":6,"y":4},{"x":7,"y":4}],"head":{"x":9,"y":3},"length":18,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":9,"y":10},{"x":10,"y":9}],"hazards":[]},"you":{"id":"ad40b1ef-e988-45ab-a06d-ad3f0e060f91","name":"Glynn","latency":"135","health":88,"body":[{"x":6,"y":2},{"x":5,"y":2},{"x":4,"y":2}],"head":{"x":6,"y":2},"length":3,"shout":"","squad":"","customizations":{"color":"#6600ff","head":"all-seeing","tail":"weight"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["up", "right"]

# Avoid edge kill
game_state ={"game":{"id":"ebd7e984-bd7c-483f-9ab9-dd1941a2f627","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":23,"board":{"height":11,"width":11,"snakes":[{"id":"59149fd6-c5d1-468d-8858-0121f071ea9f","name":"Rick2","latency":"141","health":81,"body":[{"x":5,"y":10},{"x":4,"y":10},{"x":3,"y":10},{"x":2,"y":10}],"head":{"x":5,"y":10},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"1ea02430-c413-4093-96c8-8e32503ad9ea","name":"Rick3","latency":"160","health":81,"body":[{"x":6,"y":7},{"x":6,"y":8},{"x":6,"y":9},{"x":5,"y":9}],"head":{"x":6,"y":7},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"20b643cf-33a0-47d2-8a9b-bf7467009309","name":"JonK","latency":"27","health":94,"body":[{"x":4,"y":5},{"x":4,"y":6},{"x":3,"y":6},{"x":3,"y":7},{"x":2,"y":7}],"head":{"x":4,"y":5},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"a3ca9d01-053d-4cb3-ba87-2b3f98065f76","name":"JonK3","latency":"32","health":89,"body":[{"x":2,"y":1},{"x":2,"y":0},{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0},{"x":6,"y":0}],"head":{"x":2,"y":1},"length":6,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"3b5358d1-b7f7-4be1-b81c-35f62a67ff2b","name":"Nightwing","latency":"62","health":100,"body":[{"x":0,"y":5},{"x":1,"y":5},{"x":1,"y":4},{"x":1,"y":3},{"x":1,"y":2},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":2}],"head":{"x":0,"y":5},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"af15dcfa-39c7-438f-a02b-21192ac7ebff","name":"Rick","latency":"193","health":81,"body":[{"x":8,"y":5},{"x":8,"y":4},{"x":8,"y":3},{"x":8,"y":2}],"head":{"x":8,"y":5},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"a0ee3c4b-0096-4fb2-bcdc-4b8a7dd7499a","name":"JonK2","latency":"22","health":85,"body":[{"x":1,"y":6},{"x":2,"y":6},{"x":2,"y":5},{"x":2,"y":4},{"x":3,"y":4},{"x":4,"y":4}],"head":{"x":1,"y":6},"length":6,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":10,"y":5}],"hazards":[]},"you":{"id":"3b5358d1-b7f7-4be1-b81c-35f62a67ff2b","name":"Nightwing","latency":"62","health":100,"body":[{"x":0,"y":5},{"x":1,"y":5},{"x":1,"y":4},{"x":1,"y":3},{"x":1,"y":2},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":2}],"head":{"x":0,"y":5},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["down"]
game_state={"game":{"id":"831f3b79-48e4-4add-aebe-92e735e7e18d","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":46,"board":{"height":11,"width":11,"snakes":[{"id":"7c51708d-0c60-4e23-889d-8313e4f9d140","name":"Rick3","latency":"143","health":93,"body":[{"x":3,"y":7},{"x":3,"y":6},{"x":3,"y":5},{"x":3,"y":4},{"x":2,"y":4},{"x":2,"y":3}],"head":{"x":3,"y":7},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"359fc540-ae08-4454-9c79-31558d57192e","name":"Rick4","latency":"125","health":78,"body":[{"x":4,"y":8},{"x":5,"y":8},{"x":5,"y":7},{"x":6,"y":7},{"x":6,"y":6},{"x":5,"y":6}],"head":{"x":4,"y":8},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"b25b193e-d692-4c99-a0a2-bc5b1955572a","name":"Nightwing","latency":"250","health":87,"body":[{"x":1,"y":9},{"x":1,"y":8},{"x":1,"y":7},{"x":2,"y":7},{"x":2,"y":6}],"head":{"x":1,"y":9},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"4490fd70-e67c-4cc7-ba98-f9c5955d80d3","name":"JonK2","latency":"32","health":98,"body":[{"x":8,"y":6},{"x":7,"y":6},{"x":7,"y":7},{"x":7,"y":8},{"x":7,"y":9},{"x":7,"y":10},{"x":8,"y":10},{"x":8,"y":9}],"head":{"x":8,"y":6},"length":8,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":2,"y":1},{"x":9,"y":0}],"hazards":[]},"you":{"id":"7c51708d-0c60-4e23-889d-8313e4f9d140","name":"Rick3","latency":"143","health":93,"body":[{"x":3,"y":7},{"x":3,"y":6},{"x":3,"y":5},{"x":3,"y":4},{"x":2,"y":4},{"x":2,"y":3}],"head":{"x":3,"y":7},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move not in ["left"]
game_state={"game":{"id":"5409bbb9-e528-49b6-9ae7-ba6b52ad3b53","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":88,"board":{"height":11,"width":11,"snakes":[{"id":"c98b8781-777b-4285-a345-4439efeb8f8d","name":"Nightwing","latency":"55","health":100,"body":[{"x":0,"y":8},{"x":1,"y":8},{"x":1,"y":9},{"x":2,"y":9},{"x":3,"y":9},{"x":4,"y":9},{"x":5,"y":9},{"x":6,"y":9},{"x":6,"y":8},{"x":6,"y":8}],"head":{"x":0,"y":8},"length":10,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"0306f4b0-9a24-4016-a4e2-cd54ea6037cc","name":"JonK2","latency":"19","health":93,"body":[{"x":2,"y":6},{"x":2,"y":7},{"x":3,"y":7},{"x":4,"y":7},{"x":4,"y":6},{"x":5,"y":6},{"x":6,"y":6},{"x":6,"y":5},{"x":5,"y":5}],"head":{"x":2,"y":6},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":1,"y":7},{"x":4,"y":3},{"x":8,"y":6}],"hazards":[]},"you":{"id":"f927577c-7c90-4b60-b113-3824e07f3abe","name":"Rick3","latency":"147","health":37,"body":[{"x":8,"y":1},{"x":8,"y":0},{"x":7,"y":0}],"head":{"x":8,"y":1},"length":3,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["up"]

# Aggression
game_state = {"game":{"id":"3a462210-568a-4fbf-b55f-6638c64cbdb7","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":77,"board":{"height":11,"width":11,"snakes":[{"id":"db66670b-92da-4e7d-8269-dc58b703300c","name":"Nightwing","latency":"125","health":94,"body":[{"x":4,"y":3},{"x":4,"y":4},{"x":3,"y":4},{"x":2,"y":4},{"x":1,"y":4},{"x":1,"y":5},{"x":1,"y":6},{"x":2,"y":6},{"x":2,"y":5},{"x":3,"y":5}],"head":{"x":4,"y":3},"length":10,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"47ff25b9-4670-41a5-b53c-16477c71172a","name":"Rick","latency":"117","health":82,"body":[{"x":0,"y":9},{"x":0,"y":8},{"x":0,"y":7},{"x":1,"y":7},{"x":2,"y":7}],"head":{"x":0,"y":9},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"f39940a9-ab4e-4546-b251-6691e360d766","name":"JonK2","latency":"36","health":100,"body":[{"x":8,"y":9},{"x":7,"y":9},{"x":6,"y":9},{"x":5,"y":9},{"x":4,"y":9},{"x":4,"y":8},{"x":5,"y":8},{"x":5,"y":7},{"x":6,"y":7},{"x":6,"y":6},{"x":5,"y":6},{"x":5,"y":6}],"head":{"x":8,"y":9},"length":12,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"01ed6a96-9caf-4788-a36a-02b84962289c","name":"JonK3","latency":"28","health":95,"body":[{"x":2,"y":3},{"x":1,"y":3},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1},{"x":0,"y":0},{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0}],"head":{"x":2,"y":3},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":8,"y":6}],"hazards":[]},"you":{"id":"01ed6a96-9caf-4788-a36a-02b84962289c","name":"JonK3","latency":"28","health":95,"body":[{"x":2,"y":3},{"x":1,"y":3},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1},{"x":0,"y":0},{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0}],"head":{"x":2,"y":3},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["down", "left"]
game_state = {"game":{"id":"d8c6710a-9e60-483d-9ba6-88cb561e3a3d","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":75,"board":{"height":11,"width":11,"snakes":[{"id":"571f13e5-d4f5-4489-8c7e-c479f1b29a2f","name":"JonK","latency":"23","health":88,"body":[{"x":2,"y":7},{"x":2,"y":6},{"x":1,"y":6},{"x":1,"y":5},{"x":1,"y":4},{"x":2,"y":4}],"head":{"x":2,"y":7},"length":6,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"f82f5e25-43ba-4831-b1d7-76d552b8aae6","name":"JonK3","latency":"25","health":82,"body":[{"x":7,"y":6},{"x":7,"y":5},{"x":6,"y":5},{"x":5,"y":5},{"x":4,"y":5},{"x":4,"y":6},{"x":5,"y":6}],"head":{"x":7,"y":6},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"663700c9-e165-4ad0-b5c8-0adf94fca0a1","name":"Nightwing","latency":"55","health":91,"body":[{"x":9,"y":6},{"x":9,"y":5},{"x":10,"y":5},{"x":10,"y":4},{"x":10,"y":3},{"x":9,"y":3},{"x":8,"y":3},{"x":8,"y":4}],"head":{"x":9,"y":6},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"e653eaf5-2904-4d80-ad0f-99d4001b0095","name":"JonK2","latency":"25","health":94,"body":[{"x":7,"y":4},{"x":6,"y":4},{"x":5,"y":4},{"x":4,"y":4},{"x":4,"y":3},{"x":4,"y":2},{"x":3,"y":2},{"x":3,"y":3},{"x":3,"y":4},{"x":3,"y":5},{"x":3,"y":6}],"head":{"x":7,"y":4},"length":11,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":7,"y":8}],"hazards":[]},"you":{"id":"663700c9-e165-4ad0-b5c8-0adf94fca0a1","name":"Nightwing","latency":"55","health":91,"body":[{"x":9,"y":6},{"x":9,"y":5},{"x":10,"y":5},{"x":10,"y":4},{"x":10,"y":3},{"x":9,"y":3},{"x":8,"y":3},{"x":8,"y":4}],"head":{"x":9,"y":6},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["left"]
game_state = {"game":{"id":"cb769656-fe75-4959-b123-390eff4945bb","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":109,"board":{"height":11,"width":11,"snakes":[{"id":"f1af0262-9a47-4c98-b034-86332f2433e6","name":"Nightwing","latency":"90","health":95,"body":[{"x":3,"y":4},{"x":3,"y":5},{"x":3,"y":6},{"x":3,"y":7},{"x":3,"y":8},{"x":3,"y":9},{"x":4,"y":9},{"x":4,"y":8},{"x":5,"y":8},{"x":6,"y":8},{"x":7,"y":8},{"x":7,"y":7}],"head":{"x":3,"y":4},"length":12,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"60eb8bb7-8344-4450-a3be-7c89e59c584f","name":"Rick","latency":"120","health":89,"body":[{"x":5,"y":10},{"x":6,"y":10},{"x":6,"y":9},{"x":7,"y":9},{"x":8,"y":9},{"x":8,"y":8},{"x":8,"y":7},{"x":8,"y":6},{"x":8,"y":5},{"x":8,"y":4}],"head":{"x":5,"y":10},"length":10,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":0,"y":10},{"x":8,"y":0},{"x":7,"y":4}],"hazards":[]},"you":{"id":"39ad80f7-56b9-4c89-a124-8f67589c404e","name":"JonK3","latency":"31","health":82,"body":[{"x":4,"y":1},{"x":4,"y":2},{"x":3,"y":2},{"x":3,"y":3},{"x":4,"y":3}],"head":{"x":4,"y":1},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["left"]
game_state={"game":{"id":"5409bbb9-e528-49b6-9ae7-ba6b52ad3b53","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":188,"board":{"height":11,"width":11,"snakes":[{"id":"c98b8781-777b-4285-a345-4439efeb8f8d","name":"Nightwing","latency":"65","health":98,"body":[{"x":1,"y":3},{"x":1,"y":2},{"x":1,"y":1},{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0},{"x":6,"y":0},{"x":7,"y":0},{"x":8,"y":0},{"x":8,"y":1},{"x":7,"y":1},{"x":6,"y":1},{"x":5,"y":1},{"x":5,"y":2},{"x":5,"y":3},{"x":6,"y":3},{"x":6,"y":4},{"x":7,"y":4},{"x":7,"y":3},{"x":8,"y":3}],"head":{"x":1,"y":3},"length":22,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"0306f4b0-9a24-4016-a4e2-cd54ea6037cc","name":"JonK2","latency":"12","health":96,"body":[{"x":2,"y":4},{"x":2,"y":3},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":1},{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":4,"y":6},{"x":4,"y":7},{"x":3,"y":7},{"x":3,"y":8},{"x":3,"y":9},{"x":2,"y":9},{"x":2,"y":8},{"x":1,"y":8},{"x":0,"y":8},{"x":0,"y":7},{"x":1,"y":7}],"head":{"x":2,"y":4},"length":21,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":0,"y":3},{"x":9,"y":9}],"hazards":[]},"you":{"id":"0306f4b0-9a24-4016-a4e2-cd54ea6037cc","name":"JonK2","latency":"12","health":96,"body":[{"x":2,"y":4},{"x":2,"y":3},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":1},{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":4,"y":6},{"x":4,"y":7},{"x":3,"y":7},{"x":3,"y":8},{"x":3,"y":9},{"x":2,"y":9},{"x":2,"y":8},{"x":1,"y":8},{"x":0,"y":8},{"x":0,"y":7},{"x":1,"y":7}],"head":{"x":2,"y":4},"length":21,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["up"]

# Avoid getting trapped
game_state = {"game":{"id":"8533c7c3-8372-4d85-acc4-4954d5c0aa4b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":246,"board":{"height":11,"width":11,"snakes":[{"id":"30b31eb5-c9cf-48e7-9c40-b3824fff2cc3","name":"Nightwing","latency":"255","health":89,"body":[{"x":10,"y":4},{"x":9,"y":4},{"x":9,"y":3},{"x":9,"y":2},{"x":9,"y":1},{"x":9,"y":0},{"x":8,"y":0},{"x":8,"y":1},{"x":8,"y":2},{"x":8,"y":3},{"x":8,"y":4},{"x":8,"y":5},{"x":7,"y":5},{"x":7,"y":4},{"x":7,"y":3},{"x":7,"y":2},{"x":7,"y":1}],"head":{"x":10,"y":4},"length":17,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"46b6ee1d-6ed1-472b-ab03-53fff9c83431","name":"JonK","latency":"24","health":100,"body":[{"x":9,"y":7},{"x":8,"y":7},{"x":7,"y":7},{"x":6,"y":7},{"x":6,"y":8},{"x":5,"y":8},{"x":5,"y":9},{"x":5,"y":10},{"x":4,"y":10},{"x":3,"y":10},{"x":2,"y":10},{"x":2,"y":9},{"x":1,"y":9},{"x":0,"y":9},{"x":0,"y":8},{"x":0,"y":7},{"x":0,"y":6},{"x":0,"y":5},{"x":0,"y":4},{"x":1,"y":4},{"x":2,"y":4},{"x":2,"y":5},{"x":2,"y":6},{"x":1,"y":6},{"x":1,"y":7},{"x":1,"y":7}],"head":{"x":9,"y":7},"length":26,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":5,"y":5}],"hazards":[]},"you":{"id":"ad40b1ef-e988-45ab-a06d-ad3f0e060f91","name":"Glynn","latency":"135","health":88,"body":[{"x":6,"y":2},{"x":5,"y":2},{"x":4,"y":2}],"head":{"x":6,"y":2},"length":3,"shout":"","squad":"","customizations":{"color":"#6600ff","head":"all-seeing","tail":"weight"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["up"]
game_state = {"game":{"id":"93583e37-a5d1-4f1a-b682-57883240be6a","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":219,"board":{"height":11,"width":11,"snakes":[{"id":"3d44d587-99e5-4340-8ae4-143247074998","name":"JonK","latency":"21","health":98,"body":[{"x":9,"y":6},{"x":9,"y":5},{"x":10,"y":5},{"x":10,"y":4},{"x":9,"y":4},{"x":8,"y":4},{"x":7,"y":4},{"x":7,"y":3},{"x":6,"y":3},{"x":5,"y":3},{"x":5,"y":2},{"x":4,"y":2},{"x":3,"y":2},{"x":3,"y":3},{"x":4,"y":3},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5},{"x":6,"y":5},{"x":7,"y":5}],"head":{"x":9,"y":6},"length":20,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"b4346106-cf74-4809-ab5d-ee2d1fc4686f","name":"Nightwing","latency":"39","health":100,"body":[{"x":10,"y":1},{"x":9,"y":1},{"x":8,"y":1},{"x":7,"y":1},{"x":6,"y":1},{"x":5,"y":1},{"x":4,"y":1},{"x":3,"y":1},{"x":2,"y":1},{"x":1,"y":1},{"x":1,"y":2},{"x":0,"y":2},{"x":0,"y":3},{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5},{"x":2,"y":5},{"x":2,"y":6},{"x":3,"y":6},{"x":3,"y":7},{"x":3,"y":7}],"head":{"x":10,"y":1},"length":21,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}],"food":[{"x":5,"y":9}],"hazards":[]},"you":{"id":"362c38e0-ccb9-43f0-8190-fdae1b1ff8a6","name":"JonK3","latency":"32","health":48,"body":[{"x":8,"y":6},{"x":9,"y":6},{"x":9,"y":7},{"x":10,"y":7},{"x":10,"y":6}],"head":{"x":8,"y":6},"length":5,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["down"]
game_state = {"game":{"id":"8a5a7e1e-538b-453d-83df-e908a6f96a2b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":93,"board":{"height":11,"width":11,"snakes":[{"id":"79562f65-6955-4ec4-89ee-975fca9182ed","name":"Nightwing","latency":"78","health":70,"body":[{"x":3,"y":10},{"x":3,"y":9},{"x":2,"y":9},{"x":1,"y":9},{"x":1,"y":8},{"x":0,"y":8},{"x":0,"y":7}],"head":{"x":3,"y":10},"length":7,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"78838e38-a6aa-4bb9-a9d0-737a895fbf33","name":"Rick","latency":"129","health":54,"body":[{"x":2,"y":7},{"x":3,"y":7},{"x":3,"y":6},{"x":4,"y":6},{"x":5,"y":6},{"x":6,"y":6},{"x":6,"y":5}],"head":{"x":2,"y":7},"length":7,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"702e6cfd-dde1-4cc7-bedd-128e04fe1bac","name":"Rick3","latency":"138","health":91,"body":[{"x":4,"y":7},{"x":4,"y":8},{"x":5,"y":8},{"x":6,"y":8},{"x":7,"y":8},{"x":8,"y":8},{"x":8,"y":9},{"x":7,"y":9},{"x":6,"y":9}],"head":{"x":4,"y":7},"length":9,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"88a19cd6-834b-4358-b573-175c47d751a8","name":"JonK","latency":"13","health":100,"body":[{"x":1,"y":6},{"x":0,"y":6},{"x":0,"y":5},{"x":1,"y":5},{"x":2,"y":5},{"x":3,"y":5},{"x":4,"y":5},{"x":4,"y":4},{"x":4,"y":3},{"x":4,"y":2},{"x":4,"y":1},{"x":4,"y":1}],"head":{"x":1,"y":6},"length":12,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":0,"y":1}],"hazards":[]},"you":{"id":"79562f65-6955-4ec4-89ee-975fca9182ed","name":"Nightwing","latency":"78","health":70,"body":[{"x":3,"y":10},{"x":3,"y":9},{"x":2,"y":9},{"x":1,"y":9},{"x":1,"y":8},{"x":0,"y":8},{"x":0,"y":7}],"head":{"x":3,"y":10},"length":7,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["right"]  # TODO

# Properly stall out
game_state = {"game":{"id":"61c422b1-a67b-4944-a08b-2e38b0b0843b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":281,"board":{"height":11,"width":11,"snakes":[{"id":"72b3e3f7-5597-4104-8fc4-27e47942853e","name":"Nightwing","latency":"59","health":99,"body":[{"x":5,"y":10},{"x":4,"y":10},{"x":3,"y":10},{"x":3,"y":9},{"x":4,"y":9},{"x":4,"y":8},{"x":5,"y":8},{"x":6,"y":8},{"x":7,"y":8},{"x":8,"y":8},{"x":9,"y":8},{"x":10,"y":8},{"x":10,"y":7},{"x":10,"y":6},{"x":10,"y":5},{"x":10,"y":4},{"x":10,"y":3},{"x":10,"y":2},{"x":10,"y":1},{"x":10,"y":0},{"x":9,"y":0}],"head":{"x":5,"y":10},"length":21,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"f719a121-a185-43fa-ab77-49d6a1f10dfc","name":"JonK2","latency":"20","health":94,"body":[{"x":1,"y":4},{"x":0,"y":4},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1},{"x":0,"y":0},{"x":1,"y":0},{"x":1,"y":1},{"x":1,"y":2},{"x":2,"y":2},{"x":2,"y":1},{"x":3,"y":1},{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0},{"x":6,"y":0},{"x":6,"y":1},{"x":6,"y":2},{"x":5,"y":2},{"x":5,"y":1},{"x":4,"y":1},{"x":4,"y":2},{"x":3,"y":2}],"head":{"x":1,"y":4},"length":23,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}}],"food":[{"x":3,"y":5}],"hazards":[]},"you":{"id":"018c65af-3e00-4c56-8152-f8015257ae28","name":"Rick2","latency":"165","health":77,"body":[{"x":7,"y":8},{"x":7,"y":7},{"x":6,"y":7},{"x":5,"y":7},{"x":5,"y":8}],"head":{"x":7,"y":8},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["down"]

# Prioritise more space
game_state = {"game":{"id":"b71bf7c8-36a9-47ca-b269-f512597a2527","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":28,"board":{"height":11,"width":11,"snakes":[{"id":"e82444ff-0970-4b12-b65f-a6336f5a32cc","name":"Rick2","latency":"137","health":98,"body":[{"x":5,"y":7},{"x":5,"y":6},{"x":4,"y":6},{"x":4,"y":5},{"x":4,"y":4},{"x":4,"y":3}],"head":{"x":5,"y":7},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"bd22d84f-5c11-4cb2-96e9-5867ec8b59db","name":"Glynn","latency":"44","health":72,"body":[{"x":7,"y":7},{"x":8,"y":7},{"x":8,"y":8}],"head":{"x":7,"y":7},"length":3,"shout":"","squad":"","customizations":{"color":"#6600ff","head":"all-seeing","tail":"weight"}},{"id":"8cb70727-46d9-4b4c-a5be-d5b2a4bf753e","name":"Jesse","latency":"25","health":78,"body":[{"x":6,"y":8},{"x":5,"y":8},{"x":5,"y":9},{"x":6,"y":9}],"head":{"x":6,"y":8},"length":4,"shout":"","squad":"","customizations":{"color":"#E04C07","head":"missile","tail":"nr-booster"}},{"id":"091cc519-8e82-4b29-bc00-1d08b0c5489e","name":"Nightwing","latency":"103","health":96,"body":[{"x":0,"y":8},{"x":1,"y":8},{"x":1,"y":9},{"x":2,"y":9},{"x":2,"y":8},{"x":3,"y":8},{"x":3,"y":7},{"x":3,"y":6}],"head":{"x":0,"y":8},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"478b4690-3f18-4846-af95-e0d96b894b32","name":"Rick","latency":"135","health":92,"body":[{"x":2,"y":4},{"x":2,"y":3},{"x":2,"y":2},{"x":2,"y":1},{"x":2,"y":0},{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0}],"head":{"x":2,"y":4},"length":8,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}}],"food":[{"x":4,"y":10},{"x":5,"y":10}],"hazards":[]},"you":{"id":"e9c795aa-9235-4b12-9325-a449cc75b19f","name":"Matt2","latency":"258","health":90,"body":[{"x":10,"y":8},{"x":9,"y":8},{"x":8,"y":8}],"head":{"x":10,"y":8},"length":3,"shout":"","squad":"","customizations":{"color":"#1f9490","head":"default","tail":"default"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["up"]

# Don't need food
game_state={"game":{"id":"05c3c37b-4861-476a-bbc2-b0ce4d30a8af","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":45,"board":{"height":11,"width":11,"snakes":[{"id":"8e6c3427-ebf7-49ed-9b23-700342aef7f6","name":"JonK3","latency":"26","health":90,"body":[{"x":8,"y":3},{"x":7,"y":3},{"x":7,"y":4},{"x":7,"y":5},{"x":7,"y":6},{"x":7,"y":7},{"x":7,"y":8}],"head":{"x":8,"y":3},"length":7,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"2d41193c-8534-400f-9717-d4ee9272ea4f","name":"Rick4","latency":"158","health":87,"body":[{"x":9,"y":2},{"x":8,"y":2},{"x":7,"y":2},{"x":7,"y":1},{"x":6,"y":1}],"head":{"x":9,"y":2},"length":5,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"9110ff66-e559-46ce-9a35-63628ba2ac2b","name":"Nightwing","latency":"72","health":99,"body":[{"x":1,"y":2},{"x":1,"y":3},{"x":0,"y":3},{"x":0,"y":4},{"x":0,"y":5},{"x":0,"y":6},{"x":0,"y":7},{"x":1,"y":7},{"x":1,"y":8}],"head":{"x":1,"y":2},"length":9,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"571a52e2-2e02-4b77-91f2-e8ad7af0c2f1","name":"Rick","latency":"151","health":78,"body":[{"x":3,"y":4},{"x":3,"y":5},{"x":3,"y":6},{"x":3,"y":7},{"x":3,"y":8},{"x":4,"y":8}],"head":{"x":3,"y":4},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"4e3cc686-d592-40c1-bd25-3be41bccd872","name":"Rick2","latency":"114","health":94,"body":[{"x":6,"y":3},{"x":6,"y":4},{"x":6,"y":5},{"x":6,"y":6},{"x":5,"y":6},{"x":4,"y":6},{"x":4,"y":5},{"x":4,"y":4}],"head":{"x":6,"y":3},"length":8,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}}],"food":[{"x":0,"y":0}],"hazards":[]},"you":{"id":"571a52e2-2e02-4b77-91f2-e8ad7af0c2f1","name":"Rick","latency":"151","health":78,"body":[{"x":3,"y":4},{"x":3,"y":5},{"x":3,"y":6},{"x":3,"y":7},{"x":3,"y":8},{"x":4,"y":8}],"head":{"x":3,"y":4},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}}}
next_move = Battlesnake(game_state).optimal_move()
assert next_move in ["right"]

# Takes so long
game_state = {"game":{"id":"1940ebec-c2f4-472e-96db-ad5e659b4f7d","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":14,"board":{"height":11,"width":11,"snakes":[{"id":"262d660a-3a3b-4e78-994f-5561814d9eb1","name":"ricksnek2","latency":"131","health":90,"body":[{"x":5,"y":3},{"x":6,"y":3},{"x":7,"y":3},{"x":7,"y":4}],"head":{"x":5,"y":3},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}},{"id":"7bb6b728-6e52-45c9-adeb-fc103c09d5f7","name":"Nightwing","latency":"513","health":96,"body":[{"x":2,"y":4},{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":2,"y":4},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"d14b067d-9758-4a50-9f49-03af72175426","name":"ricksnek","latency":"119","health":88,"body":[{"x":5,"y":9},{"x":5,"y":8},{"x":6,"y":8},{"x":6,"y":7}],"head":{"x":5,"y":9},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"caffeine","tail":"coffee"}}],"food":[{"x":0,"y":9},{"x":8,"y":2}],"hazards":[]},"you":{"id":"7bb6b728-6e52-45c9-adeb-fc103c09d5f7","name":"Nightwing","latency":"513","health":96,"body":[{"x":2,"y":4},{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5}],"head":{"x":2,"y":4},"length":5,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
clock_in = time.time_ns()
next_move = Battlesnake(game_state).optimal_move()
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
assert total_time < 150, f"Runtime took {total_time}"
