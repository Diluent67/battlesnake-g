"""
board = copy.deepcopy(self.board)
snake = self.all_snakes[snake_id]
head = snake.head
board[head.x, head.y] = "£"  # Representing our flood fill

# See how flood fill changes when all snakes fast-forward X turns
if fast_forward > 0:
    for snake in self.all_snakes.values():
        remove_tail = max(-snake.length + 1, -fast_forward)
        for rm in snake.body[remove_tail:]:
            board[rm.x][rm.y] = " "

# Avoid any squares that could lead to a losing head-to-head collision
risky_squares = []
if risk_averse:
    possible_threats = [opp.head for opp in self.all_snakes.values() if opp.id != snake_id and
                        opp.length >= snake.length]
    for threat in possible_threats:
        for risky_pos in threat.adjacent_pos(self.width, self.height):
            if board[risky_pos.x][risky_pos.y] not in self.obstacles:
                board[risky_pos.x][risky_pos.y] = "?"
                risky_squares.append(risky_pos)

# See what happens if an opponent were to keep moving forward and "cut off" our space
if opp_cutoff:
    opp_snake = self.all_snakes[opp_cutoff]
    opp_new_head = opp_snake.head.moved_to(opp_snake.facing_direction(), 1)
    moved_ahead = 1
    while self.is_pos_safe(opp_new_head, opp_cutoff, turn="basic")[1]:
        board[opp_new_head.x][opp_new_head.y] = "x"
        opp_new_head = opp_new_head.moved_to(opp_snake.facing_direction(), 1)
        moved_ahead += 1

# Narrow down a portion of the board that represents the snake's peripheral vision
if confined_area is not None:
    xs, ys, head = snake.peripheral_vision(confined_area, width=self.width, height=self.height)
    board = board[xs[0]:xs[1], ys[0]:ys[1]]


def update_board(self):
    """
    Fill in the board with the locations of all snakes. Our snake will be displayed like "00£" where "0" represents
    the body and "£" represents the head. Opponents will be displayed as "11£", "22£", "33£", etc. Also update the
    graph representation of the board to remove nodes occupied by our snake's body, opponent snakes, and hazards.
    """
    # global tot_time_graph
    # global counter_graph
    for opp_num, opponent in enumerate(self.opponents.values()):
        opp_body = opponent.body
        for num, pos in enumerate(opp_body):
            # clock_in = time.time_ns()
            self.board[pos.x, pos.y] = "$" if num == 0 else str(opp_num + 1)
            # Remove nodes on the graph occupied by opponent snakes since they shouldn't be reached, but retain any
            # that coincide with the position of our head
            if pos != self.you.head:
                self.graph.remove_nodes_from([pos.as_tuple()])
            # counter_graph += 1
            # tot_time_graph += round((time.time_ns() - clock_in) / 1000000, 3)
    for num, pos in enumerate(self.you.body):
        self.board[pos.x, pos.y] = "£" if num == 0 else "0"
        # Remove nodes on the graph occupied by our snake's body, but not our head since we have to traverse the
        # graph from our head
        if num > 0:
            # clock_in = time.time_ns()
            self.graph.remove_nodes_from([pos.as_tuple()])
            # counter_graph += 1
            # tot_time_graph += round((time.time_ns() - clock_in) / 1000000, 3)

    # self.board_ff = self.board.copy()
    # if (self.board == " ").sum() > (self.board.width * self.board.height * 2 / 3):
    #     for j in range(self.board.height):
    #         for i in range(self.board.width):
    #             if len(self.graph.edges((i, j))) == 4:
    #                 self.board_ff[i, j] = "£"


def display_board(self, board: Optional[np.array] = None, return_string: Optional[bool] = False):
    """
    Print out a nicely formatted board for convenient debugging e.g.

     |  |  |  |  |  |  |  |  |  |  |
     |  |  |  |  |  |  |  |  |  |  |
     |  |  |  |  | o| o| o| o| o| o|
     |  |  |  |  | o| o|  |  |  | o|
    x| x|  |  |  |  |  |  |  |  | o|
    x|  |  |  |  |  |  |  |  |  | o|
    x|  |  |  |  |  |  |  |  |  | o|
    x|  |  |  | £| o| o| o| o| o| o|
    x|  |  | $| x| x| x|  |  |  |  |
    x| x| x| x| x| x| x|  |  |  |  |
     |  |  |  |  |  |  |  |  |  |  |

    :param board: Calling display_board() will print out the current board, but for debugging purposes, you can feed
        in a different board variable to display
    :param return_string: You can optionally choose to return the board as a string for you to print later
    """
    render_board = board if board is not None else self.board
    for j in range(1, len(render_board[0]) + 1):
        display_row = ""
        for i in range(0, len(render_board)):
            display_row += f"{render_board[i][-j]}| "
        if self.debugging:
            logging.info(display_row)
        else:
            print(display_row)

    # Return the board as a string instead of printing it out
    if return_string:
        board_str = ""
        for j in range(1, len(render_board[0]) + 1):
            display_row = ""
            for i in range(0, len(render_board)):
                if render_board[i][-j] == " ":  # Adjust for difference in sizes between spaces and x/o's
                    display_row += f"  | "
                else:
                    display_row += f"{render_board[i][-j]}| "
            board_str += display_row + "\n"
        return board_str


    @staticmethod
    def snake_compass(head: dict, neck: dict) -> str:
        """
        Return the direction a snake is facing in the current board

        :param head: The location of the snake's head as a dictionary e.g. {"x": 5, "y": 10}
        :param neck: The location of the snake's neck as a dictionary e.g. {"x": 6, "y": 10}

        :return: Either "left", "right", "up", or "down" e.g. "right" for the above inputs
        """
        if neck["x"] < head["x"]:
            direction = "right"
        elif neck["x"] > head["x"]:
            direction = "left"
        elif neck["y"] < head["y"]:
            direction = "up"
        elif neck["y"] > head["y"]:
            direction = "down"
        else:
            direction = "none"  # At the beginning of the game when snakes are coiled
        return direction

    #
    # def flood_fill(
    #         self,
    #         snake_id: str,
    #         confined_area: Optional[str] = None,
    #         risk_averse: Optional[bool] = False,
    #         fast_forward: Optional[int] = 0,
    #         get_touching_opps: Optional[bool] = False
    # ) -> int | tuple[int, list]:
    #     """
    #     Recursive function to get the total available space for a given snake. Basically, count how many £ symbols
    #     we can fill while avoiding any $, o, and x symbols (obstacles).
    #
    #     :param snake_id: The ID of the desired snake we want to do flood fill for
    #     :param confined_area: Tells the function to do flood fill for only on one side of the snake (either "left",
    #         "right", "up", or "down") to represent its peripheral vision
    #     :param risk_averse: If True, flood fill will avoid any squares that directly border an opponent's head
    #     :param fast_forward: Hypothetical scenarios where we want to see how much space we still have after moving
    #         X turns ahead. E.g. if we set it to 5, then we remove 5 squares from all snake's tails before doing flood
    #         fill - this is only useful when we suspect we'll be trapped by an opponent snake.
    #     :param get_touching_opps: Option to return a list of other snakes whose heads our flood fill is touching
    #
    #     :return: The total area of the flood fill selection
    #     """
    #     head = self.all_snakes[snake_id].head
    #
    #     if snake_id == self.you.id:  # Assume we're doing flood fill for our snake
    #         board = copy.deepcopy(self.board)
    #         # See how flood fill changes when all snakes fast-forward X turns
    #         if fast_forward > 0:
    #             for snake in self.all_snakes.values():
    #                 to_remove = max(-(len(snake.body) - 1), -fast_forward)
    #                 tail_removed = snake.body[to_remove:]
    #                 for remove in tail_removed:
    #                     board[remove.x][remove.y] = " "
    #         # Try to avoid any squares that our enemy can go to
    #         if risk_averse:
    #             threats = [other.head for other in self.opponents.values() if other.length >= self.you.length]
    #             for threat in threats:
    #                 x, y = threat.x, threat.y
    #                 avoid_sq = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #                 for n in avoid_sq:
    #                     if not (n[0] == head.x and n[1] == head.y) and \
    #                             (0 <= n[0] < self.board.width and 0 <= n[1] < self.board.height):
    #                         board[n[0]][n[1]] = "x"
    #     else:  # Otherwise, generate a new board and pretend the opponent snake is our snake
    #         board = np.full((self.board.width, self.board.height), " ")
    #         for num, square in enumerate(self.all_snakes[snake_id].body):
    #             board[square.x, square.y] = "£" if num == 0 else "o"
    #         for other_id, other_snake in self.all_snakes.items():
    #             if other_id != snake_id:
    #                 for num, other_square in enumerate(other_snake.body):
    #                     board[other_square.x, other_square.y] = "$" if num == 0 else "x"
    #         # Try to avoid any squares that our enemy can go to
    #         if risk_averse:
    #             threats = [other.head for other in self.all_snakes.values() if other.length >= self.all_snakes[snake_id].length and other.id != snake_id]
    #             for threat in threats:
    #                 x, y = threat.x, threat.y
    #                 avoid_sq = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #                 for n in avoid_sq:
    #                     if not (n[0] == head.x and n[1] == head.y) and \
    #                             (0 <= n[0] < self.board.width and 0 <= n[1] < self.board.height):
    #                         board[n[0]][n[1]] = "x"
    #
    #     # Narrow down a portion of the board that represents the snake's peripheral vision
    #     if confined_area is not None:
    #         xs, ys, head = self.peripheral_vision(snake_id, confined_area)
    #         board = board[xs[0]:xs[1], ys[0]:ys[1]]
    #         self.display_board(board)
    #
    #     def fill(x, y, board, initial_square):
    #         if board[x][y] == "$":  # Opponent snake heads
    #             opp_heads_in_contact.append(Pos(x, y))
    #             boundary_pos.append(Pos(x, y))
    #             return
    #         if board[x][y] in ["x", "o"]:  # Off-limit squares
    #             boundary_pos.append(Pos(x, y))
    #             return
    #         if board[x][y] in [str(num) for num in range(1, 9)]:  # Off-limit squares
    #             boundary_pos.append(Pos(x, y))
    #             return
    #         if board[x][y] in "£" and not initial_square:  # Already filled
    #             return
    #         board[x][y] = "£"
    #         neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #         for n in neighbours:
    #             if 0 <= n[0] < len(board) and 0 <= n[1] < len(board[0]):
    #                 fill(n[0], n[1], board, initial_square=False)
    #
    #     opp_heads_in_contact = []
    #     boundary_pos = []
    #     fill(head.x, head.y, board, initial_square=True)
    #     filled = sum((row == "£").sum() for row in board)
    #     flood_fill = max(filled - 1, 0)  # Exclude the head from the count, but cannot ever be negative
    #
    #     if get_touching_opps:
    #         return flood_fill, opp_heads_in_contact, boundary_pos
    #     else:
    #         return flood_fill