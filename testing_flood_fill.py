import cv2
from skimage.segmentation import flood, flood_fill
from skimage import data, filters, color, morphology
import numpy as np
import time
from Board import Board



game_state = {'turn': 178, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 10}, {'x': 10, 'y': 9}], 'hazards': [], 'snakes': [{'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}, {'id': '46b6ee1d-6ed1-472b-ab03-53fff9c83431', 'name': 'JonK', 'health': 94, 'body': [{'x': 7, 'y': 3}, {'x': 8, 'y': 3}, {'x': 9, 'y': 3}, {'x': 9, 'y': 2}, {'x': 9, 'y': 1}, {'x': 10, 'y': 1}, {'x': 10, 'y': 0}, {'x': 9, 'y': 0}, {'x': 8, 'y': 0}, {'x': 7, 'y': 0}, {'x': 6, 'y': 0}, {'x': 5, 'y': 0}, {'x': 4, 'y': 0}, {'x': 4, 'y': 1}, {'x': 4, 'y': 2}, {'x': 4, 'y': 3}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}], 'head': {'x': 7, 'y': 3}, 'length': 18, 'food_eaten': None}]}, 'you': {'id': '30b31eb5-c9cf-48e7-9c40-b3824fff2cc3', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 0, 'y': 5}, {'x': 0, 'y': 4}, {'x': 0, 'y': 3}, {'x': 0, 'y': 2}, {'x': 1, 'y': 2}], 'head': {'x': 6, 'y': 10}, 'length': 16, 'food_eaten': None}}
game_state = {'turn': 40, 'board': {'height': 11, 'width': 11, 'food': [{'x': 8, 'y': 6}, {'x': 0, 'y': 7}], 'hazards': [], 'snakes': [{'id': '0a632f8a-7d27-4ab3-80a7-6005b27ae717', 'name': 'Nightwing', 'health': 60, 'body': [{'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}, {'x': 2, 'y': 7}], 'head': {'x': 2, 'y': 10}, 'length': 4, 'food_eaten': None}, {'id': '71595f3f-d14c-4ed3-b52a-33078d27f617', 'name': 'JonK', 'health': 76, 'body': [{'x': 6, 'y': 2}, {'x': 7, 'y': 2}, {'x': 7, 'y': 3}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}, {'x': 7, 'y': 4}, {'x': 8, 'y': 4}], 'head': {'x': 6, 'y': 2}, 'length': 7, 'food_eaten': None}, {'id': '26b61672-c5fc-4544-bc30-abbe33ad8f51', 'name': 'Einar', 'health': 91, 'body': [{'x': 6, 'y': 8}, {'x': 7, 'y': 8}, {'x': 7, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 6}, {'x': 6, 'y': 5}], 'head': {'x': 6, 'y': 8}, 'length': 6, 'food_eaten': None}, {'id': '774bf06f-6db3-4be7-8a3d-71830239b4aa', 'name': 'JonK2', 'health': 96, 'body': [{'x': 3, 'y': 5}, {'x': 4, 'y': 5}, {'x': 4, 'y': 4}, {'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 2, 'y': 3}, {'x': 2, 'y': 2}, {'x': 3, 'y': 2}], 'head': {'x': 3, 'y': 5}, 'length': 8, 'food_eaten': None}, {'id': '56833b6d-0925-44e2-a8d0-1777436c0694', 'name': 'Matt', 'health': 58, 'body': [{'x': 4, 'y': 2}, {'x': 4, 'y': 1}, {'x': 3, 'y': 1}], 'head': {'x': 4, 'y': 2}, 'length': 3, 'food_eaten': None}, {'id': '7b81e55d-2bf2-4ac2-99fe-78597e98b7c1', 'name': 'Glynn', 'health': 60, 'body': [{'x': 6, 'y': 10}, {'x': 7, 'y': 10}, {'x': 7, 'y': 9}, {'x': 6, 'y': 9}], 'head': {'x': 6, 'y': 10}, 'length': 4, 'food_eaten': None}]}, 'you': {'id': '0a632f8a-7d27-4ab3-80a7-6005b27ae717', 'name': 'Nightwing', 'health': 60, 'body': [{'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}, {'x': 2, 'y': 7}], 'head': {'x': 2, 'y': 10}, 'length': 4, 'food_eaten': None}}
you_id = game_state["you"]["id"]
board = Board(game_state)
board.update_board()
board.display()
board2 = board.board
# board = np.zeros((11,11))
# for i in range(5):
#     board[i][i] = 1
start_pt = board.all_snakes[you_id].head.as_tuple()
board2[start_pt[0], start_pt[1]] = 0

# numeric_matrix = board2.astype(np.uint8)
# mask = np.zeros(np.asarray(numeric_matrix.shape)+2, dtype=np.uint8)
# clock_in = time.time_ns()
# h2, _, _, _ = cv2.floodFill(numeric_matrix, mask, start_pt[::-1], 50, flags=4)
# mask = 1 - mask[1:-1, 1:-1]
# contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# # h = (numeric_matrix==50).sum()
# # contours = np.vstack(contours[0])
# # conts = [[x[1]-1, x[0]-1] for x in np.vstack(contours[0]).squeeze()]
# print(h2)
# print(f"Done OPENCV in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

# for i in range(5):
#     board.board[i][i+2] = "1"
board = Board(game_state)
board.update_board()
board2 = board.board
clock_in = time.time_ns()
space_ra, space_all, ff_bounds, touch_opps = board.flood_fill(you_id, full_package=True, ff_split=True)
# print(sorted([f.as_tuple() for f in ff_bounds], key=lambda x: x[0])) , [f.as_tuple() for f in ff_bounds], touch_opps
print(space_ra, space_all)
print(f"Done original in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

clock_in = time.time_ns()
a = board.fast_flood_fill(you_id, full_package=True, ff_split=True)
print(a)
print(f"Done faster ff in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")



# board = np.zeros((11,11))
# for i in range(5):
#     board[i][i] = 1
board = Board(game_state)
board.update_board()
board2 = board.board
clock_in = time.time_ns()
board2[0,2] = 0
filled_board = flood_fill(board2, (0,2), 55)
h = (filled_board==55).sum()
print(h)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")






# mask = mask[1:-1, 1:-1]
# matrix_np[mask==1] = "c"
# matrix = matrix_np.tolist()