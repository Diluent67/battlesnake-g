import cv2
from skimage.segmentation import flood, flood_fill
from skimage import data, filters, color, morphology
import numpy as np
import time
from Board import Board



game_state = {"game":{"id":"33a97bbd-134c-4fec-bd17-f567b874b75c","ruleset":{"name":"standard","version":"?","settings":{"foodSpawnChance":15,"minimumFood":1}},"map":"standard","timeout":500,"source":"ladder"},"turn":65,"board":{"width":11,"height":11,"food":[{"x":5,"y":0}],"hazards":[],"snakes":[{"id":"gs_QKPTRHcq83p3kY3Yxt4QqdTC","name":"Snake Without Brain","health":93,"body":[{"x":5,"y":4},{"x":5,"y":5},{"x":5,"y":6},{"x":4,"y":6},{"x":4,"y":7},{"x":4,"y":8},{"x":4,"y":9},{"x":5,"y":9},{"x":5,"y":10},{"x":6,"y":10}],"latency":27,"head":{"x":5,"y":4},"length":10,"shout":"","squad":"","customizations":{"color":"#888888","head":"default","tail":"default"}},{"id":"gs_V7MwWk9PtCmMVdkGmHG4xJT3","name":"vongola","health":82,"body":[{"x":8,"y":1},{"x":8,"y":2},{"x":8,"y":3},{"x":8,"y":4},{"x":8,"y":5},{"x":9,"y":5},{"x":9,"y":6},{"x":9,"y":7}],"latency":180,"head":{"x":8,"y":1},"length":8,"shout":"","squad":"","customizations":{"color":"#f0c300","head":"tiger-king","tail":"tiger-tail"}},{"id":"gs_WY4QTYfxqMKBvJ836xdKy9kX","name":"SmikkelSnek","health":35,"body":[{"x":2,"y":3},{"x":2,"y":4},{"x":1,"y":4}],"latency":79,"head":{"x":2,"y":3},"length":3,"shout":"","squad":"","customizations":{"color":"#ff0000","head":"caffeine","tail":"coffee"}},{"id":"gs_d39SdY4bp6cvTYyqhghtX48b","name":"Nightwing","health":96,"body":[{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":3,"y":5},{"x":2,"y":5},{"x":2,"y":6}],"latency":195,"head":{"x":4,"y":1},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}]},"you":{"id":"gs_d39SdY4bp6cvTYyqhghtX48b","name":"Nightwing","health":96,"body":[{"x":4,"y":1},{"x":4,"y":2},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":3,"y":5},{"x":2,"y":5},{"x":2,"y":6}],"latency":195,"head":{"x":4,"y":1},"length":8,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}
board = Board(game_state)
board.update_board()
board.display()
board2 = board.board
# board = np.zeros((11,11))
# for i in range(5):
#     board[i][i] = 1
start_pt = board.all_snakes["gs_d39SdY4bp6cvTYyqhghtX48b"].head.as_tuple()
board2[start_pt[0], start_pt[1]] = 0

numeric_matrix = board2.astype(np.uint8)
mask = np.zeros(np.asarray(numeric_matrix.shape)+2, dtype=np.uint8)
clock_in = time.time_ns()
h2, _, _, _ = cv2.floodFill(numeric_matrix, mask, start_pt[::-1], 50, flags=4)
mask = 1 - mask[1:-1, 1:-1]
contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# h = (numeric_matrix==50).sum()
# contours = np.vstack(contours[0])
# conts = [[x[1]-1, x[0]-1] for x in np.vstack(contours[0]).squeeze()]
print(h2)
print(f"Done OPENCV in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

# for i in range(5):
#     board.board[i][i+2] = "1"
board = Board(game_state)
board.update_board()
board2 = board.board
clock_in = time.time_ns()
space_ra, space_all, ff_bounds, touch_opps = board.flood_fill("gs_d39SdY4bp6cvTYyqhghtX48b", full_package=True)
print(sorted([f.as_tuple() for f in ff_bounds], key=lambda x: x[0]))
print(space_ra, space_all, [f.as_tuple() for f in ff_bounds], touch_opps)
print(f"Done original in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

clock_in = time.time_ns()
a = board.fast_flood_fill("gs_d39SdY4bp6cvTYyqhghtX48b", full_package=True)
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