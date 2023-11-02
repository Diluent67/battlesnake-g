from typing import Optional, Union
from Pos import Pos


class Snake:
    def __init__(self, snake_dict: dict):
        self.id = snake_dict["id"]
        self.name = snake_dict["name"]
        self.health = snake_dict["health"]
        self.body = []
        for seg in snake_dict["body"]:
            self.body.append(Pos(seg))
        self.body_dict = [pos.as_dict() for pos in self.body]
        self.head = Pos(snake_dict["head"])
        self.length = snake_dict["length"]
        self.tail = self.body[-1]
        # Additional "food_eaten" attribute to log if a snake's on a square with food
        self.food_eaten = snake_dict["food_eaten"] if "food_eaten" in snake_dict.keys() else None

    def as_dict(self):
        d = {
            "id": self.id,
            "latency": "0",
            "name": self.name,
            "health": self.health,
            "head": self.head.as_dict(),
            "body": self.body_dict,
            "length": self.length,
            "shout": "",
            "squad": "",
            "customizations" : {},
        }
        return d

    def facing_direction(self):
        """ Determine which direction this snake is facing """
        # Check if just starting a game
        if self.head == self.body[1]:
            # Technically None would be a more accurate choice, but I don't want to check for None
            # everytime calling this method
            return "up"

        direction = self.body[1].direction_to( self.body[0])
        return direction[0]

    def pos_ahead(self):
        """ Position in front of head """
        return self.head.moved_to(self.facing_direction())

    def peripheral_vision(self, direction: str, width: int, height: int) -> tuple[tuple, tuple, Pos]:
        """
        Calculate our snake's peripheral vision aka the portion of the board that is closest to our snake in a certain
        direction. E.g. the space bounded by [x1, x2] and [y1, y2] in the following example board. Notice that the space
        extends 3 squares above, below, and to the left of the snake, assuming we specified direction="left". Also
        notice that the head of the snake doesn't actually enter the 3x7 peripheral field - the hypothetical new head is
        returned as an output for convenience.

         |  |  |
         |  |  |
         |  |  |
         |  |  | £|
         |  | $|
         | x| x|
         |  |  |

        :param direction: The direction you'd like to point the snake towards (either "left", "right", "up", or "down",
            but use "auto" if you want to just use the direction the snake is facing in the current board)

        :return:
            [x1, x2] of a portion of the board that functions as the snake's peripheral vision
            [y1, y2] of the same portion
            The position of the snake's head if it hypothetically moved into its peripheral field (used to perform
                flood-fill on the peripheral field)
        """
        # Our peripheral field of vision when scanning for moves
        head = self.head.as_dict()
        neck = self.body_dict[1]
        dim = 3

        # Got to figure out the direction ourselves
        if direction == "auto":
            direction = self.facing_direction()
            head = neck.copy()  # Roll back our head location

        # Construct the bounds of the peripheral field depending on the requested direction
        if direction == "right":
            peripheral_box_x = head["x"] + 1, min(head["x"] + dim + 1, width)
            peripheral_box_y = max(head["y"] - dim, 0), min(head["y"] + dim + 1, height)
            head["x"], head["y"] = 0, head["y"] - peripheral_box_y[0]
        elif direction == "left":
            peripheral_box_x = max(head["x"] - dim, 0), head["x"]
            peripheral_box_y = max(head["y"] - dim, 0), min(head["y"] + dim + 1, height)
            head["x"], head["y"] = max(head["x"] - peripheral_box_x[0] - 1, 0), head["y"] - peripheral_box_y[0]
        elif direction == "up":
            peripheral_box_x = max(head["x"] - dim, 0), min(head["x"] + dim + 1, width)
            peripheral_box_y = head["y"] + 1, min(head["y"] + dim + 1, height)
            head["x"], head["y"] = head["x"] - peripheral_box_x[0], 0
        elif direction == "down":
            peripheral_box_x = max(head["x"] - dim, 0), min(head["x"] + dim + 1, width)
            peripheral_box_y = max(head["y"] - dim, 0), head["y"]
            head["x"], head["y"] = head["x"] - peripheral_box_x[0], max(head["y"] - peripheral_box_y[0] - 1, 0)
        else:  # Centre it around our snake's head
            peripheral_box_x = max(head["x"] - dim, 0), min(head["x"] + dim + 1, width)
            peripheral_box_y = max(head["y"] - dim, 0), min(head["y"] + dim + 1, height)
            head["x"], head["y"] = head["x"] - peripheral_box_x[0], head["y"] - peripheral_box_y[0]

        return peripheral_box_x, peripheral_box_y, Pos(head)