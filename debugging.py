from snake_engine import Battlesnake
import time

# aggression
game_state = {"game":{"id":"60e1b749-34f3-4558-9940-5a9f0e48a6cd","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":221,"board":{"height":11,"width":11,"snakes":[{"id":"2698362f-d048-48ac-9606-ca78e22e4099","name":"Einar","latency":"92","health":90,"body":[{"x":2,"y":5},{"x":3,"y":5},{"x":3,"y":4},{"x":3,"y":3},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":4,"y":6},{"x":4,"y":7},{"x":4,"y":8},{"x":4,"y":9},{"x":3,"y":9},{"x":2,"y":9},{"x":1,"y":9},{"x":0,"y":9},{"x":0,"y":8},{"x":0,"y":7},{"x":0,"y":6},{"x":0,"y":5},{"x":0,"y":4},{"x":0,"y":3},{"x":0,"y":2},{"x":0,"y":1}],"head":{"x":2,"y":5},"length":23,"shout":"","squad":"","customizations":{"color":"#4A412A","head":"shades","tail":"sharp"}},{"id":"70356921-27a0-4af4-8281-6eb38e35b574","name":"Nightwing","latency":"140","health":80,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":5,"y":2},{"x":6,"y":2},{"x":6,"y":3},{"x":5,"y":3},{"x":5,"y":4},{"x":5,"y":5},{"x":6,"y":5},{"x":7,"y":5},{"x":7,"y":6},{"x":8,"y":6},{"x":8,"y":7},{"x":9,"y":7},{"x":9,"y":6},{"x":9,"y":5},{"x":9,"y":4},{"x":9,"y":3}],"head":{"x":3,"y":2},"length":18,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}],"food":[{"x":1,"y":5}],"hazards":[]},"you":{"id":"11937642-f2c6-49f2-a135-fdd78d4aa332","name":"Jesse","latency":"31","health":94,"body":[{"x":3,"y":3},{"x":3,"y":4},{"x":3,"y":3}],"head":{"x":3,"y":3},"length":3,"shout":"","squad":"","customizations":{"color":"#E04C07","head":"missile","tail":"nr-booster"}}}
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

b = Battlesnake(game_state, debugging=True)
clock_in = time.time_ns()
peripheral_ra = b.board.flood_fill(b.you.id, risk_averse=True, confined_area="auto")
peripheral_all = b.board.flood_fill(b.you.id, risk_averse=False, confined_area="auto")
print(f"Total time: {round((time.time_ns() - clock_in) / 1000000, 3)}")
clock_in = time.time_ns()
peripheral_ra2, peripheral_all2, _, peripheral_touch_opps = b.board.flood_fill(b.you.id, confined_area="auto",
                                                                                  full_package=True)
print(f"Total time: {round((time.time_ns() - clock_in) / 1000000, 3)}")

clock_in = time.time_ns()
print(f"\nBest move: {b.optimal_move()}")
print(f"Total time: {round((time.time_ns() - clock_in) / 1000000, 3)}")
