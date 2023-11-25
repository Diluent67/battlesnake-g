import cv2
from skimage.segmentation import flood, flood_fill
from skimage import data, filters, color, morphology
import numpy as np
import time
from Board import Board

import cProfile, pstats


game_state = {'turn': 178, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 10}, {'x': 10, 'y': 9}], 'hazards': [], 'snakes': [{'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}, {'id': '46b6ee1d-6ed1-472b-ab03-53fff9c83431', 'name': 'JonK', 'health': 94, 'body': [{'x': 7, 'y': 3}, {'x': 8, 'y': 3}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1}, {'x': 10, 'y': 0}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 7, 'y': 0}, {'x': 6, 'y': 0}, {'x': 5, 'y': 0}, {'x': 4, 'y': 0}, {'x': 4, 'y': 1}, {'x': 4, 'y': 2}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}], 'head': {'x': 7, 'y': 3}, 'length': 18, 'food_eaten': None}]}, 'you': {'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}}
# game_state =  {'turn': 246, 'board': {'height': 11, 'width': 11, 'food': [{'x': 5, 'y': 5}], 'hazards': [], 'snakes': [{'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 87, 'body': [{'x': 10, 'y': 6}, {'x': 10, 'y': 5}, {'x': 10, 'y': 4}, {'x': 9, 'y': 4}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 8, 'y': 1}, {'x': 8, 'y': 2}, {'x': 8, 'y': 3}, {'x': 8, 'y': 4}, {'x': 8, 'y': 5}, {'x': 7, 'y': 5}, {'x': 7, 'y': 4}, {'x': 7, 'y': 3}], 'head': {'x': 10, 'y': 6}, 'length': 17, 'food_eaten': None}, {'id': '46b6ee1d-6ed1-472b-ab03-53fff9c83431', 'name': 'JonK', 'health': 98, 'body': [{'x': 9, 'y': 5}, {'x': 9, 'y': 6}, {'x': 9, 'y': 7}, {'x': 8, 'y': 7}, {'x': 7, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 5, 'y': 9}, {'x': 5, 'y': 10}, {'x': 4, 'y': 10}, {'x': 3, 'y': 10}, {'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 1, 'y': 9}, {'x': 0, 'y': 9}, {'x': 0, 'y': 8}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 1, 'y': 4}, {'x': 2, 'y': 4}, {'x': 2, 'y': 5}, {'x': 2, 'y': 6}, {'x': 1, 'y': 6}], 'head': {'x': 9, 'y': 5}, 'length': 26, 'food_eaten': None}]}, 'you': {'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 87, 'body': [{'x': 10, 'y': 6}, {'x': 10, 'y': 5}, {'x': 10, 'y': 4}, {'x': 9, 'y': 4}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 8, 'y': 1}, {'x': 8, 'y': 2}, {'x': 8, 'y': 3}, {'x': 8, 'y': 4}, {'x': 8, 'y': 5}, {'x': 7, 'y': 5}, {'x': 7, 'y': 4}, {'x': 7, 'y': 3}], 'head': {'x': 10, 'y': 6}, 'length': 17, 'food_eaten': None}}
you_id = game_state["you"]["id"]
board = Board(game_state)
board.update_board()
board.display()
print("\n")
board2 = board.board


start_pt = board.all_snakes[you_id].head.as_tuple()
board2[start_pt[0], start_pt[1]] = 0
for f in board.food:
    board2[f.x, f.y] = 0
board2 = board2.astype(np.uint8)

clock_in = time.time_ns()
# TIME
profiler = cProfile.Profile()
profiler.enable()

mask = np.zeros(np.asarray(board2.shape)+2, dtype=np.uint8)
retval, image2, mask, _ = cv2.floodFill(board2, mask, start_pt[::-1], 1, flags=4)
mask = mask[1:-1, 1:-1]
# contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# # Create a structuring element for dilation that only considers up/left/right/down neighbors
kernel = np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]], np.uint8)
dilated_array = cv2.dilate(mask, kernel, iterations=1)
# Find the edges by subtracting the original array from the dilated one
edge_array = dilated_array - mask
edge_coordinates = np.column_stack(np.where(edge_array == 1))
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()
print(f"Done OPENCV in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
# print(retval, edge_coordinates)


clock_in = time.time_ns()
profiler = cProfile.Profile()
profiler.enable()
a = board.fast_flood_fill(you_id, full_package=True, ff_split=True)
profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()
print(f"Done faster ff in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
# print(a)