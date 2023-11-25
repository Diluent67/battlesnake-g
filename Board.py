from __future__ import annotations
import copy
import cv2
import networkx as nx
import numpy as np
from typing import Optional, Union
from Pos import Pos
from Snake import Snake


class Board:
    def __init__(self, game_state: dict):
        """
        Represents our Battlesnake board in any given state. Provides visualisations useful for debugging and performs
        flood fill + pathfinding.

        :param game_state: The move API request (https://docs.battlesnake.com/api/example-move#move-api-response)
        """
        board_dict = game_state["board"]
        self.width = board_dict["width"]
        self.height = board_dict["height"]

        # Process food locations as Pos objects, but skip if previously done
        food_locs = board_dict.get("food", [])
        if len(food_locs) > 0 and isinstance(food_locs[0], Pos):
            self.food = food_locs
        else:
            self.food = [Pos(xy) for xy in food_locs]

        # Process hazard locations as Pos objects, but skip if previously done
        hazard_locs = board_dict.get("hazards", [])
        if len(hazard_locs) > 0 and isinstance(hazard_locs[0], Pos):
            self.hazards = hazard_locs
        else:
            self.hazards = [Pos(xy) for xy in hazard_locs]

        # Process all snakes as a dictionary of Snake objects with their IDs as lookups
        you_snake = Snake(game_state["you"])
        self.all_snakes: dict[str, Snake] = {you_snake.id: you_snake}   # Our snake should be the first one
        for snake_dict in board_dict["snakes"]:
            if snake_dict["id"] == you_snake.id:
                continue
            self.all_snakes[snake_dict["id"]] = Snake(snake_dict)

        # Represent the Battlesnake board as a Numpy array and a NetworkX graph
        self.board = np.zeros((self.width, self.height))
        self.graph = nx.grid_2d_graph(self.width, self.height)

        # TODO put these as class variables?
        self.obstacles = [10] + np.arange(11, 99, 11).tolist() + [255]
        self.board_translation = {
            0: " ",  # Empty space
            1: "£",  # Starting point for flood fill
            10: "H",  # Snake head
            11: "1", 22: "2", 33: "3", 44: "4", 55: "5", 66: "6", 77: "7", 88: "8",  # Up to 8 snakes
            100: "f",  # Food
            255: "x",  # Hazards or off-limit squares
            "O": "O"  # For visualising nodes with "display_graph"
        }

    def as_dict(self):
        return {
            "height": self.height,
            "width": self.width,
            "food": [pos.as_dict() for pos in self.food],
            "hazards": [pos.as_dict() for pos in self.hazards],
            "snakes": [snake.as_dict() for snake in self.all_snakes.values()]
        }

    def update_board(self):
        """
        Fill in the board with the locations of all snakes, food, and hazards.

        The Battlesnake board is represented in two ways:

        Numpy array (uint8 data type for compatibility with OpenCV's flood fill function)
            - 0 = empty square
            - 1-8 = up to 8 snakes
            - 10 = snake head
            - 50 = starting point for flood fill
            - 100 = food
            - 255 = hazards or off-limit squares

        NetworkX graph (to use NetworkX's implementation of Dijkstra's algorithm)
            - Node = empty square
            - No node = occupied by a snake or hazard, so it's unreachable
        """
        for f in self.food:
            self.board[f.x, f.y] = 100

        for h in self.hazards:
            self.board[h.x, h.y] = 255
            self.graph.remove_node(h.as_tuple())

        for snake_num, snake in enumerate(self.all_snakes.values()):
            skip_tail = snake.body[-2] == snake.tail
            for pos_num, pos in enumerate(snake.body):
                if skip_tail and pos_num == len(snake.body) - 1:
                    continue

                self.board[pos.x, pos.y] = 10 if pos_num == 0 else 11 * (snake_num + 1)
                # Keep any nodes that coincide with the position of our snake's head for future pathfinding
                if not (snake_num == 0 and pos_num == 0):
                    self.graph.remove_nodes_from([pos.as_tuple()])

    def display(
            self,
            board: Optional[np.array] = None,
            show: Optional[bool] = True,
            add_lengths: Optional[bool] = True
    ) -> str:
        """
        Convert the board's Numpy array representation into a nicely formatted string for convenient debugging, e.g.

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
        :param show: Option to print the board automatically or not
        :param add_lengths: Option to add a column of information showing all snake lengths

        :return: The board represented as a formatted string
        """
        board = self.board if board is None else board
        board_str = ""
        for j in range(1, len(board[0]) + 1):
            display_row = f"{self.height - j}\t "
            for i in range(0, len(board)):
                display_row += f"{self.board_translation[board[i][-j]]}| "
            # Add snake length information
            if add_lengths:
                if j <= len(self.all_snakes):
                    jth_snake = list(self.all_snakes.values())[j - 1]
                    display_row += f"\t\t\tSnake {j}: {jth_snake.length}"
            board_str += display_row + "\n"
        board_str += "\n\t " + "  ".join(map(str, np.arange(0, self.width)))

        if show:
            print(board_str)
        else:
            return board_str

    def display_graph(self, show: Optional[bool] = True) -> str:
        """Convert the board's NetworkX graph representation into a nicely formatted string for convenient debugging."""
        board = np.full((self.width, self.height), 0)
        for node in self.graph.nodes:
            board[node[0], node[1]] = "O"
        return self.display(board=board, show=show)

    def identify_snake(self, pos: Pos) -> Snake | None:
        """Given any position on the board, return the Snake lying on top of it."""
        matches = [snake for snake in self.all_snakes.values() if pos in snake.body]
        if len(matches) == 0:
            return None
        # If multiple snakes occupy the position, return the longest snake
        if len(matches) > 1:
            matches = sorted(matches, key=lambda snake: snake.length, reverse=True)
        return matches[0]

    def shortest_dist(self, start: Pos, end: Pos) -> int:
        """
        Get the best approximation for the distance between two positions. When possible, use Dijkstra's algorithm to
        get an exact path, but if that's not possible (e.g. due to obstructions), return 1e6 + the Manhattan distance.

        To illustrate the rationale, let's say we have to compare the distance between A to each of (B, C, D):
            - A -> B is unreachable with a default Dijkstra output of 1e6, but has a Manhattan distance of 2
            - A -> C is reachable with a Dijkstra output of 15, but a Manhattan distance of 10
            - A -> D is unreachable with a default Dijkstra output of 1e6, but has a Manhattan distance of 5
        Which point is closer to A? Obviously C if we go with Dijkstra's algorithm, but then B and D both have the same
        1e6 outputs. To discern which point is hypothetically closer, we set B => 1e6 + 2 and D => 1e6 + 5, which lets
        us select B as the closer point to D!

        :param start: A location on the board as a Pos object, e.g. Pos({"x": 5, "y": 10})
        :param end: Another location on the board

        :return: The closest distance between the start and end points. If there's no connecting path, approximate with
            1e6 + the Manhattan distance.
        """
        closest = self.dijkstra_shortest_path(start, end)
        if closest == 1e6:
            closest += start.manhattan_dist(end)
        return closest
    
    def longest_paths_to_stall(  # TODO revisit this I'm confused if we need both outputs tbh
            self,
            start: Pos,
            end: Pos,
            min_length: int,
            simple_paths_cutoff: int
    ) -> tuple[int, int]:
        """
        Compute the longest paths between two positions (relevant during efforts to stall and escape a trapped area). As
        an example, if our snake is trapped, and an opening in our surrounding area forms in 5 moves, we want to 
        know whether we can stall for 5 moves successfully. 

        :param start: A location on the board as a Pos object, e.g. Pos({"x": 5, "y": 10})
        :param end: Another location on the board
        :param min_length: The minimum amount of moves required to stall (e.g. before more space opens up)
        :param simple_paths_cutoff: The maximum path length to stop NetworkX's search while running "all_simple_paths". 
            Only paths of length <= cutoff are returned.

        :return: 
            The longest distance between the start and end inputs 
            The sho
        """
        start = start.as_tuple()
        end = end.as_tuple()
        # Ensure the start and end positions exist as nodes on the graph so NetworkX can find a path between them
        temp_added_nodes = self.check_missing_nodes(self.graph, [start, end])

        longest = 1e6
        shortest = 1e6
        # Find all possible paths between the two points (below the desired cutoff) 
        possible_paths = [path for path in nx.all_simple_paths(self.graph, start, end, cutoff=simple_paths_cutoff)]
        if len(possible_paths) > 0:
            # Filter for the longest path
            longest_path = max(possible_paths, key=lambda path: len(path))
            longest = len(longest_path) - 1
            # Now filter for the shortest path that's longer than the inputted minimum length
            shortest = longest
            paths_above_threshold = [path for path in possible_paths if len(path) > min_length]
            if len(paths_above_threshold) > 0:
                shortest_path = min(paths_above_threshold, key=lambda path: len(path))
                shortest = len(shortest_path) - 1

        # Remove any temporary nodes that were previously added
        self.graph.remove_nodes_from(temp_added_nodes)

        return longest, shortest

    def dijkstra_shortest_path(
            self,
            start: Pos,
            end: Pos,
            snake_id: Optional[str] = None,
            return_full_path: Optional[bool] = False
    ) -> int | tuple[int, list]:
        """
        Compute the shortest path between two positions using Dijkstra's algorithm implemented in NetworkX.

        :param start: A location on the board as a Pos object, e.g. Pos({"x": 5, "y": 10})
        :param end: Another location on the board
        :param snake_id: The ID of the snake we're finding a path for
        :param return_full_path: Option to include the complete path identified by the algorithm in the output

        :return: The shortest distance between the start and end inputs (1e6 if no path could be found)
        """
        # Running Dijkstra's is time-consuming, so skip over scenarios where the additional accuracy is negligible
        if (manhattan_approx := start.manhattan_dist(end)) >= 10:
            return (manhattan_approx, None) if return_full_path else manhattan_approx

        start = start.as_tuple()
        end = end.as_tuple()
        # Ensure the start and end positions exist as nodes on the graph so NetworkX can find a path between them
        check_nodes = [start, end]
        # If a snake tail is directly adjacent to our head, then the tail is a free square TODO: All tails adjacent to our head are free?
        if snake_id is not None:
            our_snake = self.all_snakes[snake_id]
            if our_snake.head.manhattan_dist(our_snake.tail) == 1:
                check_nodes.append(our_snake.tail.as_tuple())
        temp_added_nodes = self.check_missing_nodes(self.graph, check_nodes)

        try:
            path = nx.shortest_path(self.graph, start, end)
            shortest = len(path)
        except nx.exception.NetworkXNoPath:
            path = None
            shortest = 1e6

        # Remove any temporary nodes that were previously added
        self.graph.remove_nodes_from(temp_added_nodes)

        if return_full_path:
            return shortest, path
        else:
            return shortest

    @staticmethod
    def check_missing_nodes(G: nx.Graph, nodes_to_check: list[tuple]) -> list:
        """
        A helper function to use with Dijkstra's algorithm implemented in NetworkX. If the graph representation of the
        Battlesnake board doesn't contain a node at a desired position, the NetworkX "shortest_path" function will error
        out since it can't compute a path to a non-existent node. This function temporarily adds a node at that position
        (if it wasn't already present) and creates edges to neighbouring nodes.

        :param G: A graph representation of the board
        :param nodes_to_check: A list of nodes to temporarily add to the graph

        :return: A list of nodes that were temporarily added
        """
        added_nodes = []
        node_count = G.number_of_nodes()
        for node in nodes_to_check:
            G.add_node(node)
            # Add edges between the added node and any surrounding nodes
            x, y = node
            possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for e in possible_edges:
                if G.has_node(e):
                    G.add_edge(node, e)
            # Keep track of any new nodes that were added
            if (node_count := G.number_of_nodes() - node_count) > 0:
                added_nodes.append(node)

        return added_nodes

    def closest_food(self, snake_id, risk_averse=True) -> tuple[int, Pos]:
        """
        Compute the shortest distance to food, but ignore any that an opponent snake could reach first or any that could 
        lead to death via entrapment or edge kill.

        :param snake_id: The ID of the snake we want to find food for
        :param risk_averse: Option to avoid any food that could lead to our death

        :return:
            The shortest distance to food
            The location of the food as a Pos object
        """
        you = self.all_snakes[snake_id]
        opponents = [snake for snake in self.all_snakes.values() if snake.id != snake_id]

        best_dist, best_food = np.inf, None
        sorted_food = sorted(self.food, key=lambda f: you.head.manhattan_dist(f))  # Pre-sort for efficiency
        for food in sorted_food:
            dist_food = self.dijkstra_shortest_path(food, you.head)
            opp_dist_food, food_edge_killed = 1e6, False
            
            # The idea is to ignore any food that an opponent can reach first and any food that can lead to an edge kill
            if risk_averse:
                # Find which opponents are equally close to the same food as us (use the Manhattan distance to estimate)
                closest_opps = [opp for opp in opponents if opp.head.manhattan_dist(food) <= dist_food]
                # Then double-check more accurately using Dijkstra's algorithm (to minimise Dijkstra runtime)
                if len(closest_opps) > 0:
                    # A longer enemy snake is technically closer to the same food since it'd win the head-to-head battle
                    opp_dist_food = min(
                        [self.dijkstra_shortest_path(food, snake.head) - 1 if (
                                snake.length >= you.length) else self.dijkstra_shortest_path(food, snake.head) 
                         for snake in closest_opps]
                    )
                # Look ahead to avoid getting edge-killed from getting the food TODO: entrapment next?
                if food.x in [0, self.width - 1] or food.y in [0, self.height - 1]:
                    edge_kill_sqs = self.edge_kill_squares(food)
                    # Check if any enemy snake is on a prime edge-killing square by the time we get to the food
                    for kill_sq in edge_kill_sqs:
                        closest_edge_killer = [opp for opp in opponents if (
                                opp.length > you.length and opp.head.manhattan_dist(kill_sq) <= dist_food - 1)]
                        if len(closest_edge_killer) > 0:
                            food_edge_killed = True
                            break

            # Update our snake's shortest computed distance to food if the coast is clear
            if dist_food < best_dist and opp_dist_food >= dist_food and not food_edge_killed:
                best_dist, best_food = dist_food, food
            # "Prune" on the first instance that we stop updating
            elif best_food is not None:
                break

        return best_dist, best_food

    def evaluate_pos(
            self,
            pos: Pos,
            snake_id: str,
            turn_type: Optional[str] = "over"
    ) -> tuple[bool, bool]:
        """
        Determine if a location on the board is safe (e.g. if it's out-of-bounds or hits a different snake) or risky
        (e.g. if there's a chance of a head-to-head collision). Can be used in the middle of running the minimax
        algorithm, but collision rules (e.g. when it's okay to go to a square occupied by a tail) may vary depending on
        whose turn it is during the tree search, so specify the "turn_type" parameter as necessary.

        :param pos: Any location on the board as a Pos object, e.g. Pos({"x": 5, "y": 10})
        :param snake_id: The ID of the snake we're evaluating a position for
        :param turn_type: Either "you", "opponents", "over", or "basic". Addresses nuances with running this function
            during the minimax tree search or independently.
            - If "you", this means we're at a depth where our snake has to make a move.
            - If "opponents", then we're at a depth where we've made a move, but the opponent snakes haven't.
            - If "over", then both our snake and the opponents' have made moves (and 1 full turn has been completed).
                Useful to determine which snakes have died or not.
            - If "static", then only check to see if the snake goes out-of-bounds or hits any snake without considering
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

        # Prevent snake from colliding with other snakes. While traversing the minimax search tree, collision rules will
        # differ depending on whose turn it is since our snake makes moves separately from opponent snakes.
        length = self.all_snakes[snake_id].length
        risky_flag = False
        for opp_num, (opp_id, opp_snake) in enumerate(self.all_snakes.items()):

            if turn_type == "you":
                # We can run into the tail of any snake since it will have to move forward
                if snake_id != opp_id and pos in opp_snake.body[:-1]:
                    return False, True
                # Weird edge case where our head is fed into the function (it's technically safe)
                elif snake_id == opp_id and pos in opp_snake.body[1:-1]:
                    return False, True
                # Flag a move as risky if it could lead to a losing head-to-head collision
                elif (snake_id != opp_id  # Skip the same snake we're evaluating
                      and length <= opp_snake.length  # Only if the other snake is the same length or longer
                      and pos.manhattan_dist(opp_snake.head) <= 2):  # Only if we're collision-bound
                    if pos.manhattan_dist(opp_snake.head) == 2:  # TODO: why did we put 2?
                        print(pos.as_tuple())
                        print(opp_snake.head.as_tuple())
                        self.display()
                        raise ValueError
                    risky_flag = True

            elif turn_type == "opponents":
                # Specific situations against our snake
                if opp_num == 0:
                    # Our snake's tail is off-limits since we will already have moved
                    if pos in opp_snake.body[1:]:
                        return False, True
                    # Avoid losing head-to-head collisions with our snake. Suicidal collisions (when both snakes are the
                    # same length) are risky, but technically still safe
                    elif pos == opp_snake.head:
                        if length < opp_snake.length:
                            return False, True  # TODO: Can an enemy snake just kill itself?
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

            elif turn_type == "over":
                # Move is invalid if it collides with the body of any snake
                if pos in opp_snake.body[1:]:
                    return False, True
                # Move is invalid if it collides with the head of a snake that is the same length or longer
                elif snake_id != opp_id and pos == opp_snake.head and length <= opp_snake.length:
                    return False, True

            elif turn_type == "static":
                if pos in opp_snake.body:
                    return False, True
                elif (snake_id != opp_id  # Skip the same snake we're evaluating
                      and length <= opp_snake.length  # Only if the other snake is the same length or longer
                      and pos.manhattan_dist(opp_snake.head) == 1):  # Only if we're collision-bound
                    risky_flag = True

        return True, risky_flag

    def remove_snakes(self, snake_ids: list[str]):
        """Manually remove a set of snakes from the board. Might be prone to errors if there's an overlapping snake."""
        for snake_id in snake_ids:
            snake = self.all_snakes[snake_id]
            for rm in snake.body:
                self.board[rm.x, rm.y] = 0
            self.check_missing_nodes(self.graph, [pos.as_tuple() for pos in snake.body])
            self.all_snakes.pop(snake_id)

    def edge_kill_squares(self, pos: Pos) -> tuple[Pos, Pos]:
        """If we're on the edge of the board, we're vulnerable to kills if there's an opponent on these 2 squares."""
        if pos.x == 0:
            return Pos({"x": pos.x + 1, "y": pos.y}), Pos({"x": pos.x + 2, "y": pos.y})
        elif pos.x == self.width - 1:
            return Pos({"x": pos.x - 1, "y": pos.y}), Pos({"x": pos.x - 2, "y": pos.y})
        elif pos.y == 0:
            return Pos({"x": pos.x, "y": pos.y + 1}), Pos({"x": pos.x, "y": pos.y + 2})
        elif pos.y == self.height - 1:
            return Pos({"x": pos.x, "y": pos.y - 1}), Pos({"x": pos.x, "y": pos.y - 2})

    # def flood_fill_database(
    #         self,
    #         initialise: Optional[bool] = False,
    #         add: Optional[bool] = False,
    #         check: Optional[bool] = False
    # ):
    #     if initialise:
    #         ff_db = {}
    #         for snake in self.all_snakes.values():
    #             ff_db[snake.id] = {"full_package": [], "confine_to": [], }
    #     if add:
    #         pass
    #     if check:
    #         pass

    def fast_flood_fill(
            self,
            snake_id: str,
            risk_averse: Optional[bool] = True,
            ff_split: Optional[bool] = False,
            confine_to: Optional[str] = None,
            confined_dist: Optional[int] = 3,
            opp_cutoff: Optional[str] = None,
            full_package: Optional[bool] = False,
    ):
        board = copy.deepcopy(self.board).astype(np.uint8)
        snake = self.all_snakes[snake_id]
        head = snake.head

        # Remove food from the board since it'll block our flood fill
        for f in self.food:
            board[f.x, f.y] = 0

        # Cases where our tail is directly adjacent to our head and therefore in the way of our flood fill TODO: opponent tail as well?
        if head.manhattan_dist(snake.tail) == 1:
            board[snake.tail.x, snake.tail.y] = 0

        # Avoid any squares that could lead to a losing head-to-head collision
        risky_squares = []
        if risk_averse:
            possible_threats = [opp.head for opp in self.all_snakes.values() if (
                    opp.id != snake_id and opp.length >= snake.length)]
            for threat in possible_threats:
                for risky_pos in threat.adjacent_pos(self.width, self.height):
                    if board[risky_pos.x, risky_pos.y] not in self.obstacles:
                        board[risky_pos.x, risky_pos.y] = 255
                        risky_squares.append(risky_pos)

        # See what happens if an opponent were to keep moving forward and "cut off" our space
        if opp_cutoff:
            opp_snake = self.all_snakes[opp_cutoff]
            opp_dir = opp_snake.facing_direction()
            opp_new_head = opp_snake.head.moved_to(opp_dir, 1)
            while not self.evaluate_pos(opp_new_head, opp_cutoff, turn_type="static")[1]:
                board[opp_new_head.x, opp_new_head.y] = 255
                opp_new_head = opp_new_head.moved_to(opp_dir, 1)

            # Narrow down a portion of the board that represents the snake's peripheral vision
        if confine_to is not None:
            xs, ys, new_head = snake.peripheral_vision(
                confine_to, dist=confined_dist, width=self.width, height=self.height)
            board = board[xs[0]:xs[1], ys[0]:ys[1]]
            # Account for the board change if we're running the full package
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

        mask = np.zeros(np.array(board.shape) + 2, dtype=np.uint8)
        if not ff_split:
            board[head.x, head.y] = 0
        if ff_split:
            if snake.facing_direction() in ["left", "right"]:
                start_pt_left = head.moved_to("up").as_tuple()
                start_pt_right = head.moved_to("down").as_tuple()
            else:
                start_pt_left = head.moved_to("left").as_tuple()
                start_pt_right = head.moved_to("right").as_tuple()

            retval_left, _, mask, _ = cv2.floodFill(board, mask, start_pt_left[::-1], 1, flags=4 | cv2.FLOODFILL_MASK_ONLY)
            mask = np.zeros(np.array(board.shape) + 2, dtype=np.uint8)
            retval_right, _, mask, _ = cv2.floodFill(board, mask, start_pt_right[::-1], 1, flags=4 | cv2.FLOODFILL_MASK_ONLY)

            retval = retval_left if retval_left > retval_right else retval_right
            start_pt = start_pt_left if retval_left > retval_right else start_pt_right
            mask = mask[1:-1, 1:-1]  # 1s represent the barriers to the flood fill
        else:
            start_pt = head.as_tuple()
            retval, image2, mask, _ = cv2.floodFill(board, mask, start_pt[::-1], 1, flags=4)
            mask = mask[1:-1, 1:-1]  # 1s represent the barriers to the flood fill

        # Create a structuring element for dilation that only considers up/left/right/down neighbors
        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], np.uint8)
        dilated_array = cv2.dilate(mask, kernel, iterations=1)
        # Find the edges by subtracting the original array from the dilated one
        edge_array = dilated_array - mask
        edge_coordinates = np.column_stack(np.where(edge_array == 1))
        edge_coordinates_set = {tuple(edge) for edge in edge_coordinates}

        if full_package:
            retval_ra = retval
            # Repeat but assume all risky squares are fair game
            for risky_sq in risky_squares:
                board[risky_sq.x, risky_sq.y] = 0

            mask = np.zeros(np.array(board.shape) + 2, dtype=np.uint8)
            retval_all, _, _, _ = cv2.floodFill(board, mask, start_pt[::-1], 1, 1, 1, flags=4 | cv2.FLOODFILL_FIXED_RANGE)

            return max(retval_ra - 1, 1e-15), max(retval_all - 1, 1e-15), edge_coordinates_set

        return max(retval - 1, 1e-15)

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
        Get the total available space for a given snake.

        :param snake_id: The ID of the snake we want to do flood fill for
        :param risk_averse: Option to avoid any squares that directly border a longer opponent's head
        :param confine_to: Tells the function to do flood fill on only one side of the snake (either "left", "right",
            "up", or "down") to represent its peripheral vision
        :param confined_dist: Paired with "confine_to" to determine the depth of the snake's peripheral vision
        :param fast_forward: Hypothetical scenarios where we want to see how much space we still have after moving
            X turns ahead. E.g. if we set it to 5, then we remove 5 squares from all snake's tails before doing flood
            fill - this is only useful when we suspect we'll be trapped by an opponent snake.
        :param opp_cutoff: Input any opponent snake IDs and see how much space we still have after they "cut off" our
            space. Assume the opponents keep going forward until they meet the edge of the board or an obstacle.
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
        board[head.x, head.y] = 1  # Representing our flood fill

        # See how flood fill changes when all snakes fast-forward X turns
        if fast_forward > 0:
            for snake in self.all_snakes.values():
                remove_tail = max(-snake.length + 1, -fast_forward)
                for rm in snake.body[remove_tail:]:
                    board[rm.x, rm.y] = 0

        # Cases where our tail is directly adjacent to our head and therefore in the way of our flood fill TODO: opponent tail as well?
        if head.manhattan_dist(snake.tail) == 1:
            board[snake.tail.x, snake.tail.y] = 0

        # Avoid any squares that could lead to a losing head-to-head collision
        risky_squares = []
        if risk_averse:
            possible_threats = [opp.head for opp in self.all_snakes.values() if (
                    opp.id != snake_id and opp.length >= snake.length)]
            for threat in possible_threats:
                for risky_pos in threat.adjacent_pos(self.width, self.height):
                    if board[risky_pos.x, risky_pos.y] not in self.obstacles:
                        board[risky_pos.x, risky_pos.y] = 255
                        risky_squares.append(risky_pos)

        # See what happens if an opponent were to keep moving forward and "cut off" our space
        if opp_cutoff:
            opp_snake = self.all_snakes[opp_cutoff]
            opp_dir = opp_snake.facing_direction()
            opp_new_head = opp_snake.head.moved_to(opp_dir, 1)
            while not self.evaluate_pos(opp_new_head, opp_cutoff, turn_type="static")[1]:
                board[opp_new_head.x, opp_new_head.y] = 255
                opp_new_head = opp_new_head.moved_to(opp_dir, 1)

        # Narrow down a portion of the board that represents the snake's peripheral vision
        if confine_to is not None:
            xs, ys, new_head = snake.peripheral_vision(
                confine_to, dist=confined_dist, width=self.width, height=self.height)
            board = board[xs[0]:xs[1], ys[0]:ys[1]]
            # Account for the board change if we're running the full package
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
            if board.shape[0] == 0 or board.shape[1] == 0:  # Empty board TODO: remove from recursive
                return
            if board[x][y] == self.obstacles[0]:  # Opponent snake heads
                heads_in_contact.append(Pos({"x": x, "y": y}))
                boundaries.append(Pos({"x": x, "y": y}))
                return
            if board[x][y] in (self.obstacles if avoid_risk else self.obstacles[:-1]):  # Off-limit squares
                boundaries.append(Pos({"x": x, "y": y}))
                return
            if board[x][y] == 1 and not initial_square:  # Already filled
                return

            board[x][y] = 1
            avoid_sq = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for n in avoid_sq:
                # if 0 <= n[0] < board_width and 0 <= n[1] < board_height:
                if min_x <= n[0] < max_x and min_y <= n[1] < max_y:
                    fill(n[0], n[1], board, initial_square=False, avoid_risk=avoid_risk)

        boundaries = []
        heads_in_contact = []
        # board_width, board_height = len(board), len(board[0])
        crop = 6
        min_x, max_x = 0, len(board)
        min_y, max_y = 0, len(board[0])
        # if confine_to is not None:
        #     min_x, max_x = 0, len(board)
        #     min_y, max_y = 0, len(board[0])
        # else:
        #     min_x, max_x = max(0, head.x - crop), min(self.width, head.x + crop)
        #     min_y, max_y = max(0, head.y - crop), min(self.height, head.y + crop)
        if ff_split:
            if snake.facing_direction() in ["left", "right"]:
                left_x, left_y = head.moved_to("up").as_tuple()
                right_x, right_y = head.moved_to("down").as_tuple()
            else:
                left_x, left_y = head.moved_to("left").as_tuple()
                right_x, right_y = head.moved_to("right").as_tuple()
            fill(left_x, left_y, board, initial_square=False, avoid_risk=risk_averse)
            left_filled = sum((row == 1).sum() for row in board)
            fill(right_x, right_y, board, initial_square=False, avoid_risk=risk_averse)
            right_filled = sum((row == 1).sum() for row in board) - left_filled + 1
            flood_fill_ra = max(left_filled - 1, 1e-15) if left_filled > right_filled else max(right_filled - 1, 1e-15)
            undesired = min([left_filled, right_filled])
        else:
            fill(head.x, head.y, board, initial_square=True, avoid_risk=risk_averse)
            filled = sum((row == 1).sum() for row in board)
            flood_fill_ra = max(filled - 1, 1e-15)  # Exclude the head from the count, but cannot ever be negative

        if full_package:
            # Repeat but assume all risky squares are fair game
            for risky_sq in risky_squares:
                # Situations where our snake's head was previously overwritten by a risky square
                if risky_sq == head and board[risky_sq.x][risky_sq.y] != 1:
                    board[risky_sq.x][risky_sq.y] = 1
                    fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
                # Ensure that the skipped square can be connected to the main flood fill
                surr_risks = risky_sq.adjacent_pos(len(board), len(board[0]))
                for surr_risk in surr_risks:
                    if board[surr_risk.x][surr_risk.y] == 1:
                        # Remove from the list of boundary squares and update the fill
                        if risky_sq in boundaries:
                            boundaries = [pos for pos in boundaries if pos != risky_sq]
                        fill(risky_sq.x, risky_sq.y, board, initial_square=True, avoid_risk=False)
                        break
            filled = sum((row == 1).sum() for row in board)
            flood_fill_all = max(filled - 1, 1e-15) if ff_split else max(filled - 1, 1e-15)

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
