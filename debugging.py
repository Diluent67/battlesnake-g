from snake_engine import Battlesnake
import time

game_state = {"game":{"id":"5f48c478-724e-4b52-9c91-5404fe8d0be8","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":226,"board":{"height":11,"width":11,"snakes":[{"id":"8a1cf727-771b-440b-b184-7357ef44aa85","name":"Nightwing","latency":"182","health":96,"body":[{"x":1,"y":7},{"x":2,"y":7},{"x":2,"y":8},{"x":2,"y":9},{"x":2,"y":10},{"x":3,"y":10},{"x":3,"y":9},{"x":4,"y":9},{"x":5,"y":9},{"x":5,"y":10},{"x":6,"y":10},{"x":7,"y":10},{"x":8,"y":10},{"x":9,"y":10}],"head":{"x":1,"y":7},"length":14,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"ced01f1e-7493-44a2-8816-446e83528422","name":"Rick2","latency":"124","health":95,"body":[{"x":4,"y":4},{"x":5,"y":4},{"x":5,"y":5},{"x":6,"y":5},{"x":6,"y":6},{"x":7,"y":6},{"x":8,"y":6},{"x":9,"y":6},{"x":9,"y":5},{"x":9,"y":4},{"x":10,"y":4},{"x":10,"y":3},{"x":9,"y":3},{"x":9,"y":2},{"x":9,"y":1},{"x":8,"y":1},{"x":7,"y":1},{"x":6,"y":1}],"head":{"x":4,"y":4},"length":18,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}],"food":[{"x":3,"y":3},{"x":8,"y":2},{"x":5,"y":1}],"hazards":[]},"you":{"id":"c71b5283-26d6-4077-ba2a-1b593564ae85","name":"Rick3","latency":"171","health":74,"body":[{"x":0,"y":6},{"x":0,"y":7},{"x":0,"y":8},{"x":0,"y":9}],"head":{"x":0,"y":6},"length":4,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}}}
game_state = {"game": {"id": "7b0452d3-a738-4e19-be93-da148e2a1e53", "ruleset": {"name": "standard", "version": "cli",
                                                                                 "settings": {"foodSpawnChance": 15,
                                                                                              "minimumFood": 1,
                                                                                              "hazardDamagePerTurn": 14,
                                                                                              "hazardMap": "",
                                                                                              "hazardMapAuthor": "",
                                                                                              "royale": {
                                                                                                  "shrinkEveryNTurns": 25},
                                                                                              "squad": {
                                                                                                  "allowBodyCollisions": False,
                                                                                                  "sharedElimination": False,
                                                                                                  "sharedHealth": False,
                                                                                                  "sharedLength": False}}},
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 18,
              "board": {"height": 11, "width": 11, "snakes": [
                  {"id": "23a550b8-8365-41c3-a50c-ab311f034748", "name": "Nightwing", "latency": "514", "health": 84,
                   "body": [{"x": 7, "y": 3}, {"x": 6, "y": 3}, {"x": 5, "y": 3}, {"x": 4, "y": 3}],
                   "head": {"x": 7, "y": 3}, "length": 4, "shout": "", "squad": "",
                   "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}},
                  {"id": "12a17dfe-093f-4e94-9308-e115daf95fad", "name": "JonK2", "latency": "15", "health": 88,
                   "body": [{"x": 6, "y": 4}, {"x": 7, "y": 4}, {"x": 8, "y": 4}, {"x": 8, "y": 3}, {"x": 9, "y": 3}],
                   "head": {"x": 6, "y": 4}, "length": 5, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}},
                  {"id": "e11cc612-fe9a-44ae-8e11-e1d53db78d49", "name": "Rick2", "latency": "116", "health": 92,
                   "body": [{"x": 7, "y": 7}, {"x": 7, "y": 6}, {"x": 8, "y": 6}, {"x": 8, "y": 7}, {"x": 9, "y": 7}],
                   "head": {"x": 7, "y": 7}, "length": 5, "shout": "", "squad": "",
                   "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}},
                  {"id": "61a555e3-c09f-424b-b132-706eff747d2c", "name": "Rick3", "latency": "146", "health": 82,
                   "body": [{"x": 9, "y": 9}, {"x": 9, "y": 8}, {"x": 10, "y": 8}], "head": {"x": 9, "y": 9},
                   "length": 3, "shout": "", "squad": "",
                   "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}},
                  {"id": "dd064945-98bf-4b08-8b27-7fd2d1c94e88", "name": "JonK", "latency": "31", "health": 86,
                   "body": [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}, {"x": 5, "y": 8}, {"x": 5, "y": 9}],
                   "head": {"x": 5, "y": 5}, "length": 5, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}},
                  {"id": "ed3bda6b-5d39-4a18-9a2c-acd51ab70092", "name": "JonK3", "latency": "44", "health": 90,
                   "body": [{"x": 6, "y": 10}, {"x": 7, "y": 10}, {"x": 8, "y": 10}, {"x": 8, "y": 9},
                            {"x": 7, "y": 9}], "head": {"x": 6, "y": 10}, "length": 5, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}],
                        "food": [{"x": 6, "y": 5}], "hazards": []},
              "you": {"id": "dd064945-98bf-4b08-8b27-7fd2d1c94e88", "name": "JonK", "latency": "31", "health": 86,
                      "body": [{"x": 5, "y": 5}, {"x": 5, "y": 6}, {"x": 5, "y": 7}, {"x": 5, "y": 8},
                               {"x": 5, "y": 9}], "head": {"x": 5, "y": 5}, "length": 5, "shout": "", "squad": "",
                      "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
