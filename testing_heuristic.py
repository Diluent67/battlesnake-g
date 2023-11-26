from snake_engine import Battlesnake
import numpy as np


game_state = {'turn': 187, 'board': {'height': 11, 'width': 11, 'food': [{'x': 2, 'y': 2}, {'x': 4, 'y': 0}], 'hazards': [], 'snakes': [{'id': 'gs_dVW9Hk6RBvjwPkdCGwv7hFtK', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 4, 'y': 3}, {'x': 4, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}, {'x': 2, 'y': 3}, {'x': 2, 'y': 4}, {'x': 2, 'y': 5}, {'x': 2, 'y': 6}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}, {'x': 3, 'y': 9}, {'x': 4, 'y': 9}, {'x': 5, 'y': 9}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}], 'head': {'x': 4, 'y': 3}, 'length': 19, 'food_eaten': None}, {'id': 'gs_qKcBJTP9Vx8ffjjmHW4CHFY8', 'name': 'CoolerestSnake!', 'health': 94, 'body': [{'x': 5, 'y': 4}, {'x': 5, 'y': 3}, {'x': 5, 'y': 2}, {'x': 5, 'y': 1}, {'x': 5, 'y': 0}, {'x': 6, 'y': 0}, {'x': 7, 'y': 0}, {'x': 8, 'y': 0}, {'x': 8, 'y': 1}, {'x': 8, 'y': 2}, {'x': 8, 'y': 3}, {'x': 8, 'y': 4}, {'x': 7, 'y': 4}, {'x': 6, 'y': 4}], 'head': {'x': 5, 'y': 4}, 'length': 14, 'food_eaten': None}, {'id': 'gs_6CCSqDqQfF3MVCppJtXhqQjc', 'name': 'ich heisse marvin', 'health': 57, 'body': [{'x': 7, 'y': 6}, {'x': 8, 'y': 6}, {'x': 8, 'y': 7}, {'x': 7, 'y': 7}, {'x': 6, 'y': 7}, {'x': 5, 'y': 7}, {'x': 5, 'y': 6}, {'x': 5, 'y': 5}], 'head': {'x': 7, 'y': 6}, 'length': 8, 'food_eaten': None}]}, 'you': {'id': 'gs_dVW9Hk6RBvjwPkdCGwv7hFtK', 'name': 'Nightwing', 'health': 98, 'body': [{'x': 4, 'y': 3}, {'x': 4, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}, {'x': 2, 'y': 3}, {'x': 2, 'y': 4}, {'x': 2, 'y': 5}, {'x': 2, 'y': 6}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}, {'x': 3, 'y': 9}, {'x': 4, 'y': 9}, {'x': 5, 'y': 9}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}, {'x': 5, 'y': 8}], 'head': {'x': 4, 'y': 3}, 'length': 19, 'food_eaten': None}}
b = Battlesnake(game_state, debugging=True)
b.board.update_board()
h = b.heuristic(tree_depth=1)
print(h)

# game_state = {'turn': 28, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 9}], 'hazards': [], 'snakes': [{'id': '9056e000-4397-46b6-b321-06b8b1bd12b5', 'name': 'Nightwing', 'health': 94, 'body': [{'x': 9, 'y': 4}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}, {'x': 8, 'y': 2}, {'x': 8, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 4}, 'length': 6, 'food_eaten': None}, {'id': '6bd34103-09ec-47e6-8598-8ac6d0ff1b09', 'name': 'JonK2', 'health': 95, 'body': [{'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 2, 'y': 8}, {'x': 2, 'y': 9}, {'x': 2, 'y': 10}, {'x': 1, 'y': 10}, {'x': 1, 'y': 9}], 'head': {'x': 4, 'y': 8}, 'length': 7, 'food_eaten': None}, {'id': 'e4c107b4-6897-4d79-8c8a-138693b5188a', 'name': 'Rick3', 'health': 76, 'body': [{'x': 4, 'y': 4}, {'x': 4, 'y': 3}, {'x': 5, 'y': 3}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}], 'head': {'x': 4, 'y': 4}, 'length': 5, 'food_eaten': None}, {'id': '786748dc-dc17-4c11-a435-079dd13f9916', 'name': 'JonK', 'health': 74, 'body': [{'x': 5, 'y': 5}, {'x': 4, 'y': 5}, {'x': 3, 'y': 5}, {'x': 2, 'y': 5}], 'head': {'x': 5, 'y': 5}, 'length': 4, 'food_eaten': None}, {'id': '0078b037-c58e-4b18-b783-6eed306ab57e', 'name': 'Rick', 'health': 72, 'body': [{'x': 7, 'y': 9}, {'x': 6, 'y': 9}, {'x': 5, 'y': 9}], 'head': {'x': 7, 'y': 9}, 'length': 3, 'food_eaten': None}]}, 'you': {'id': '9056e000-4397-46b6-b321-06b8b1bd12b5', 'name': 'Nightwing', 'health': 94, 'body': [{'x': 9, 'y': 4}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}, {'x': 8, 'y': 2}, {'x': 8, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 4}, 'length': 6, 'food_eaten': None}}
# b = Battlesnake(game_state, debugging=True)
# print(b.optimal_move())