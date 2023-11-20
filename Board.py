from __future__ import annotations
import copy
import networkx as nx
import numpy as np
from typing import Optional, Union
from Pos import Pos
from Snake import Snake


class Board:
    def __init__(self, board_dict: dict, all_snakes: Optional[dict[str, Snake]] = None):
        """
        Represents our Battlesnake board in any given state. Provides visualisations useful for debugging and can
        perform flood fill.

        :param board_dict: The "board" portion of the move API request
        :param all_snakes: To avoid repeating code, input any previously loaded snakes
        """
        self.width = board_dict["width"]
        self.height = board_dict["height"]
        self.food = [Pos(xy) for xy in board_dict["food"]]
        self.hazards = [Pos(xy) for xy in board_dict["hazards"]] if "hazards" in board_dict.keys() else []
        if all_snakes is None:
            all_snakes: dict[str, Snake] = {}
            for snake_dict in board_dict["snakes"]:
                all_snakes[snake_dict["id"]] = Snake(snake_dict)
        self.all_snakes = all_snakes
        self.board = np.full((self.width, self.height), " ")
        self.graph = nx.grid_2d_graph(self.width, self.height)
        self.obstacles = ["H"] + [str(num) for num in range(0, 9)] + ["x", "?"]

    def as_dict(self):
        d = dict()
        d["width"] = self.width
        d["height"] = self.height
        d["hazards"] = [pos.as_dict() for pos in self.hazards]
        d["food"] = [pos.as_dict() for pos in self.food]
        d["snakes"] = [snake.as_dict() for snake in self.all_snakes.values()]
        return d

    def update_board(self):
        """
        Fill in the board with the locations of all snakes. Our snake will be displayed like "00H" where "0" represents
        the body and "H" represents the head. Opponents will be displayed as "11H", "22H", "33H", etc. Also update the
        graph representation of the board to remove nodes occupied by our snake's body, opponent snakes, and hazards.
        """
        for f in self.food:
            self.board[f.x, f.y] = "f"

        for h in self.hazards:
            self.board[h.x, h.y] = "x"
            self.graph.remove_nodes_from([h.as_tuple()])

        for snake_num, snake in enumerate(self.all_snakes.values()):
            body = snake.body
            for num, pos in enumerate(body):
                self.board[pos.x, pos.y] = "H" if num == 0 else str(snake_num)
                # Remove nodes on the graph occupied by opponent snakes since they shouldn't be reached, but keep any
                # that coincide with the position of our head
                if not (snake_num == 0 and num == 0):
                    self.graph.remove_nodes_from([pos.as_tuple()])

    def whiteout(self, crop_centre):
        min_x, max_x = max(0, crop_centre.x - 9), min(self.width - 1, crop_centre.x + 9)
        min_y, max_y = max(0, crop_centre.y - 9), min(self.height - 1, crop_centre.y + 9)
        for i in range(0, self.width):
            for j in range(0, self.height):
                if not (min_x <= i <= max_x and min_y <= j <= max_y):
                    self.board[i, j] = "x"
        return

    def display_graph(self, show=True):
        g = np.full((self.width, self.height), " ")
        nodes = self.graph.nodes
        for node in nodes:
            g[node[0]][node[1]] = "x"
        self.display(board=g, show=show)

    def display(
            self,
            board: Optional[np.array] = None,
            show: Optional[bool] = True,
            add_lengths: Optional[bool] = True
    ) -> str:
        """
        Convert the board into a nicely formatted string for convenient debugging e.g.

        10	  |  |  |  |  |  |  |  |  | f|  | 			Snake 0: 14
        9	  |  |  |  |  |  |  |  |  |  |  | 			Snake 1: 23
        8	 H| 0| 0| 0|  |  |  |  |  |  |  |
        7	  |  |  | 0| 0| 0| 0| 0|  |  |  |
        6	  |  |  |  |  |  |  | 0| 0|  |  |
        5	 f|  |  |  |  |  |  | 0| 0|  |  |
        4	 H| 1| 1| 1| 1|  |  |  |  |  |  |
        3	  |  |  |  | 1|  |  |  |  |  |  |
        2	  |  |  |  | 1| 1| 1| 1| 1| 1| 1|
        1	  |  |  |  | 1|  |  |  |  |  | 1|
        0	  |  |  |  | 1| 1| 1| 1| 1| 1| 1|

             0  1  2  3  4  5  6  7  8  9  10

        :param board: Calling display() will print out the current board, but for debugging purposes, you can feed in a
            different board variable to display
        :param show: The function normally returns a string, but can optionally print it automatically if True
        :param add_lengths: Adds a column of information showing all snake lengths
        """
        board = self.board if board is None else board
        board_str = ""
        for j in range(1, len(board[0]) + 1):
            display_row = f"{self.height - j}\t "
            for i in range(0, len(board)):
                display_row += f"{board[i][-j]}| "
            # Add snake length information
            if add_lengths:
                if j <= len(self.all_snakes):
                    jth_snake = list(self.all_snakes.values())[j - 1]
                    display_row += f"\t\t\tSnake {j - 1}: {jth_snake.length}"
            board_str += display_row + "\n"
        board_str += "\n\t " + "  ".join(map(str, np.arange(0, self.width)))
        if show:
            print(board_str)
        return board_str

    def crop_board(self, xs: Union[list, tuple], ys: Union[list, tuple]) -> np.array:
        """Return a portion of the board"""
        self.board = self.board[xs[0]:xs[1], ys[0]:ys[1]]

    def identify_snake(self, pos: Pos) -> Snake:
        """Given any position on the board, return the Snake lying on top of it"""
        matched = [snake for snake in self.all_snakes.values() if pos in snake.body]
        if len(matched) > 1:
            matched = sorted(matched, key=lambda snake: snake.length, reverse=True)
        return matched[0]

    def shortest_dist(self, start: Pos, end: Pos) -> int:
        """
        Get the best approximation for the distance between two positions. When possible, use Dijkstra's algorithm to
        get an exact path, but if that's not possible (e.g. due to obstructions), return 1e6 + the Manhattan distance.

        To illustrate the rationale, let's say we have to compare the distance between A to B, C, and D:
            - A -> B is unreachable with a default Dijkstra output of 1e6, but has a Manhattan distance of 2
            - A -> C is reachable with a Dijkstra output of 15, but a Manhattan distance of 10
            - A -> D is unreachable (1e6), but has a Manhattan distance of 5
        Which point is closer? Obviously C if we go with Dijkstra's algorithm, but then B and D both have the same 1e6
        outputs. To discern which point is hypothetically closer, we set B => 1e6 + 2 and D => 1e6 + 5, which lets us
        select B as the closer point to D!

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board

        :return: The closest distance between the start and end points. If there's no connecting path, approximate with
            1e6 + the Manhattan distance.
        """
        closest = self.dijkstra_shortest_path(start, end)
        if closest == 1e6:
            closest += start.manhattan_dist(end)
        return closest

    def dijkstra_shortest_path(self, start: Pos, end: Pos, from_snake: Optional[str] = None,
                               get_path: Optional[bool] = False) -> int | tuple[int, list]:
        """
        Return the shortest path between two positions using Dijkstra's algorithm implemented in networkx

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board
        :param get_path: Return the complete path identified by the algorithm

        :return: The shortest distance between the start and end inputs. 1e6 if no path could be found
        """
        if (manhattan_approx := start.manhattan_dist(end) )> self.width / 2:
            return (manhattan_approx, None) if get_path else manhattan_approx

        start = start.as_tuple()
        end = end.as_tuple()
        check_nodes = [start, end]
        # Cases where our tail is directly adjacent to our head and in the way of our graph
        if from_snake is not None:
            our_snake = self.all_snakes[from_snake]
            if our_snake.head.manhattan_dist(our_snake.tail) == 1:
                check_nodes.append(our_snake.tail.as_tuple())
        # Add in missing nodes
        temp_graph, temp_added_nodes = self.check_missing_nodes(self.graph, check_nodes)

        # Run networkx's Dijkstra method (it'll error out if no path is possible)
        try:
            path = nx.shortest_path(temp_graph, start, end)
            shortest = len(path)
        except nx.exception.NetworkXNoPath:
            path = None
            shortest = 1e6

        # Remove any temporary nodes that were previously added
        for temp_nodes in temp_added_nodes:
            temp_graph.remove_node(temp_nodes)

        if get_path:
            return shortest, path
        else:
            return shortest

    @staticmethod
    def check_missing_nodes(G: nx.Graph, nodes: list[tuple]) -> tuple[nx.Graph, list]:
        """
        A helper function to use with Dijkstra's algorithm implemented in networkx. If the graph representation of the
        Battlesnake board doesn't contain a node at a desired position, the networkx shortest_path function will error
        out since it can't compute a path to a non-existent node. This function temporarily adds a node at that position
        and creates edges to neighbouring nodes, while also outputting the name of that node for later removal.

        :param G: A graph representation of the board
        :param nodes: The desired start and end locations on the board

        :return:
            A graph with nodes added to the desired start and end positions if they weren't previously there
            A list of the locations of any added nodes
        """
        # If the desired location is on a hazard/snake, then it's absent from the graph, and we want to add in the node
        added_nodes = []
        for num, node in enumerate(nodes):
            if not G.has_node(node):
                added_nodes.append(node)
                G.add_node(node)
                x, y = node
                # Include edges to connect the added node to surrounding nodes if possible
                possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for e in possible_edges:
                    if G.has_node(e):
                        G.add_edge(node, e)
        return G, added_nodes

    def longest_path(self, start: Pos, end: Pos, simple_paths_cutoff: int, threshold: Optional[int] = 0) -> tuple[int, int]:
        """
        Return the longest path between two positions (relevant during an effort to stall)

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board
        :param threshold:

        :return: The longest distance between the start and end inputs. 1e6 if no path could be found
        """
        start = start.as_tuple()
        end = end.as_tuple()
        temp_graph, temp_added_nodes = self.check_missing_nodes(self.graph, [start, end])

        longest = 1e6
        shortest = 1e6
        # Get all possible paths and filter for the longest one
        possible_paths = [path for path in nx.all_simple_paths(temp_graph, start, end, cutoff=simple_paths_cutoff)]
        if len(possible_paths) > 0:
            longest_path = max(possible_paths, key=lambda path: len(path))
            longest = len(longest_path) - 1
            # Now filter for the shortest path longer than the desired threshold
            shortest = longest
            if threshold > 0:
                paths_above_threshold = [path for path in possible_paths if len(path) > threshold]
                if len(paths_above_threshold) > 0:
                    shortest_path = min(paths_above_threshold, key=lambda path: len(path))
                    shortest = len(shortest_path) - 1

        # Remove any temporary nodes that were previously added
        for temp_nodes in temp_added_nodes:
            temp_graph.remove_node(temp_nodes)

        return longest, shortest

    def closest_dist_to_food(self, snake_id, risk_averse=True) -> tuple[int, Pos]:
        """
        Compute the shortest distance to food for a snake, but only if it's closer to it than an opponent snake

        :param snake_id: The ID of the desired snake we want to find food for
        :param risk_averse: Avoid any food that an opponent snake is closer to

        :return:
            The shortest distance to food
            The location of the food as a Pos object
        """
        you = self.all_snakes[snake_id]
        opponents = [snake for snake in self.all_snakes.values() if snake.id != snake_id]

        best_dist = np.inf
        best_food = None
        sorted_food = sorted(self.food, key=lambda f: you.head.manhattan_dist(f))  # Pre-sort for efficiency
        for food in sorted_food:
            dist_food = self.dijkstra_shortest_path(food, you.head)

            opp_dist_to_food = 1e6
            food_edge_killed = False
            if risk_averse:
                # Find which opponents are equally close to the same food as us (use the Manhattan distance to estimate)
                closest_opps = [opp for opp in opponents if opp.head.manhattan_dist(food) <= dist_food]
                # Then double-check more accurately using Dijkstra's algorithm (to minimise Dijkstra function calls)
                if len(closest_opps) > 0:
                    # If an enemy snake is longer than ours, and we're both 2 squares away from food, then they're
                    # technically closer to it since they'd win the head-to-head battle
                    opp_dist_to_food = min(
                        [self.dijkstra_shortest_path(food, snake.head) - 1 if snake.length >= you.length
                         else self.dijkstra_shortest_path(food, snake.head)
                         for snake in closest_opps]
                    )

                # TODO MAKE MORE ROBUST
                # Avoid getting edge-killed as a result of getting the food
                if food.x in [0, self.width - 1] or food.y in [0, self.height - 1]:
                    edge_kill_sqs = self.edge_kill_squares(food)
                    for kill_sq in edge_kill_sqs:
                        closest_edge_kill = [opp for opp in opponents if opp.length > you.length and
                                             opp.head.manhattan_dist(kill_sq) <= dist_food - 1]
                        if len(closest_edge_kill) > 0:
                            food_edge_killed = True
                            break

            # Update the shortest distance
            if dist_food < best_dist and opp_dist_to_food >= dist_food and not food_edge_killed:
                best_dist = dist_food
                best_food = food
            # "Prune" on the first instance that we stop updating
            elif best_food is not None:
                break

        return best_dist, best_food

    def edge_kill_squares(self, pos):
        if pos.x == 0:
            return Pos({"x": pos.x + 1, "y": pos.y}), Pos({"x": pos.x + 2, "y": pos.y})
        if pos.x == self.width - 1:
            return Pos({"x": pos.x - 1, "y": pos.y}), Pos({"x": pos.x - 2, "y": pos.y})
        if pos.y == 0:
            return Pos({"x": pos.x, "y": pos.y + 1}), Pos({"x": pos.x, "y": pos.y + 2})
        if pos.y == self.height - 1:
            return Pos({"x": pos.x, "y": pos.y - 1}), Pos({"x": pos.x, "y": pos.y - 2})

    def is_pos_safe(
            self,
            pos: Pos,
            snake_id: str,
            turn: Optional[str] = "done"
    ) -> tuple[bool, bool]:
        """
        Determine if a location on the board is safe (e.g. if it's out-of-bounds or hits a different snake) or risky
        (e.g. if there's a chance of a head-to-head collision). Can be used in the middle of running the minimax
        algorithm, but make sure to specify the "turn" parameter depending on where we are in the minimax tree.

        :param pos: Any location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param snake_id: The ID of the desired snake we're evaluating a move for
        :param turn: Either "ours", "opponents", "done", or "basic". Addresses nuances with running this function during
            the minimax algorithm or independently.
            - If "ours", this means we're at a depth where our snake has to make a move.
            - If "opponents", then we're at a depth where we've made a move but the opponent snakes haven't.
            - If "done", then both our snake and the opponents' have made moves (and 1 full turn has been completed).
            - If "basic", then only check to see if the snake goes out-of-bounds or hits any snake without considering
                collisions (for flood fill purposes).

        :return:
            True if the square is safe, False otherwise
            True if the square is risky, False otherwise
        """
        # Prevent snake from moving out of bounds
        if pos.x < 0 or pos.x >= self.width:
            return False, True
        if pos.y < 0 or pos.y >= self.height:
            return False, True

        # Prevent snake from moving into a hazard
        if pos in self.hazards:
            return False, True

        # Prevent snake from colliding with other snakes
        length = self.all_snakes[snake_id].length
        risky_flag = False
        for opp_num, (opp_id, opp_snake) in enumerate(self.all_snakes.items()):

            # Different rules apply during the middle of running minimax, depending on whose turn it is since our snake
            # makes moves separately from opponent snakes
            if turn == "ours":
                # We can run into the tail of any snake since it will have to move forward
                if snake_id != opp_id and pos in opp_snake.body[:-1]:
                    return False, True
                # Weird edge cases where our head is fed into the function (it's technically safe)
                elif snake_id == opp_id and pos in opp_snake.body[1:-1]:
                    return False, True
                # Flag a move as risky if it could lead to a losing head-to-head collision
                elif (snake_id != opp_id  # Skip the same snake we're evaluating
                      and length <= opp_snake.length  # Only if the other snake is the same length or longer
                      and pos.manhattan_dist(opp_snake.head) <= 2):  # Only if we're collision-bound
                    risky_flag = True

            elif turn == "opponents":
                if opp_num == 0:  # Specific situations against our snake
                    # Our snake's tail is off-limits since we will already have moved
                    if pos in opp_snake.body[1:]:
                        return False, True
                    # Avoid losing head-to-head collisions with our snake. Suicidal collisions (when our snake is the
                    # same length) are risky, but technically still safe
                    elif pos == opp_snake.head:
                        if length < opp_snake.length:
                            return False, True
                        elif length == opp_snake.length:
                            return True, True
                else:
                    # Tail is fine against other opponents
                    if pos in opp_snake.body[:-1]:
                        return False, True
                    # Flag a move as risky if it could lead to a losing head-to-head collision
                    elif (snake_id != opp_id  # Skip the same snake we're evaluating
                          and length <= opp_snake.length  # Only if the other snake is the same length or longer
                          and pos.manhattan_dist(opp_snake.head) == 1):  # Only if we're collision-bound
                        risky_flag = True

            elif turn == "done":
                # Move is invalid if it collides with the body of any snake
                if pos in opp_snake.body[1:]:
                    return False, True
                # Move is invalid if it collides with the head of a snake that is the same length or longer
                elif snake_id != opp_id and pos == opp_snake.head and length <= opp_snake.length:
                    return False, True

            elif turn == "basic":
                if pos in opp_snake.body:
                    return False, True
                elif (snake_id != opp_id  # Skip the same snake we're evaluating
                      and length <= opp_snake.length  # Only if the other snake is the same length or longer
                      and pos.manhattan_dist(opp_snake.head) == 1):  # Only if we're collision-bound
                    risky_flag = True

        return True, risky_flag

    def remove_snake(self, snake_ids: list):
        for snake_id in snake_ids:
            snake = self.all_snakes[snake_id]
            for rm in snake.body:
                self.board[rm.x][rm.y] = " "
            # temp_graph, _ = self.check_missing_nodes(self.graph, [pos.as_tuple() for pos in snake.body])
            self.all_snakes.pop(snake_id)

    def flood_fill_database(
            self,
            initialise: Optional[bool] = False,
            add: Optional[bool] = False,
            check: Optional[bool] = False
    ):
        if initialise:
            ff_db = {}
            for snake in self.all_snakes.values():
                ff_db[snake.id] = {"full_package": [], "confine_to": [], }
        if add:
            pass
        if check:
            pass


    def flood_fill(
            self,
            snake_id: str,
            risk_averse: Optional[bool] = True,
            confine_to: Optional[str] = None,
            confined_dist: Optional[int] = 3,
            fast_forward: Optional[int] = 0,
            opp_cutoff: Optional[str] = None,
            get_boundaries: Optional[bool] = False,
            get_touching_opps: Optional[bool] = False,
            full_package: Optional[bool] = False,
            ff_split: Optional[bool] = False
    ) -> int | tuple[int, list[Pos]]:
        """
        Recursive function to get the total available space for a given snake. Basically, count how many £ symbols
        we can fill while avoiding any obstacle symbols

        :param snake_id: The ID of the desired snake we want to do flood fill for
        :param risk_averse: If True, flood fill will avoid any squares that directly border a longer opponent's head
        :param confine_to: Tells the function to do flood fill for only on one side of the snake (either "left",
            "right", "up", or "down") to represent its peripheral vision
        :param confined_dist:
        :param fast_forward: Hypothetical scenarios where we want to see how much space we still have after moving
            X turns ahead. E.g. if we set it to 5, then we remove 5 squares from all snake's tails before doing flood
            fill - this is only useful when we suspect we'll be trapped by an opponent snake.
        :param opp_cutoff: Input any opponent snake ID and see how much space we still have after our opponent "cuts off"
            our space. E.g. assume the opponent keeps going forward until it meets the edge of the board or an obstacle.
        :param get_boundaries: Option to return a list of positions that represent the edges of our flood fill
        :param get_touching_opps: Option to return a list of other snakes whose heads our flood fill is touching
        :param full_package: Option to run 4 parameters at once with a single function call: risk_averse=True,
            risk_averse=False, get_boundaries=True, and get_touching_opps=True

        :return:
            The total area of the flood fill selection
            Optionally, a list of other snakes whose heads our flood fill is touching
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

        # Cases where our tail is directly adjacent to our head and in the way of our flood fill
        if head.manhattan_dist(snake.tail) == 1:
            board[snake.tail.x][snake.tail.y] = " "

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
            while not self.is_pos_safe(opp_new_head, opp_cutoff, turn="basic")[1]:
                board[opp_new_head.x][opp_new_head.y] = "x"
                opp_new_head = opp_new_head.moved_to(opp_snake.facing_direction(), 1)
                moved_ahead += 1

        # Narrow down a portion of the board that represents the snake's peripheral vision
        if confine_to is not None:
            xs, ys, new_head = snake.peripheral_vision(
                confine_to, dist=confined_dist, width=self.width, height=self.height)
            board = board[xs[0]:xs[1], ys[0]:ys[1]]
            # Account for the board change
            if full_package:
                shifted_risky_squares = []
                for risky_pos in risky_squares:
                    if risky_pos.within_bounds([xs, ys]):
                        shift_x, shift_y = new_head.x - head.x, new_head.y - head.y
                        new_risky_pos = Pos({"x": risky_pos.x + shift_x, "y": risky_pos.y + shift_y})
                        shifted_risky_squares.append(new_risky_pos)
                risky_squares = shifted_risky_squares
            # Update our snake's head pointer to adjust to the cropped board
            head = new_head

        def fill(x, y, board, initial_square, avoid_risk):
            if board.size == 0:  # Empty board
                return
            if board[x][y] == self.obstacles[0]:  # Opponent snake heads
                heads_in_contact.append(Pos({"x": x, "y": y}))
                boundaries.append(Pos({"x": x, "y": y}))
                return
            if board[x][y] in (self.obstacles if avoid_risk else self.obstacles[:-1]):  # Off-limit squares
                boundaries.append(Pos({"x": x, "y": y}))
                return
            if board[x][y] in "£" and not initial_square:  # Already filled
                return

            board[x][y] = "£"
            avoid_sq = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for n in avoid_sq:
                # if 0 <= n[0] < board_width and 0 <= n[1] < board_height:
                if min_x <= n[0] < max_x and min_y <= n[1] < max_y:
                    fill(n[0], n[1], board, initial_square=False, avoid_risk=avoid_risk)

        boundaries = []
        heads_in_contact = []
        # board_width, board_height = len(board), len(board[0])
        crop = 5
        if confine_to is not None:
            min_x, max_x = 0, len(board)
            min_y, max_y = 0, len(board[0])
        else:
            min_x, max_x = max(0, head.x - crop), min(self.width, head.x + crop)
            min_y, max_y = max(0, head.y - crop), min(self.height, head.y + crop)
        if ff_split:
            fill(head.moved_to("left").x, head.moved_to("left").y, board, initial_square=False, avoid_risk=risk_averse)
            left_filled = sum((row == "£").sum() for row in board)
            fill(head.moved_to("right").x, head.moved_to("right").y, board, initial_square=False, avoid_risk=risk_averse)
            right_filled = sum((row == "£").sum() for row in board) - left_filled + 1
            flood_fill_ra = max(left_filled - 1, 1e-15) if left_filled > right_filled else max(right_filled - 1, 1e-15)
        else:
            fill(head.x, head.y, board, initial_square=True, avoid_risk=risk_averse)
            filled = sum((row == "£").sum() for row in board)
            flood_fill_ra = max(filled - 1, 1e-15)  # Exclude the head from the count, but cannot ever be negative

        if full_package:
            # Repeat but assume all risky squares are fair game
            for risky_sq in risky_squares:
                # Situations where our snake's head was previously overwritten by a risky square
                if risky_sq == head and board[risky_sq.x][risky_sq.y] != "£":
                    board[risky_sq.x][risky_sq.y] = "£"
                    fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
                # Ensure that the skipped square can be connected to the main flood fill
                surr_risks = risky_sq.adjacent_pos(len(board), len(board[0]))
                for surr_risk in surr_risks:
                    if board[surr_risk.x][surr_risk.y] == "£":
                        # Remove from the list of boundary squares and update the fill
                        if risky_sq in boundaries:
                            boundaries = [pos for pos in boundaries if pos != risky_sq]
                        fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
                        break
            filled = sum((row == "£").sum() for row in board)
            flood_fill_all = max(filled - 1, 1e-15)

        if get_boundaries:
            return flood_fill_ra, boundaries
        elif get_touching_opps:
            return flood_fill_ra, heads_in_contact
        elif full_package:
            if confine_to is None:
                self.space_ra = flood_fill_ra
                self.space_all = flood_fill_all
                self.ff_bounds = list(set(boundaries))
                self.touch_opps = list(set(heads_in_contact))
                return self.space_ra, self.space_all, self.ff_bounds, self.touch_opps
            else:
                return flood_fill_ra, flood_fill_all, list(set(boundaries)), list(set(heads_in_contact))
        else:
            return flood_fill_ra
