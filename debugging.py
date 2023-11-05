from snake_engine import Battlesnake

game_state = {"game": {"id": "84eb7f1c-2027-417b-baf7-2f776ed2db41", "ruleset": {"name": "standard", "version": "cli",
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
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 190,
              "board": {"height": 11, "width": 11, "snakes": [
                  {"id": "d5b4e8ab-2b61-4957-8436-395dbaad78e2", "name": "Nightwing", "latency": "198", "health": 100,
                   "body": [{"x": 0, "y": 8}, {"x": 1, "y": 8}, {"x": 2, "y": 8}, {"x": 3, "y": 8}, {"x": 3, "y": 7},
                            {"x": 4, "y": 7}, {"x": 5, "y": 7}, {"x": 6, "y": 7}, {"x": 7, "y": 7}, {"x": 7, "y": 6},
                            {"x": 7, "y": 5}, {"x": 8, "y": 5}, {"x": 8, "y": 6}, {"x": 8, "y": 6}],
                   "head": {"x": 0, "y": 8}, "length": 14, "shout": "", "squad": "",
                   "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}},
                  {"id": "c04d0e8f-2e84-4206-8f08-d68b59f9d6b6", "name": "JonK", "latency": "17", "health": 100,
                   "body": [{"x": 0, "y": 4}, {"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}, {"x": 4, "y": 4},
                            {"x": 4, "y": 3}, {"x": 4, "y": 2}, {"x": 5, "y": 2}, {"x": 6, "y": 2}, {"x": 7, "y": 2},
                            {"x": 8, "y": 2}, {"x": 9, "y": 2}, {"x": 10, "y": 2}, {"x": 10, "y": 1}, {"x": 10, "y": 0},
                            {"x": 9, "y": 0}, {"x": 8, "y": 0}, {"x": 7, "y": 0}, {"x": 6, "y": 0}, {"x": 5, "y": 0},
                            {"x": 4, "y": 0}, {"x": 4, "y": 1}, {"x": 4, "y": 1}], "head": {"x": 0, "y": 4},
                   "length": 23, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}],
                        "food": [{"x": 9, "y": 10}, {"x": 0, "y": 5}], "hazards": []},
              "you": {"id": "a9e1996e-6e0a-4f07-bb79-ecb08b9797b8", "name": "Einar", "latency": "174", "health": 76,
                      "body": [{"x": 3, "y": 10}, {"x": 4, "y": 10}, {"x": 5, "y": 10}, {"x": 6, "y": 10},
                               {"x": 7, "y": 10}, {"x": 8, "y": 10}, {"x": 9, "y": 10}, {"x": 10, "y": 10},
                               {"x": 10, "y": 9}], "head": {"x": 3, "y": 10}, "length": 9, "shout": "", "squad": "",
                      "customizations": {"color": "#4A412A", "head": "shades", "tail": "sharp"}}}

b = Battlesnake(game_state, debugging=True)
print(b.optimal_move())
