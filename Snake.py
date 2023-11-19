from typing import Optional, Union
from Pos import Pos


class Snake:
    def __init__(self, snake_dict: dict):
        """
        Represents a snake in any given position, with useful methods that get information on the snake's direction, 
        peripheral, etc.

        :param snake_dict: The "all_snakes" portion of the move API request
        """
        self.id = snake_dict["id"]
        self.name = snake_dict["name"]
        self.health = snake_dict["health"]
        self.body = [Pos(seg) for seg in snake_dict["body"]]
        self.body_dict = [pos.as_dict() for pos in self.body]
        self.head = Pos(snake_dict["head"])
        self.length = snake_dict["length"]
        self.tail = self.body[-1]
        self.food_eaten = Pos(snake_dict["food_eaten"]) if (  # If a snake's on a square with food
                "food_eaten" in snake_dict.keys() and snake_dict["food_eaten"] is not None) else None
        self.dead = False

    def as_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "health": self.health,
            "body": self.body_dict,
            "head": self.head.as_dict(),
            "length": self.length,
            "food_eaten": self.food_eaten.as_dict() if self.food_eaten is not None else None
        }
        return d

    def facing_direction(self):
        """Determine which direction this snake is facing"""
        # Check if just starting a game
        if self.head == self.body[1]:
            # Technically None would be a more accurate choice, but I don't want to check for None
            # every time calling this method
            return "up"

        direction = self.body[1].direction_to(self.body[0])
        return direction[0]

    def pos_ahead(self):
        """Position in front of head"""
        return self.head.moved_to(self.facing_direction())

    def make_move(self, direction, food_list, return_dict: Optional[bool] = True, board_changes: Optional[dict] = None):
        """Simulate a move in a given direction and log any food eaten"""
        snake_dict = self.as_dict()
        # Update the head, body, and health of the snake to reflect the simulated move
        new_head = self.head.moved_to(direction)
        new_head_dict = new_head.as_dict()
        snake_dict["health"] = self.health - 1
        snake_dict["body"] = [new_head_dict] + self.body_dict[:-1]
        snake_dict["head"] = new_head_dict
        snake_dict["food_eaten"] = new_head_dict if new_head in food_list else None

        if board_changes is not None:
            board_changes["add"].append(new_head.as_tuple())
            if sum([pos == self.body[-1] for pos in self.body]) == 1:
                board_changes["remove"].append(self.body[-1].as_tuple())

        if return_dict:
            return snake_dict
        else:
            return Snake(snake_dict)

    def ate_food(self):
        """Update the snake's attributes if it ate food"""
        self.length += 1
        self.health = 100
        self.body += [self.body[-1]]
        self.food_eaten = None

    def peripheral_vision(
            self,
            direction: Optional[str] = "auto",
            dist: Optional[int] = 3,
            width: Optional[int] = 11,
            height: Optional[int] = 11,
            return_pos_only: Optional[bool] = False
    ) -> tuple[tuple, tuple, Pos]:
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
         |  | H|
         | 1| 1|
         |  |  |

        :param direction: The direction you'd like to point the snake towards (either "left", "right", "up", or "down",
            but use "auto" if you want to just use the direction the snake is facing in the current board)
        :param dist: How far our peripheral extends in any direction
        :param width: The width of the board
        :param height: The height of the board
        :param return_pos_only:

        :return:
            [x1, x2] of a portion of the board that functions as the snake's peripheral vision
            [y1, y2] of the same portion
            The position of the snake's head if it hypothetically moved into its peripheral field (used to perform
                flood-fill on the peripheral field)
        """
        # Our peripheral field of vision when scanning for moves
        head = self.head.__copy__()
        neck = Pos(self.body_dict[1])

        # Got to figure out the direction ourselves
        if direction == "auto":
            direction = self.facing_direction()
            head = neck  # Roll back our head location

        # Construct the bounds of the peripheral field depending on the requested direction
        if direction == "right":
            peripheral_box_x = head.x + 1, min(head.x + dist + 1, width)
            peripheral_box_y = max(head.y - dist, 0), min(head.y + dist + 1, height)
            head.x, head.y = 0, head.y - peripheral_box_y[0]
        elif direction == "left":
            peripheral_box_x = max(head.x - dist, 0), head.x
            peripheral_box_y = max(head.y - dist, 0), min(head.y + dist + 1, height)
            head.x, head.y = max(head.x - peripheral_box_x[0] - 1, 0), head.y - peripheral_box_y[0]
        elif direction == "up":
            peripheral_box_x = max(head.x - dist, 0), min(head.x + dist + 1, width)
            peripheral_box_y = head.y + 1, min(head.y + dist + 1, height)
            head.x, head.y = head.x - peripheral_box_x[0], 0
        elif direction == "down":
            peripheral_box_x = max(head.x - dist, 0), min(head.x + dist + 1, width)
            peripheral_box_y = max(head.y - dist, 0), head.y
            head.x, head.y = head.x - peripheral_box_x[0], max(head.y - peripheral_box_y[0] - 1, 0)
        else:  # Centre it around our snake's head
            peripheral_box_x = max(head.x - dist, 0), min(head.x + dist + 1, width)
            peripheral_box_y = max(head.y - dist, 0), min(head.y + dist + 1, height)
            head.x, head.y = head.x - peripheral_box_x[0], head.y - peripheral_box_y[0]

        if return_pos_only:
            return peripheral_box_x, peripheral_box_y
        return peripheral_box_x, peripheral_box_y, head
    