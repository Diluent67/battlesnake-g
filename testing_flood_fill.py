import cv2
from skimage.segmentation import flood, flood_fill
from skimage import data, filters, color, morphology
import numpy as np
import time
from Board import Board

import cProfile, pstats

ff_split = False
game_state = {'turn': 178, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 10}, {'x': 10, 'y': 9}], 'hazards': [], 'snakes': [{'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}, {'id': '46b6ee1d-6ed1-472b-ab03-53fff9c83431', 'name': 'JonK', 'health': 94, 'body': [{'x': 7, 'y': 3}, {'x': 8, 'y': 3}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1}, {'x': 10, 'y': 0}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 7, 'y': 0}, {'x': 6, 'y': 0}, {'x': 5, 'y': 0}, {'x': 4, 'y': 0}, {'x': 4, 'y': 1}, {'x': 4, 'y': 2}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}], 'head': {'x': 7, 'y': 3}, 'length': 18, 'food_eaten': None}]}, 'you': {'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}}
game_state =  {'turn': 246, 'board': {'height': 11, 'width': 11, 'food': [{'x': 5, 'y': 5}], 'hazards': [], 'snakes': [{'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 87, 'body': [{'x': 10, 'y': 6}, {'x': 10, 'y': 5}, {'x': 10, 'y': 4}, {'x': 9, 'y': 4}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 8, 'y': 1}, {'x': 8, 'y': 2}, {'x': 8, 'y': 3}, {'x': 8, 'y': 4}, {'x': 8, 'y': 5}, {'x': 7, 'y': 5}, {'x': 7, 'y': 4}, {'x': 7, 'y': 3}], 'head': {'x': 10, 'y': 6}, 'length': 17, 'food_eaten': None}, {'id': '46b6ee1d-6ed1-472b-ab03-53fff9c83431', 'name': 'JonK', 'health': 98, 'body': [{'x': 9, 'y': 5}, {'x': 9, 'y': 6}, {'x': 9, 'y': 7}, {'x': 8, 'y': 7}, {'x': 7, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 5, 'y': 9}, {'x': 5, 'y': 10}, {'x': 4, 'y': 10}, {'x': 3, 'y': 10}, {'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 1, 'y': 9}, {'x': 0, 'y': 9}, {'x': 0, 'y': 8}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4}, {'x': 2, 'y': 5}, {'x': 2, 'y': 6}, {'x': 1, 'y': 6}], 'head': {'x': 9, 'y': 5}, 'length': 26, 'food_eaten': None}]}, 'you': {'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 87, 'body': [{'x': 10, 'y': 6}, {'x': 10, 'y': 5}, {'x': 10, 'y': 4}, {'x': 9, 'y': 4}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 8, 'y': 1}, {'x': 8, 'y': 2}, {'x': 8, 'y': 3}, {'x': 8, 'y': 4}, {'x': 8, 'y': 5}, {'x': 7, 'y': 5}, {'x': 7, 'y': 4}, {'x': 7, 'y': 3}], 'head': {'x': 10, 'y': 6}, 'length': 17, 'food_eaten': None}}
game_state = {"game":{"id":"0eecf020-5cc2-4da5-adb4-33d2fabc580b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":63,"board":{"height":11,"width":11,"snakes":[{"id":"63f6454f-3f0b-4959-a46a-b6173bf97d9f","name":"JonK","latency":"24","health":85,"body":[{"x":6,"y":1},{"x":7,"y":1},{"x":8,"y":1},{"x":9,"y":1},{"x":10,"y":1},{"x":10,"y":2},{"x":10,"y":3},{"x":10,"y":4},{"x":10,"y":5}],"head":{"x":6,"y":1},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"73ec1a21-05e9-40da-854d-70e7562141ba","name":"Rick2","latency":"138","health":90,"body":[{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":6,"y":4},{"x":6,"y":3},{"x":7,"y":3},{"x":7,"y":2}],"head":{"x":3,"y":4},"length":7,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"e995934c-190f-4e1f-ae73-9623eae1ad42","name":"Nightwing","latency":"88","health":95,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":4,"y":1},{"x":3,"y":1},{"x":3,"y":0},{"x":2,"y":0}],"head":{"x":3,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"ac9551aa-67aa-403e-bdea-68637eafa25e","name":"Rick","latency":"138","health":49,"body":[{"x":3,"y":6},{"x":3,"y":5},{"x":4,"y":5},{"x":5,"y":5},{"x":5,"y":6},{"x":5,"y":7}],"head":{"x":3,"y":6},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"5ef4a0b9-14fe-49e5-9614-4a045cc95a15","name":"Matt","latency":"37","health":94,"body":[{"x":1,"y":2},{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5},{"x":0,"y":5},{"x":0,"y":4}],"head":{"x":1,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#1f9490","head":"default","tail":"default"}}],"food":[{"x":6,"y":5}],"hazards":[]},"you":{"id":"e995934c-190f-4e1f-ae73-9623eae1ad42","name":"Nightwing","latency":"88","health":95,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":4,"y":1},{"x":3,"y":1},{"x":3,"y":0},{"x":2,"y":0}],"head":{"x":3,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}

you_id = game_state["you"]["id"]
board = Board(game_state)
board.update_board()
board.display()
print("\n")
board2 = board.board

# import copy
# clock_in = time.time_ns()
# board55 = copy.deepcopy(board2).astype(np.uint8)
# print(f"Ran deepcopy {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
#
# clock_in = time.time_ns()
# board55 = board2.astype(np.uint8)
# for f in board.food:
#     board55[f.x, f.y] = 0
#
# for f in board.food:
#     board55[f.x, f.y] = 100
# t = []
# for i in range(5):
#     for f in board.food:
#         t.append(f)
#
# print(f"Ran deepcopy {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
# # print(a)
#
# start_pt = board.all_snakes[you_id].head.as_tuple()
# board2[start_pt[0], start_pt[1]] = 0
# for f in board.food:
#     board2[f.x, f.y] = 0
# board2 = board2.astype(np.uint8)

# clock_in = time.time_ns()
# mask = np.zeros(np.asarray(board2.shape)+2, dtype=np.uint8)
# retval, image2, mask, _ = cv2.floodFill(board2, mask, start_pt[::-1], 1, flags=4)
# mask = mask[1:-1, 1:-1]
# # contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# # # Create a structuring element for dilation that only considers up/left/right/down neighbors
# kernel = np.array([[0, 1, 0],
#                    [1, 1, 1],
#                    [0, 1, 0]], np.uint8)
# dilated_array = cv2.dilate(mask, kernel, iterations=1)
# # Find the edges by subtracting the original array from the dilated one
# edge_array = dilated_array - mask
# edge_coordinates = np.column_stack(np.where(edge_array == 1))
# print(f"Done OPENCV in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
# print(retval, edge_coordinates)

board = Board(game_state)
board.update_board()
clock_in = time.time_ns()
a = board.fast_flood_fill(you_id, full_package=True, ff_split=ff_split)
print(f"Done faster ff in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
print(a)




# for i in range(5):
#     board.board[i][i+2] = "1"
board = Board(game_state)
board.update_board()
board2 = board.board
clock_in = time.time_ns()
space_ra, space_all, ff_bounds, touch_opps = board.flood_fill(you_id, full_package=True, ff_split=ff_split)
# print(sorted([f.as_tuple() for f in ff_bounds], key=lambda x: x[0])) , [f.as_tuple() for f in ff_bounds], touch_opps
print(f"Done original in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
print(space_ra, space_all, sorted([a.as_tuple() for a in ff_bounds]))



from Pos import Pos
po = Pos({"x": 8, "y": 3})
clock_in = time.time_ns()
if po in ff_bounds:
    print("A")
print(f"Found in og list of lists in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

# clock_in = time.time_ns()
# if [8,3] in a[-1]:
#     print("A")
# print(f"Found in fast list of lists in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
clock_in = time.time_ns()

if tuple([8,3]) in a[-1]:
    print("A")
print(f"Found in fast list of lists in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

# # board = np.zeros((11,11))
# # for i in range(5):
# #     board[i][i] = 1
# board = Board(game_state)
# board.update_board()
# board2 = board.board
# clock_in = time.time_ns()
# board2[0,2] = 0
# filled_board = flood_fill(board2, (0,2), 55)
# h = (filled_board==55).sum()
# print(h)
# print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")






# mask = mask[1:-1, 1:-1]
# matrix_np[mask==1] = "c"
# matrix = matrix_np.tolist()