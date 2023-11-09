from snake_engine import Battlesnake
import time
import numpy as np


game_state = {'turn': 30, 'board': {'height': 11, 'width': 11, 'food': [], 'hazards': [], 'snakes': [{'id': '394e7449-3aae-4d0b-a85d-30dbe14dcc11', 'name': 'Nightwing', 'health': 72, 'body': [{'x': 0, 'y': 6}, {'x': 0, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}], 'head': {'x': 0, 'y': 6}, 'length': 4, 'food_eaten': None}, {'id': '5af5fbcb-1f86-422d-96ab-833ec49e660b', 'name': 'Rick4', 'health': 100, 'body': [{'x': 6, 'y': 6}, {'x': 6, 'y': 5}, {'x': 6, 'y': 4}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}, {'x': 4, 'y': 4}], 'head': {'x': 6, 'y': 6}, 'length': 6, 'food_eaten': None}, {'id': '822dfa8a-7502-4dd6-8cdc-591c8ff0b405', 'name': 'Rick', 'health': 95, 'body': [{'x': 8, 'y': 6}, {'x': 8, 'y': 7}, {'x': 8, 'y': 8}, {'x': 9, 'y': 8}, {'x': 10, 'y': 8}, {'x': 10, 'y': 7}], 'head': {'x': 8, 'y': 6}, 'length': 6, 'food_eaten': None}, {'id': '9610c627-687f-4b76-a77b-cb8536eacce1', 'name': 'JonK2', 'health': 76, 'body': [{'x': 7, 'y': 9}, {'x': 7, 'y': 10}, {'x': 8, 'y': 10}, {'x': 8, 'y': 9}, {'x': 9, 'y': 9}], 'head': {'x': 7, 'y': 9}, 'length': 5, 'food_eaten': None}, {'id': 'ed603536-f608-4398-8fb7-3ddd12867d73', 'name': 'Rick2', 'health': 91, 'body': [{'x': 0, 'y': 10}, {'x': 0, 'y': 9}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}, {'x': 2, 'y': 10}, {'x': 3, 'y': 10}], 'head': {'x': 0, 'y': 10}, 'length': 6, 'food_eaten': None}, {'id': '70f0fd83-753b-4cf4-8f4f-84f4f6679827', 'name': 'JonK', 'health': 70, 'body': [{'x': 8, 'y': 4}, {'x': 9, 'y': 4}, {'x': 9, 'y': 5}, {'x': 8, 'y': 5}], 'head': {'x': 8, 'y': 4}, 'length': 4, 'food_eaten': None}, {'id': '85720c44-c37e-4300-a85a-c222d31178cc', 'name': 'JonK3', 'health': 98, 'body': [{'x': 8, 'y': 0}, {'x': 9, 'y': 0}, {'x': 10, 'y': 0}, {'x': 10, 'y': 1}, {'x': 9, 'y': 1}, {'x': 8, 'y': 1}, {'x': 7, 'y': 1}, {'x': 7, 'y': 2}], 'head': {'x': 8, 'y': 0}, 'length': 8, 'food_eaten': None}]}, 'you': {'id': '394e7449-3aae-4d0b-a85d-30dbe14dcc11', 'name': 'Nightwing', 'health': 72, 'body': [{'x': 0, 'y': 6}, {'x': 0, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}], 'head': {'x': 0, 'y': 6}, 'length': 4, 'food_eaten': None}}
b = Battlesnake(game_state, debugging=True)
b.board.display()
# b.heuristic()
print("\n\n")
clock_in = time.time_ns()
print(b.board.flood_fill(b.you.id, risk_averse=True))  # 58
print(b.board.flood_fill(b.you.id, risk_averse=False))  # 78
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

space_left, opps = b.board.flood_fill(b.you.id, risk_averse=False, get_touching_opps=True)
print(f"Number of opp heads: {len(set(opps))}")
print(f"{[opp.as_tuple() for opp in opps]}")

_, boundaries = b.board.flood_fill(b.you.id, risk_averse=False,  get_boundaries=True)
boundaries = [opp.as_tuple() for opp in boundaries]
print(f"Number of bounds: {len(set(boundaries))}")
print(f"{sorted(boundaries)}")

clock_in = time.time_ns()
flood_fill, flood_fill_all, boundary_pos, heads_in_contact = b.board.flood_fill(b.you.id, risk_averse=True, full_package=True)
boundary_pos = [opp.as_tuple() for opp in boundary_pos]
print(flood_fill, flood_fill_all)
print(f"Number of opp heads: {len(heads_in_contact)}")
print(f"{sorted([opp.as_tuple() for opp in heads_in_contact])}")
print(f"Number of bounds: {len(set(boundary_pos))}")
print(f"{sorted(boundary_pos)}")
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

print([opp for opp in set(boundary_pos).difference(set(opps))])

# print("\n\n\n")
# aces = np.random.randint(100, size=1000)
# clock_in = time.time_ns()
# d = []
# for i in aces:
#     if i not in d:
#         d.append(i)
# print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
#
# clock_in = time.time_ns()
# d2 = set()
# for i in aces:
#     d2.add(i)
# print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
#
# print(len(d))
# print(len(d2))
#
