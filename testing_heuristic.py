from snake_engine import Battlesnake
import numpy as np


game_state = {'turn': 194, 'board': {'height': 11, 'width': 11, 'food': [{'x': 0, 'y': 0}], 'hazards': [], 'snakes': [{'id': 'gs_ttqMrvHMrDhVb3XGbBcvDw6c', 'name': 'Nightwing', 'health': 89, 'body': [{'x': 2, 'y': 8}, {'x': 3, 'y': 8}, {'x': 4, 'y': 8}, {'x': 4, 'y': 7}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 5, 'y': 9}, {'x': 6, 'y': 9}, {'x': 6, 'y': 10}, {'x': 7, 'y': 10}, {'x': 7, 'y': 9}, {'x': 7, 'y': 8}, {'x': 8, 'y': 8}, {'x': 9, 'y': 8}, {'x': 9, 'y': 7}], 'head': {'x': 2, 'y': 8}, 'length': 17, 'food_eaten': None}, {'id': 'gs_tXxjRDpbqt4rvqdY3tydJXgT', 'name': 'Shapeshifter', 'health': 98, 'body': [{'x': 2, 'y': 4}, {'x': 3, 'y': 4}, {'x': 4, 'y': 4}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}, {'x': 6, 'y': 5}, {'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 4, 'y': 6}, {'x': 3, 'y': 6}, {'x': 3, 'y': 5}, {'x': 2, 'y': 5}, {'x': 1, 'y': 5}, {'x': 1, 'y': 4}, {'x': 1, 'y': 3}], 'head': {'x': 2, 'y': 4}, 'length': 15, 'food_eaten': None}, {'id': 'gs_WBqhg4jBfMFF4cxtVVkvxtD9', 'name': 'Spaceheater⠀', 'health': 44, 'body': [{'x': 3, 'y': 9}, {'x': 2, 'y': 9}, {'x': 2, 'y': 10}, {'x': 1, 'y': 10}, {'x': 0, 'y': 10}, {'x': 0, 'y': 9}, {'x': 0, 'y': 8}, {'x': 0, 'y': 7}, {'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}], 'head': {'x': 3, 'y': 9}, 'length': 12, 'food_eaten': None}]}, 'you': {'id': 'gs_ttqMrvHMrDhVb3XGbBcvDw6c', 'name': 'Nightwing', 'health': 89, 'body': [{'x': 2, 'y': 8}, {'x': 3, 'y': 8}, {'x': 4, 'y': 8}, {'x': 4, 'y': 7}, {'x': 5, 'y': 7}, {'x': 6, 'y': 7}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}, {'x': 5, 'y': 9}, {'x': 6, 'y': 9}, {'x': 6, 'y': 10}, {'x': 7, 'y': 10}, {'x': 7, 'y': 9}, {'x': 7, 'y': 8}, {'x': 8, 'y': 8}, {'x': 9, 'y': 8}, {'x': 9, 'y': 7}], 'head': {'x': 2, 'y': 8}, 'length': 17, 'food_eaten': None}}
b = Battlesnake(game_state, debugging=True)
b.board.update_board()
h = b.heuristic(tree_depth=1)
print(h)

# game_state = {'turn': 28, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 9}], 'hazards': [], 'snakes': [{'id': '9056e000-4397-46b6-b321-06b8b1bd12b5', 'name': 'Nightwing', 'health': 94, 'body': [{'x': 9, 'y': 4}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}, {'x': 8, 'y': 2}, {'x': 8, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 4}, 'length': 6, 'food_eaten': None}, {'id': '6bd34103-09ec-47e6-8598-8ac6d0ff1b09', 'name': 'JonK2', 'health': 95, 'body': [{'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 2, 'y': 8}, {'x': 2, 'y': 9}, {'x': 2, 'y': 10}, {'x': 1, 'y': 10}, {'x': 1, 'y': 9}], 'head': {'x': 4, 'y': 8}, 'length': 7, 'food_eaten': None}, {'id': 'e4c107b4-6897-4d79-8c8a-138693b5188a', 'name': 'Rick3', 'health': 76, 'body': [{'x': 4, 'y': 4}, {'x': 4, 'y': 3}, {'x': 5, 'y': 3}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}], 'head': {'x': 4, 'y': 4}, 'length': 5, 'food_eaten': None}, {'id': '786748dc-dc17-4c11-a435-079dd13f9916', 'name': 'JonK', 'health': 74, 'body': [{'x': 5, 'y': 5}, {'x': 4, 'y': 5}, {'x': 3, 'y': 5}, {'x': 2, 'y': 5}], 'head': {'x': 5, 'y': 5}, 'length': 4, 'food_eaten': None}, {'id': '0078b037-c58e-4b18-b783-6eed306ab57e', 'name': 'Rick', 'health': 72, 'body': [{'x': 7, 'y': 9}, {'x': 6, 'y': 9}, {'x': 5, 'y': 9}], 'head': {'x': 7, 'y': 9}, 'length': 3, 'food_eaten': None}]}, 'you': {'id': '9056e000-4397-46b6-b321-06b8b1bd12b5', 'name': 'Nightwing', 'health': 94, 'body': [{'x': 9, 'y': 4}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}, {'x': 8, 'y': 2}, {'x': 8, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 4}, 'length': 6, 'food_eaten': None}}
# b = Battlesnake(game_state, debugging=True)
# print(b.optimal_move())