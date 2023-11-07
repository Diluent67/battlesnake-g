from snake_engine import *

game_state = {"game": {"id": "2e5ebfcf-d9ec-4202-ab29-9f42f49cb027", "ruleset": {"name": "standard", "version": "cli",
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
                       "map": "standard", "timeout": 500, "source": ""}, "turn": 0, "board": {"height": 11, "width": 11,
                                                                                              "snakes": [{
                                                                                                             "id": "71595f3f-d14c-4ed3-b52a-33078d27f617",
                                                                                                             "name": "JonK",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 5,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 5,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 5,
                                                                                                                          "y": 9}],
                                                                                                             "head": {
                                                                                                                 "x": 5,
                                                                                                                 "y": 9},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#B7410E",
                                                                                                                 "head": "sleepy",
                                                                                                                 "tail": "offroad"}},
                                                                                                         {
                                                                                                             "id": "26b61672-c5fc-4544-bc30-abbe33ad8f51",
                                                                                                             "name": "Einar",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 9,
                                                                                                                          "y": 5},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 5},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 5}],
                                                                                                             "head": {
                                                                                                                 "x": 9,
                                                                                                                 "y": 5},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#4A412A",
                                                                                                                 "head": "shades",
                                                                                                                 "tail": "sharp"}},
                                                                                                         {
                                                                                                             "id": "774bf06f-6db3-4be7-8a3d-71830239b4aa",
                                                                                                             "name": "JonK2",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 5,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 5,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 5,
                                                                                                                          "y": 1}],
                                                                                                             "head": {
                                                                                                                 "x": 5,
                                                                                                                 "y": 1},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#B7410E",
                                                                                                                 "head": "sleepy",
                                                                                                                 "tail": "offroad"}},
                                                                                                         {
                                                                                                             "id": "0a632f8a-7d27-4ab3-80a7-6005b27ae717",
                                                                                                             "name": "Nightwing",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 1,
                                                                                                                          "y": 5},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 5},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 5}],
                                                                                                             "head": {
                                                                                                                 "x": 1,
                                                                                                                 "y": 5},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#3333ff",
                                                                                                                 "head": "ski",
                                                                                                                 "tail": "mystic-moon"}},
                                                                                                         {
                                                                                                             "id": "eef4ef01-a03d-439d-8e31-65cb20d7a1d9",
                                                                                                             "name": "Rick",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 9,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 1}],
                                                                                                             "head": {
                                                                                                                 "x": 9,
                                                                                                                 "y": 1},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#00ff00",
                                                                                                                 "head": "shark",
                                                                                                                 "tail": "coffee"}},
                                                                                                         {
                                                                                                             "id": "56833b6d-0925-44e2-a8d0-1777436c0694",
                                                                                                             "name": "Matt",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 1,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 1},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 1}],
                                                                                                             "head": {
                                                                                                                 "x": 1,
                                                                                                                 "y": 1},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#1f9490",
                                                                                                                 "head": "default",
                                                                                                                 "tail": "default"}},
                                                                                                         {
                                                                                                             "id": "7b81e55d-2bf2-4ac2-99fe-78597e98b7c1",
                                                                                                             "name": "Glynn",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 1,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 1,
                                                                                                                          "y": 9}],
                                                                                                             "head": {
                                                                                                                 "x": 1,
                                                                                                                 "y": 9},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#6600ff",
                                                                                                                 "head": "all-seeing",
                                                                                                                 "tail": "weight"}},
                                                                                                         {
                                                                                                             "id": "c421b7c4-4ed7-4d06-9967-e90f8108bbff",
                                                                                                             "name": "Jesse",
                                                                                                             "latency": "0",
                                                                                                             "health": 100,
                                                                                                             "body": [{
                                                                                                                          "x": 9,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 9},
                                                                                                                      {
                                                                                                                          "x": 9,
                                                                                                                          "y": 9}],
                                                                                                             "head": {
                                                                                                                 "x": 9,
                                                                                                                 "y": 9},
                                                                                                             "length": 3,
                                                                                                             "shout": "",
                                                                                                             "squad": "",
                                                                                                             "customizations": {
                                                                                                                 "color": "#E04C07",
                                                                                                                 "head": "missile",
                                                                                                                 "tail": "nr-booster"}}],
                                                                                              "food": [
                                                                                                  {"x": 6, "y": 10},
                                                                                                  {"x": 10, "y": 6},
                                                                                                  {"x": 6, "y": 0},
                                                                                                  {"x": 0, "y": 4},
                                                                                                  {"x": 8, "y": 0},
                                                                                                  {"x": 2, "y": 0},
                                                                                                  {"x": 2, "y": 10},
                                                                                                  {"x": 8, "y": 10},
                                                                                                  {"x": 5, "y": 5}],
                                                                                              "hazards": []},
              "you": {"id": "71595f3f-d14c-4ed3-b52a-33078d27f617", "name": "JonK", "latency": "0", "health": 100,
                      "body": [{"x": 5, "y": 9}, {"x": 5, "y": 9}, {"x": 5, "y": 9}], "head": {"x": 5, "y": 9},
                      "length": 3, "shout": "", "squad": "",
                      "customizations": {"color": "#B7410E", "head": "sleepy", "tail": "offroad"}}}

clock_in = time.time_ns()
game = Battlesnake(game_state, debugging=False)
print(game.optimal_move())
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")


import cProfile, pstats
profiler = cProfile.Profile()
profiler.enable()
game.optimal_move()
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()
print("\n\n")
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats()
# import timeit
# start = timeit.default_timer()
# print("The start time is :", start)
# next_move = game.flood_fill(game.my_id, confined_area="left")
# print("The difference of time is :",
#               timeit.default_timer() - start)
