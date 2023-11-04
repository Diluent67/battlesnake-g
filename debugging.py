from snake_engine import Battlesnake

game_state = {"game": {"id": "8533c7c3-8372-4d85-acc4-4954d5c0aa4b", "ruleset": {"name": "standard", "version": "cli",
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
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 178,
              "board": {"height": 11, "width": 11, "snakes": [
                  {"id": "30b31eb5-c9cf-48e7-9c40-b3824fff2cc3", "name": "Nightwing", "latency": "351", "health": 100,
                   "body": [{"x": 6, "y": 8}, {"x": 5, "y": 8}, {"x": 4, "y": 8}, {"x": 3, "y": 8}, {"x": 3, "y": 7},
                            {"x": 2, "y": 7}, {"x": 1, "y": 7}, {"x": 0, "y": 7}, {"x": 0, "y": 6}, {"x": 0, "y": 5},
                            {"x": 0, "y": 4}, {"x": 0, "y": 3}, {"x": 0, "y": 2}, {"x": 1, "y": 2}, {"x": 1, "y": 3},
                            {"x": 1, "y": 3}], "head": {"x": 6, "y": 8}, "length": 16, "shout": "", "squad": "",
                   "customizations": {"color": "#3333ff", "head": "ski", "tail": "mystic-moon"}},
                  {"id": "46b6ee1d-6ed1-472b-ab03-53fff9c83431", "name": "JonK", "latency": "23", "health": 96,
                   "body": [{"x": 9, "y": 3}, {"x": 9, "y": 2}, {"x": 9, "y": 1}, {"x": 10, "y": 1}, {"x": 10, "y": 0},
                            {"x": 9, "y": 0}, {"x": 8, "y": 0}, {"x": 7, "y": 0}, {"x": 6, "y": 0}, {"x": 5, "y": 0},
                            {"x": 4, "y": 0}, {"x": 4, "y": 1}, {"x": 4, "y": 2}, {"x": 4, "y": 3}, {"x": 4, "y": 4},
                            {"x": 5, "y": 4}, {"x": 6, "y": 4}, {"x": 7, "y": 4}], "head": {"x": 9, "y": 3},
                   "length": 18, "shout": "", "squad": "",
                   "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}],
                        "food": [{"x": 9, "y": 10}, {"x": 10, "y": 9}], "hazards": []},
              "you": {"id": "ad40b1ef-e988-45ab-a06d-ad3f0e060f91", "name": "Glynn", "latency": "135", "health": 88,
                      "body": [{"x": 6, "y": 2}, {"x": 5, "y": 2}, {"x": 4, "y": 2}], "head": {"x": 6, "y": 2},
                      "length": 3, "shout": "", "squad": "",
                      "customizations": {"color": "#6600ff", "head": "all-seeing", "tail": "weight"}}}

next_move = Battlesnake(game_state, debugging=True).optimal_move()
print(next_move)