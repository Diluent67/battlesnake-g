from __future__ import annotations
from typing import Optional, Union


class Pos:
    def __init__(self, x: Union[int, dict], y: int = None):
        """An (x, y) position, with many helper methods"""
        # Create from a dictionary with x and y keys, or as named parameters
        if isinstance(x, dict):
            if "x" not in x:
                raise Exception("Pos constructor dict has no 'x' key")
            elif "y" not in x:
                raise Exception("Pos constructor dict has no 'y' key")
            self.x = x["x"]
            self.y = x["y"]
        elif isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            if y is None:
                raise Exception("Pos constructor: no y value")
            self.x = x
            self.y = y

    def __copy__(self):
        return Pos(self.x, self.y)

    def __eq__(self, other):
        """Two points are equal if they have the same x and y"""
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(self.__str__())

    def as_dict(self):
        return {"x": self.x, "y": self.y}

    def as_tuple(self):
        return self.x, self.y

    def manhattan_dist(self, end: Pos):
        """Return the Manhattan distance to another position"""
        return sum(abs(value1 - value2) for value1, value2 in zip(self.as_tuple(), end.as_tuple()))

    def moved_to(self, direction, distance=1):
        """Return this position moved by 1 in a given direction"""
        if direction == "left":
            next_x = self.x - distance
            next_y = self.y
        elif direction == "right":
            next_x = self.x + distance
            next_y = self.y
        elif direction == "up":
            next_x = self.x
            next_y = self.y + distance
        elif direction == "down":
            next_x = self.x
            next_y = self.y - distance
        else:
            raise Exception(f"Invalid direction: {direction}")

        return Pos(x=next_x, y=next_y)

    def adjacent_pos(self, width, height):
        """Return a list of all bordering positions"""
        surr_pos = []
        for direction in ["left", "up", "right", "down"]:
            moved = self.moved_to(direction)
            if 0 <= moved.x < width and 0 <= moved.y < height:
                surr_pos.append(moved)
        return surr_pos

    def direction_to(self, other):
        """Return directions(s) to other Pos"""
        if self == other:
            return []

        dirs = []
        if self.x < other.x:
            dirs.append("right")
        elif self.x > other.x:
            dirs.append("left")

        if self.y < other.y:
            dirs.append("up")
        elif self.y > other.y:
            dirs.append("down")

        return dirs

    def within_bounds(self, bounds):
        xs, ys = bounds
        return xs[0] <= self.x < xs[1] and ys[0] <= self.y < ys[1]

    