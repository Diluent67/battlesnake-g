from snake_engine import Battlesnake
import time
import numpy as np

print("\n\n")
clock_in = time.time_ns()
for i in range(5000):
    a = {"x": 5, "y": 10}
    h = a["x"]
    j = a["y"]
a = {"x": 5, "y": 10}
for i in range(5000):
    h = a["x"]
    j = a["y"]
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")

print("\n\n")
a = {"x": 5, "y": 1}
b = (5, 1)
clock_in = time.time_ns()
for i in range(5000):
    if isinstance(a, dict):
        h = a["x"]
        j = a["y"]
    else:
        h = b[0]
        j = b[1]
for i in range(5000):
    if isinstance(b, dict):
        h = a["x"]
        j = a["y"]
    else:
        h = b[0]
        j = b[1]
print(f"Done in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")




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
