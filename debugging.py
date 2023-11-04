from snake_engine import Battlesnake

game_state = {"game": {"id": "28ed1cda-afe6-4d05-a566-8d2cf0a8f2af", "ruleset": {"name": "standard", "version": "cli",
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
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 167,
              "board": {"height": 11, "width": 11, "snakes": [
                  {"id": "855756ea-d478-48ef-a45f-d86ab19f268c", "name": "Nightwing", "latency": "297", "health": 84,
                   "body": [{"x": 7, "y": 4}, {"x": 6, "y": 4}, {"x": 6, "y": 3}, {"x": 5, "y": 3}, {"x": 5, "y": 2},
                            {"x": 5, "y": 1}, {"x": 6, "y": 1}, {"x": 6, "y": 2}, {"x": 7, "y": 2}, {"x": 7, "y": 3},
                            {"x": 8, "y": 3}], "head": {"x": 7, "y": 4}, "length": 11, "shout": "", "squad": "",
                   "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}},
                  {"id": "21763327-6d6e-4028-87d8-5060b1e6fa4d", "name": "JonK2", "latency": "29", "health": 95,
                   "body": [{"x": 8, "y": 1}, {"x": 7, "y": 1}, {"x": 7, "y": 0}, {"x": 6, "y": 0}, {"x": 5, "y": 0},
                            {"x": 4, "y": 0}, {"x": 3, "y": 0}, {"x": 2, "y": 0}, {"x": 2, "y": 1}, {"x": 2, "y": 2},
                            {"x": 2, "y": 3}, {"x": 3, "y": 3}, {"x": 3, "y": 4}, {"x": 3, "y": 5}, {"x": 4, "y": 5},
                            {"x": 4, "y": 6}, {"x": 5, "y": 6}, {"x": 5, "y": 5}], "head": {"x": 8, "y": 1},
                   "length": 18, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}},
                  {"id": "3bd0031c-3c56-4356-b93a-f2bbbe26751f", "name": "Rick2", "latency": "116", "health": 35,
                   "body": [{"x": 2, "y": 7}, {"x": 3, "y": 7}, {"x": 4, "y": 7}, {"x": 5, "y": 7}, {"x": 6, "y": 7},
                            {"x": 6, "y": 8}, {"x": 5, "y": 8}, {"x": 4, "y": 8}, {"x": 3, "y": 8}],
                   "head": {"x": 2, "y": 7}, "length": 9, "shout": "", "squad": "",
                   "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}}],
                        "food": [{"x": 9, "y": 2}], "hazards": []},
              "you": {"id": "d8e1d216-97a9-41c5-905c-be866dc9fb39", "name": "Rick", "latency": "183", "health": 100,
                      "body": [{"x": 5, "y": 0}, {"x": 6, "y": 0}, {"x": 7, "y": 0}, {"x": 8, "y": 0},
                               {"x": 8, "y": 0}], "head": {"x": 5, "y": 0}, "length": 5, "shout": "", "squad": "",
                      "customizations": {"color": "#00ff00", "head": "shark", "tail": "coffee"}}}

b = Battlesnake(game_state, debugging=True)
print(b.optimal_move())
