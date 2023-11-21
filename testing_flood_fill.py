import cv2
from skimage.segmentation import flood, flood_fill
from skimage import data, filters, color, morphology
import numpy as np
import time
from Board import Board



game_state = {"game":{"id":"ee187fa6-1b1a-4ced-9783-f928d75e5b8c","ruleset":{"name":"standard","version":"?","settings":{"foodSpawnChance":15,"minimumFood":1}},"map":"standard","timeout":500,"source":"custom"},"turn":122,"board":{"width":11,"height":11,"food":[{"x":0,"y":0}],"hazards":[],"snakes":[{"id":"gs_v3QBMtmqBWRxYfmFyDHtJM88","name":"NightwingV2","health":100,"body":[{"x":0,"y":2},{"x":1,"y":2},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":3},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":5,"y":5},{"x":6,"y":5},{"x":7,"y":5},{"x":8,"y":5},{"x":8,"y":4},{"x":8,"y":4}],"latency":109,"head":{"x":0,"y":2},"length":14,"shout":"","squad":"","customizations":{"color":"#1f51ff","head":"silly","tail":"mlh-gene"}},{"id":"gs_mBj6TQXj3gq7rTmwx6tSWWy6","name":"Nightwing","health":96,"body":[{"x":5,"y":9},{"x":4,"y":9},{"x":3,"y":9},{"x":3,"y":8},{"x":4,"y":8},{"x":4,"y":7},{"x":3,"y":7},{"x":3,"y":6},{"x":4,"y":6},{"x":5,"y":6},{"x":6,"y":6},{"x":7,"y":6},{"x":8,"y":6}],"latency":118,"head":{"x":5,"y":9},"length":13,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}]},"you":{"id":"gs_v3QBMtmqBWRxYfmFyDHtJM88","name":"NightwingV2","health":100,"body":[{"x":0,"y":2},{"x":1,"y":2},{"x":2,"y":2},{"x":3,"y":2},{"x":3,"y":3},{"x":4,"y":3},{"x":4,"y":4},{"x":4,"y":5},{"x":5,"y":5},{"x":6,"y":5},{"x":7,"y":5},{"x":8,"y":5},{"x":8,"y":4},{"x":8,"y":4}],"latency":109,"head":{"x":0,"y":2},"length":14,"shout":"","squad":"","customizations":{"color":"#1f51ff","head":"silly","tail":"mlh-gene"}}}
board = Board(game_state["board"])
for i in range(5):
    board.board[i][i+2] = "0"
clock_in = time.time_ns()
h = board.flood_fill("gs_v3QBMtmqBWRxYfmFyDHtJM88")
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")


board = np.zeros((11,11))
for i in range(5):
    board[i][i] = 1
clock_in = time.time_ns()
filled_board = flood_fill(board, (2, 1), 2)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")




board = np.zeros((11,11))
for i in range(5):
    board[i][i] = -1
numeric_matrix = board.astype(np.uint8)
# mask = np.zeros(np.asarray(numeric_matrix.shape)+2, dtype=np.uint8)
start_pt = (2,1)
clock_in = time.time_ns()
cv2.floodFill(numeric_matrix, None, start_pt, 2, flags=4)
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

# mask = mask[1:-1, 1:-1]
# matrix_np[mask==1] = "c"
# matrix = matrix_np.tolist()