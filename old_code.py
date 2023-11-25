


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



# COLLISIONS
    # # Did any snakes die from head-to-head collisions?
    # all_heads = [(snake["head"]["x"], snake["head"]["y"]) for snake in all_snakes]
    # count_heads = Counter(all_heads)
    # butt_heads = [k for k, v in count_heads.items() if v > 1]  # Any square where > 1 heads collided
    # rm_snake_indices = []
    # for butt_head in butt_heads:
    #     overlapping_snakes = np.array([  # Array of (id, length) for colliding snakes
    #         (snake["id"], snake["length"]) for snake in all_snakes
    #         if (snake["head"]["x"] == butt_head[0] and snake["head"]["y"] == butt_head[1])
    #     ])
    #     lengths = overlapping_snakes[:, 1].astype(int)
    #     # If our snake died, don't remove it just yet
    #     if not (self.you.id in overlapping_snakes[:, 0]):
    #         indices_largest_snakes = np.argwhere(lengths == lengths.max()).flatten().tolist()
    #         if len(indices_largest_snakes) > 1:  # No winner if the snakes are the same length
    #             winner_id = None
    #         else:
    #             winner_id = overlapping_snakes[:, 0][indices_largest_snakes[0]]
    #         # Remove any dead snakes
    #         for rm_id in overlapping_snakes[:, 0]:
    #             if rm_id != winner_id:  # Grab the snake index to remove later
    #                 rm_snake_indices.extend([i for i in range(len(all_snakes)) if all_snakes[i]["id"] == rm_id])
    #
    # for i in sorted(rm_snake_indices, reverse=True):
    #     del all_snakes[i]


    def is_game_over(self, for_snake_id: Optional[str] = None, depth: Optional[int] = 4) -> tuple[bool, bool]:
        """
        Determine if the game is over for our snake. Can optionally be used to determine whether any opponent snake is
        dead or not.

        :param for_snake_id: The ID of the desired snake we want to know died or not
        :param depth: During minimax, things get complicated when we call this function right after making a move for
            our snake, but before the opponent snakes have made moves. We only want to return True when a complete turn
            is done (e.g. our snake made a move and our opponents did as well). Thus, we need the current depth that
            minimax is on to determine this.

        :return:
            True if the overall game has a winner or if our snake is dead, False otherwise
            True if the snake associated with the input snake ID is alive, False otherwise
        """
        # Skip if we're at the beginning of the game when all snakes are still coiled up
        if self.turn == 0:
            return False, True

        snake_monitor = {}  # A dictionary for each snake showing whether they're alive
        for snake_id, snake in self.all_snakes.items():
            # Check that the snake is on a safe square (depending on if we're at a depth where only we've made a move)
            is_safe, _ = self.board.evaluate_pos(snake.head, snake_id, turn="done" if depth % 2 == 0 else "ours")
            snake_monitor[snake_id] = is_safe

        # Game is over if there's only one snake remaining or if our snake died
        game_over = True if (sum(snake_monitor.values()) == 1 or not snake_monitor[self.you.id]) else False
        # See if a specific snake is alive or not
        snake_still_alive = snake_monitor[for_snake_id if for_snake_id is not None else self.you.id]

        return game_over, snake_still_alive



    # def flood_fill(
    #         self,
    #         snake_id: str,
    #         risk_averse: Optional[bool] = True,
    #         confine_to: Optional[str] = None,
    #         confined_dist: Optional[int] = 3,
    #         fast_forward: Optional[int] = 0,
    #         opp_cutoff: Optional[str] = None,
    #         get_boundaries: Optional[bool] = False,
    #         get_touching_opps: Optional[bool] = False,
    #         full_package: Optional[bool] = False,
    #         ff_split: Optional[bool] = False
    # ) -> int | tuple[int, list[Pos]]:
    #     """
    #     Get the total available space for a given snake.
    #
    #     :param snake_id: The ID of the snake we want to do flood fill for
    #     :param risk_averse: Option to avoid any squares that directly border a longer opponent's head
    #     :param confine_to: Tells the function to do flood fill on only one side of the snake (either "left", "right",
    #         "up", or "down") to represent its peripheral vision
    #     :param confined_dist: Paired with "confine_to" to determine the depth of the snake's peripheral vision
    #     :param fast_forward: Hypothetical scenarios where we want to see how much space we still have after moving
    #         X turns ahead. E.g. if we set it to 5, then we remove 5 squares from all snake's tails before doing flood
    #         fill - this is only useful when we suspect we'll be trapped by an opponent snake.
    #     :param opp_cutoff: Input any opponent snake IDs and see how much space we still have after they "cut off" our
    #         space. Assume the opponents keep going forward until they meet the edge of the board or an obstacle.
    #     :param get_boundaries: Option to return a list of positions that represent the edges of our flood fill
    #     :param get_touching_opps: Option to return a list of other snakes whose heads our flood fill is touching
    #     :param full_package: Option to run 4 parameters at once with a single function call: risk_averse=True,
    #         risk_averse=False, get_boundaries=True, and get_touching_opps=True
    #
    #     :return:
    #         The total area of the flood fill selection
    #         Optionally, a list of other snakes whose heads our flood fill is touching
    #     """
    #     board = copy.deepcopy(self.board)
    #     snake = self.all_snakes[snake_id]
    #     head = snake.head
    #     board[head.x, head.y] = 1  # Representing our flood fill
    #
    #     # See how flood fill changes when all snakes fast-forward X turns
    #     if fast_forward > 0:
    #         for snake in self.all_snakes.values():
    #             remove_tail = max(-snake.length + 1, -fast_forward)
    #             for rm in snake.body[remove_tail:]:
    #                 board[rm.x, rm.y] = 0
    #
    #     # Cases where our tail is directly adjacent to our head and therefore in the way of our flood fill TODO: opponent tail as well?
    #     if head.manhattan_dist(snake.tail) == 1:
    #         board[snake.tail.x, snake.tail.y] = 0
    #
    #     # Avoid any squares that could lead to a losing head-to-head collision
    #     risky_squares = []
    #     if risk_averse:
    #         possible_threats = [opp.head for opp in self.all_snakes.values() if (
    #                 opp.id != snake_id and opp.length >= snake.length)]
    #         for threat in possible_threats:
    #             for risky_pos in threat.adjacent_pos(self.width, self.height):
    #                 if board[risky_pos.x, risky_pos.y] not in self.obstacles:
    #                     board[risky_pos.x, risky_pos.y] = 255
    #                     risky_squares.append(risky_pos)
    #
    #     # See what happens if an opponent were to keep moving forward and "cut off" our space
    #     if opp_cutoff:
    #         opp_snake = self.all_snakes[opp_cutoff]
    #         opp_dir = opp_snake.facing_direction()
    #         opp_new_head = opp_snake.head.moved_to(opp_dir, 1)
    #         while not self.evaluate_pos(opp_new_head, opp_cutoff, turn_type="static")[1]:
    #             board[opp_new_head.x, opp_new_head.y] = 255
    #             opp_new_head = opp_new_head.moved_to(opp_dir, 1)
    #
    #     # Narrow down a portion of the board that represents the snake's peripheral vision
    #     if confine_to is not None:
    #         xs, ys, new_head = snake.peripheral_vision(
    #             confine_to, dist=confined_dist, width=self.width, height=self.height)
    #         board = board[xs[0]:xs[1], ys[0]:ys[1]]
    #         # Account for the board change if we're running the full package
    #         if full_package:
    #             shifted_risky_squares = []
    #             for risky_pos in risky_squares:
    #                 if risky_pos.within_bounds([xs, ys]):
    #                     shift_x, shift_y = new_head.x - head.x, new_head.y - head.y
    #                     new_risky_pos = Pos({"x": risky_pos.x + shift_x, "y": risky_pos.y + shift_y})
    #                     shifted_risky_squares.append(new_risky_pos)
    #             risky_squares = shifted_risky_squares
    #         # Update our snake's head pointer to adjust to the cropped board
    #         head = new_head
    #
    #     def fill(x, y, board, initial_square, avoid_risk):
    #         if board.shape[0] == 0 or board.shape[1] == 0:  # Empty board TODO: remove from recursive
    #             return
    #         if board[x][y] == self.obstacles[0]:  # Opponent snake heads
    #             heads_in_contact.append(Pos({"x": x, "y": y}))
    #             boundaries.append(Pos({"x": x, "y": y}))
    #             return
    #         if board[x][y] in (self.obstacles if avoid_risk else self.obstacles[:-1]):  # Off-limit squares
    #             boundaries.append(Pos({"x": x, "y": y}))
    #             return
    #         if board[x][y] == 1 and not initial_square:  # Already filled
    #             return
    #
    #         board[x][y] = 1
    #         avoid_sq = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #         for n in avoid_sq:
    #             # if 0 <= n[0] < board_width and 0 <= n[1] < board_height:
    #             if min_x <= n[0] < max_x and min_y <= n[1] < max_y:
    #                 fill(n[0], n[1], board, initial_square=False, avoid_risk=avoid_risk)
    #
    #     boundaries = []
    #     heads_in_contact = []
    #     # board_width, board_height = len(board), len(board[0])
    #     crop = 6
    #     min_x, max_x = 0, len(board)
    #     min_y, max_y = 0, len(board[0])
    #     # if confine_to is not None:
    #     #     min_x, max_x = 0, len(board)
    #     #     min_y, max_y = 0, len(board[0])
    #     # else:
    #     #     min_x, max_x = max(0, head.x - crop), min(self.width, head.x + crop)
    #     #     min_y, max_y = max(0, head.y - crop), min(self.height, head.y + crop)
    #     if ff_split:
    #         if snake.facing_direction() in ["left", "right"]:
    #             left_x, left_y = head.moved_to("up").as_tuple()
    #             right_x, right_y = head.moved_to("down").as_tuple()
    #         else:
    #             left_x, left_y = head.moved_to("left").as_tuple()
    #             right_x, right_y = head.moved_to("right").as_tuple()
    #         fill(left_x, left_y, board, initial_square=False, avoid_risk=risk_averse)
    #         left_filled = sum((row == 1).sum() for row in board)
    #         fill(right_x, right_y, board, initial_square=False, avoid_risk=risk_averse)
    #         right_filled = sum((row == 1).sum() for row in board) - left_filled + 1
    #         flood_fill_ra = max(left_filled - 1, 1e-15) if left_filled > right_filled else max(right_filled - 1, 1e-15)
    #         undesired = min([left_filled, right_filled])
    #     else:
    #         fill(head.x, head.y, board, initial_square=True, avoid_risk=risk_averse)
    #         filled = sum((row == 1).sum() for row in board)
    #         flood_fill_ra = max(filled - 1, 1e-15)  # Exclude the head from the count, but cannot ever be negative
    #
    #     if full_package:
    #         # Repeat but assume all risky squares are fair game
    #         for risky_sq in risky_squares:
    #             # Situations where our snake's head was previously overwritten by a risky square
    #             if risky_sq == head and board[risky_sq.x][risky_sq.y] != 1:
    #                 board[risky_sq.x][risky_sq.y] = 1
    #                 fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
    #             # Ensure that the skipped square can be connected to the main flood fill
    #             surr_risks = risky_sq.adjacent_pos(len(board), len(board[0]))
    #             for surr_risk in surr_risks:
    #                 if board[surr_risk.x][surr_risk.y] == 1:
    #                     # Remove from the list of boundary squares and update the fill
    #                     if risky_sq in boundaries:
    #                         boundaries = [pos for pos in boundaries if pos != risky_sq]
    #                     fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
    #                     break
    #         filled = sum((row == 1).sum() for row in board)
    #         flood_fill_all = max(filled - 1, 1e-15) if ff_split else max(filled - 1, 1e-15)
    #
    #     if get_boundaries:
    #         return flood_fill_ra, boundaries
    #     elif get_touching_opps:
    #         return flood_fill_ra, heads_in_contact
    #     elif full_package:
    #         if confine_to is None:
    #             self.space_ra = flood_fill_ra
    #             self.space_all = flood_fill_all
    #             self.ff_bounds = list(set(boundaries))
    #             self.touch_opps = list(set(heads_in_contact))
    #             return self.space_ra, self.space_all, self.ff_bounds, self.touch_opps
    #         else:
    #             return flood_fill_ra, flood_fill_all, list(set(boundaries)), list(set(heads_in_contact))
    #     else:
    #         return flood_fill_ra