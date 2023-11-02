from __future__ import annotations
import copy
import networkx as nx
import numpy as np
from typing import Optional, Union
from Pos import Pos
from Snake import Snake


class Board:
    def __init__(self, board_dict: dict, all_snakes: dict[str, Snake]):
        """
        Represents our Battlesnake board in any given state. Provides visualisations useful for debugging and can
        perform flood fill.

        :param board_dict: The board portion of the move API request
        :param all_snakes: To avoid repeating code, input previously loaded snakes
        """
        self.width = board_dict["width"]
        self.height = board_dict["height"]
        self.food = [Pos(xy) for xy in board_dict["food"]]
        self.hazards = [Pos(xy) for xy in board_dict["hazards"]]
        self.all_snakes = all_snakes
        self.board = np.full((self.width, self.height), " ")
        self.graph = nx.grid_2d_graph(self.width, self.height)
        self.update_board()

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

    def __str__(self):
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
        """
        board_str = ""
        for j in range(1, len(self.board[0]) + 1):
            display_row = f"{self.height - j}\t "
            for i in range(0, len(self.board)):
                display_row += f"{self.board[i][-j]}| "
            # Add snake length information
            if j <= len(self.all_snakes):
                jth_snake = list(self.all_snakes.values())[j - 1]
                display_row += f"\t\t\tSnake {j - 1}: {jth_snake.length}"
            board_str += display_row + "\n"
        board_str += "\n\t " + "  ".join(map(str, np.arange(0, self.width)))
        return board_str

    def as_dict(self):
        d = dict()
        d["width"] = self.width
        d["height"] = self.height
        d["hazards"] = [ pos.as_dict() for pos in self.hazards ]
        d["food"] = [ pos.as_dict() for pos in self.food ]
        d["snakes"] = [ snake.as_dict() for snake in self.all_snakes.values() ]
        return d

    def closest_dist(self, start: Pos, end: Pos) -> int:
        """
        Get the best approximation for the distance between two positions. When possible, use Dijkstra's algorithm to
        get an exact path, but if that's not possible (e.g. due to obstructions), use the Manhattan distance.

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board

        :return: The closest distance (either using Dijkstra's or Manhattan) between the start and end inputs
        """
        closest = self.dijkstra_shortest_dist(start, end)
        if closest == 1e6:
            closest = start.manhattan_dist(end)
        return closest

    def dijkstra_shortest_dist(self, start: Pos, end: Pos) -> int:
        """
        Return the shortest path between two positions using Dijkstra's algorithm implemented in networkx

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board

        :return: The shortest distance between the start and end inputs. 1e6 if no path could be found
        """
        start = start.as_tuple()
        end = end.as_tuple()
        temp_graph, temp_added_nodes = self.check_missing_nodes(self.graph, [start, end])

        # Run networkx's Dijkstra method (it'll error out if no path is possible)
        try:
            path = nx.shortest_path(temp_graph, start, end)
            shortest = len(path)
        except nx.exception.NetworkXNoPath:
            shortest = 1e6

        for temp_nodes in temp_added_nodes:
            temp_graph.remove_node(temp_nodes)
        return shortest

    @staticmethod
    def check_missing_nodes(G: nx.Graph, nodes: list[tuple]):
        # If the desired location is on a hazard/snake, then it's absent from the graph, and we want to add in the node
        added = []
        for num, node in enumerate(nodes):
            if node not in G.nodes():
                added.append(node)
                G.add_node(node)
                x, y = node
                # Include edges to connect the added node to surrounding nodes if possible
                possible_edges = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for e in possible_edges:
                    if e in G.nodes:
                        G.add_edge(node, e)
        return G, added

    def stall_path(self, start: Pos, end: Pos) -> int:
        """
        Return the longest path between two positions using algorithm implemented in networkx

        :param start: A location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param end: A different location on the board

        :return: The longest distance between the start and end inputs. 1e6 if no path could be found
        """
        start = start.as_tuple()
        end = end.as_tuple()
        temp_graph, temp_added_nodes = self.check_missing_nodes(self.graph, [start, end])

        find_longest = [path for path in nx.all_simple_paths(temp_graph, start, end)]
        if len(find_longest) > 0:
            longest_path = max(find_longest, key=lambda path: len(path))
            longest = len(longest_path) - 1
        else:
            longest = 1e6
        for temp_nodes in temp_added_nodes:
            temp_graph.remove_node(temp_nodes)
        return longest

    def dist_to_nearest_food(self, snake_id) -> tuple[int, Pos]:
        """Return the shortest distance to food for our snake, but only if we're closer to it than an opponent snake"""
        best_dist = np.inf
        best_food = None
        you = self.all_snakes[snake_id]
        opponents = [snake for snake in self.all_snakes.values() if snake.id != snake_id]
        for food in self.food:
            dist = self.dijkstra_shortest_dist(food, you.head)
            # If an enemy snake is longer than ours, and we're both 2 squares away from food, then they're technically
            # closer to it since they'd win the head-to-head battle.
            dist_enemy = min([self.dijkstra_shortest_dist(food, snake.head) if snake.length < you.length
                              else self.dijkstra_shortest_dist(food, snake.head) - 1
                              for snake in opponents])
            if dist < best_dist and dist_enemy >= dist:
                best_dist = dist
                best_food = food
        return best_dist, best_food

    def is_pos_safe(
            self,
            pos: Pos,
            snake_id: str,
            turn: Optional[str] = "done"
    ) -> tuple[bool, bool]:
        """
        Determine if a location on the board is safe (e.g. if it's out-of-bounds or hits a different snake) or risky
        (e.g. if there's a chance of a head-to-head collision). Can be used in the middle of running the minimax
        algorithm, but make sure to specify the "turn_over" parameter.

        :param pos: Any location on the board as a Pos object e.g. Pos({"x": 5, "y": 10})
        :param snake_id: The ID of the desired snake we're evaluating a move for
        :param turn: Either "ours", "opponents", "done", or "basic". Addresses nuances with running this function during
            the minimax algorithm or outside of it.
            - If "ours", this means we're at a depth where our snake has to make a move.
            - If "opponents", then we're at a depth where we've made a move but the opponent snakes haven't. If "done",
              then both our snake and the opponent snakes have made moves (and one complete turn has been completed).
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
                # We cannot hit our own head
                elif snake_id == opp_id and pos in opp_snake.body[1:-1]:
                    return False, True
                # Flag a move as risky if it could lead to a losing head-to-head collision
                elif (snake_id != opp_id  # Skip the same snake we're evaluating
                      and length <= opp_snake.length  # Only if the other snake is the same length or longer
                      and pos.manhattan_dist(opp_snake.head) == 2):  # Only if we're collision-bound
                    risky_flag = True

            elif turn == "opponents":
                if opp_num == 0:  # Our snake
                    # Our snake's tail is off-limits since we will already have moved
                    if pos in opp_snake.body[1:]:
                        return False, True
                    # Avoid losing head-to-head collisions with our snake, but suicidal collisions are fine if our snake
                    # is the same length and also dies
                    elif pos == opp_snake.head and length < opp_snake.length:
                        return False, True
                else:
                    # Tail is fine against other opponents
                    if pos in opp_snake.body[:-1]:
                        return False, True
                    # Flag a move as risky if it could lead to a losing head-to-head collision
                    elif (snake_id != opp_id  # Skip the same snake we're evaluating
                          and length <= opp_snake.length  # Only if the other snake is the same length or longer
                          and pos.manhattan_dist(opp_snake.head) == 2):  # Only if we're collision-bound
                        risky_flag = True

            elif turn == "done":
                # Move is invalid if it collides with the body of a snake
                if pos in opp_snake.body[1:]:
                    return False, True
                # Move is invalid if it collides with the head of a snake that is the same length or longer
                elif snake_id != opp_id and pos == opp_snake.head and length <= opp_snake.length:
                    return False, True

            elif turn == "basic":
                if pos in opp_snake.body:
                    return False, True

        return True, risky_flag

    def flood_fill(
            self,
            snake_id: str,
            confined_area: Optional[str] = None,
            risk_averse: Optional[bool] = False,
            fast_forward: Optional[int] = 0,
            return_boundaries: Optional[bool] = False,
            return_touching_opps: Optional[bool] = False
    ) -> int | tuple[int, list]:
        """
        Recursive function to get the total available space for a given snake. Basically, count how many £ symbols
        we can fill while avoiding any obstacle symbols e.g. "1", "2", ".", etc.

        :param snake_id: The ID of the desired snake we want to do flood fill for
        :param confined_area: Tells the function to do flood fill for only on one side of the snake (either "left",
            "right", "up", or "down") to represent its peripheral vision
        :param risk_averse: If True, flood fill will avoid any squares that directly border an opponent's head
        :param fast_forward: Hypothetical scenarios where we want to see how much space we still have after moving
            X turns ahead. E.g. if we set it to 5, then we remove 5 squares from all snake's tails before doing flood
            fill - this is only useful when we suspect we'll be trapped by an opponent snake.
        :param return_boundaries: Option to return a list of positions that represent the edges of our flood fill
        :param return_touching_opps: Option to return a list of other snakes whose heads our flood fill is touching

        :return:
            The total area of the flood fill selection
            Optionally, a list of other snakes whose heads our flood fill is touching
        """
        board = copy.deepcopy(self.board)
        head = self.all_snakes[snake_id].head
        board[head.x, head.y] = "£"  # Representing our flood fill
        obstacles = [str(num) for num in range(0, 9)] + ["x"]

        # See how flood fill changes when all snakes fast-forward X turns
        if fast_forward > 0:
            for snake in self.all_snakes.values():
                remove_tail = max(-snake.length + 1, -fast_forward)
                for rm in snake.body[remove_tail:]:
                    board[rm.x][rm.y] = " "

        # Avoid any squares that our enemy can go to
        if risk_averse:
            threats = [other.head for other in self.all_snakes.values()
                       if other.id != snake_id and other.length >= self.all_snakes[snake_id].length]
            for threat in threats:
                risky_squares = threat.adjacent_pos(self.width, self.height)
                for risky_pos in risky_squares:
                    if head == risky_pos:
                        board[risky_pos.x][risky_pos.y] = "x"

        # Narrow down a portion of the board that represents the snake's peripheral vision
        if confined_area is not None:
            pass
            xs, ys, head = self.all_snakes[snake_id].peripheral_vision(confined_area, self.width, self.height)
            board = board[xs[0]:xs[1], ys[0]:ys[1]]

        def fill(x, y, board, initial_square):
            if board[x][y] == "$":  # Opponent snake heads
                heads_in_contact.append(Pos(x, y))
                boundary_pos.append(Pos(x, y))
                return
            if board[x][y] in obstacles:  # Off-limit squares
                boundary_pos.append(Pos(x, y))
                return
            if board[x][y] in "£" and not initial_square:  # Already filled
                return
            
            board[x][y] = "£"
            neighbours = Pos(x, y).adjacent_pos(len(board), len(board[0]))
            for n in neighbours:
                fill(n.x, n.y, board, initial_square=False)

        boundary_pos = []
        heads_in_contact = []
        fill(head.x, head.y, board, initial_square=True)
        filled = sum((row == "£").sum() for row in board)
        flood_fill = max(filled - 1, 0)  # Exclude the head from the count, but cannot ever be negative

        if return_boundaries:
            return flood_fill, boundary_pos
        elif return_touching_opps:
            return flood_fill, heads_in_contact
        else:
            return flood_fill
