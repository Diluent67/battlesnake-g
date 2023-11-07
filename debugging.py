from snake_engine import Battlesnake
import time

game_state = {"game": {"id": "8a5a7e1e-538b-453d-83df-e908a6f96a2b", "ruleset": {"name": "standard", "version": "cli",
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
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 93,
              "board": {"height": 11, "width": 11, "snakes": [
                  {"id": "79562f65-6955-4ec4-89ee-975fca9182ed", "name": "Nightwing", "latency": "78", "health": 70,
                   "body": [{"x": 3, "y": 10}, {"x": 3, "y": 9}, {"x": 2, "y": 9}, {"x": 1, "y": 9}, {"x": 1, "y": 8},
                            {"x": 0, "y": 8}, {"x": 0, "y": 7}], "head": {"x": 3, "y": 10}, "length": 7, "shout": "",
                   "squad": "", "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}},
                  {"id": "78838e38-a6aa-4bb9-a9d0-737a895fbf33", "name": "Rick", "latency": "129", "health": 54,
                   "body": [{"x": 2, "y": 7}, {"x": 3, "y": 7}, {"x": 3, "y": 6}, {"x": 4, "y": 6}, {"x": 5, "y": 6},
                            {"x": 6, "y": 6}, {"x": 6, "y": 5}], "head": {"x": 2, "y": 7}, "length": 7, "shout": "",
                   "squad": "", "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}},
                  {"id": "702e6cfd-dde1-4cc7-bedd-128e04fe1bac", "name": "Rick3", "latency": "138", "health": 91,
                   "body": [{"x": 4, "y": 7}, {"x": 4, "y": 8}, {"x": 5, "y": 8}, {"x": 6, "y": 8}, {"x": 7, "y": 8},
                            {"x": 8, "y": 8}, {"x": 8, "y": 9}, {"x": 7, "y": 9}, {"x": 6, "y": 9}],
                   "head": {"x": 4, "y": 7}, "length": 9, "shout": "", "squad": "",
                   "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}},
                  {"id": "88a19cd6-834b-4358-b573-175c47d751a8", "name": "JonK", "latency": "13", "health": 100,
                   "body": [{"x": 1, "y": 6}, {"x": 0, "y": 6}, {"x": 0, "y": 5}, {"x": 1, "y": 5}, {"x": 2, "y": 5},
                            {"x": 3, "y": 5}, {"x": 4, "y": 5}, {"x": 4, "y": 4}, {"x": 4, "y": 3}, {"x": 4, "y": 2},
                            {"x": 4, "y": 1}, {"x": 4, "y": 1}], "head": {"x": 1, "y": 6}, "length": 12, "shout": "",
                   "squad": "", "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}],
                        "food": [{"x": 0, "y": 1}], "hazards": []},
              "you": {"id": "79562f65-6955-4ec4-89ee-975fca9182ed", "name": "Nightwing", "latency": "78", "health": 70,
                      "body": [{"x": 3, "y": 10}, {"x": 3, "y": 9}, {"x": 2, "y": 9}, {"x": 1, "y": 9},
                               {"x": 1, "y": 8}, {"x": 0, "y": 8}, {"x": 0, "y": 7}], "head": {"x": 3, "y": 10},
                      "length": 7, "shout": "", "squad": "",
                      "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}}}

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
print(b.optimal_move())
total_time = round((time.time_ns() - clock_in) / 1000000, 3)
print(total_time)
