from __future__ import annotations
import logging
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import time
from collections import Counter
from networkx_tree import hierarchy_pos
from typing import Any, Optional
from Board import Board
from Pos import Pos
from Snake import Snake

my_name = "Nightwing"
# Use these global variables to add data for visualising the minimax decision tree
tree_tracker = {6: [], 5: [], 4: [], 3: [], 2: [], 1: [], 0: []}
tree_node_counter = 1
tree_edges = []
tree_nodes = []


class Battlesnake:
    def __init__(self, game_state: dict, debugging: Optional[bool] = False):
        """
        Represents our Battlesnake game and includes all our decision-making methods

        :param game_state: The move API request (https://docs.battlesnake.com/api/example-move#move-api-response)
        :param debugging: Set to True if you want to view a log of what's happening behind the minimax algorithm
        """
        # Process our snake using Rick's Snake class
        self.you = Snake(game_state["you"])
        # Weird edge case when running locally where the "you" snake is not our actual snake
        if self.you.name != my_name:
            right_you = [snake_dict for snake_dict in game_state["board"]["snakes"] if snake_dict["name"] == my_name][0]
            self.you = Snake(right_you)

        # Process all snakes as a dictionary of Snake objects with their IDs as a lookup
        self.all_snakes: dict[str, Snake] = {self.you.id: self.you}
        for snake_dict in game_state["board"]["snakes"]:
            if snake_dict["id"] == self.you.id:
                continue
            self.all_snakes[snake_dict["id"]] = Snake(snake_dict)
        # Weird edge case when running locally where our snake is not in the "snakes" field
        if self.you.id not in self.all_snakes.keys():
            self.all_snakes[self.you.id] = self.you

        # Opponent snakes
        self.opponents = self.all_snakes.copy()
        self.opponents.pop(self.you.id)

        # General game data
        self.turn = game_state["turn"]
        self.board = Board(game_state["board"], all_snakes=self.all_snakes)

        # Finish up our constructor
        self.dict = game_state
        self.og_snakes = self.all_snakes.copy()  # For keeping track of which snakes get killed
        self.og_length = self.you.length
        self.minimax_search_depth = 4  # Depth for minimax algorithm
        self.peripheral_size = 3  # Length of our snake's "peripheral vision"
        self.debugging = debugging
        logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
        if not self.debugging:
            logging.disable(logging.INFO)

    def get_obvious_moves(
            self,
            snake_id: str,
            risk_averse: Optional[bool] = True,
            sort_by_dist_to: Optional[str] = None,
            sort_by_peripheral: Optional[bool] = False
    ) -> list:
        """
        Return a list of valid moves for any hypothetical snake.

        :param snake_id: The ID of the desired snake we want to find moves for (can also be any opponent snake).
        :param risk_averse: Return possible moves that avoid death-inducing collisions (essentially we're assuming our
            opponents are out to get us, but only if they're longer). Set False to include any risky moves towards other
            snakes that might kill us.
        :param sort_by_dist_to: Input any snake ID here. This will return all possible moves, but sort the moves by the
            distance from our snake (after making the move) to the head of the snake whose ID was inputted. Very useful
            for discerning which moves are more threatening or bring us closer to a different snake.
        :param sort_by_peripheral: If True, return all possible moves, but sort the moves by the amount of space that
            each move will give us in our "peripheral vision". Very useful for discerning which moves allow us more
            immediate space.

        :return: A (possibly) sorted list of possible moves for the given snake
        """
        # Loop through possible moves and remove from consideration if it's invalid + keep track of risky moves
        possible_moves = ["up", "down", "left", "right"]
        risky_moves = []
        head = self.all_snakes[snake_id].head
        for move in possible_moves.copy():
            is_safe, is_risky = self.board.is_pos_safe(
                head.moved_to(move), snake_id, turn="ours" if snake_id == self.you.id else "opponents")
            if not is_safe or (risk_averse and is_risky):
                possible_moves.remove(move)
            if is_risky:
                risky_moves.append(move)

        # Sort the possible moves if needed
        if len(possible_moves) > 1:
            if sort_by_dist_to is not None:
                head2 = self.all_snakes[sort_by_dist_to].head
                possible_moves = sorted(possible_moves,
                                        key=lambda move2: self.board.shortest_dist(head2, head.moved_to(move2)))
            if sort_by_peripheral:
                possible_moves = sorted(possible_moves,
                                        key=lambda move2: self.board.flood_fill(snake_id, confined_area=move2),
                                        reverse=True)
        # De-prioritise any risky moves and send them to the back
        if len(risky_moves) > 0:
            for risky in risky_moves:
                if risky in possible_moves:
                    possible_moves.append(possible_moves.pop(possible_moves.index(risky)))

        return possible_moves

    def is_game_over(self, for_snake_id: Optional[str] = None, depth: Optional[int] = 4) -> tuple[bool, bool]:
        """
        Determine if the game is over for our snake. Can optionally be used to determine whether any opponent snake is
        dead or not.

        :param for_snake_id: The ID of the desired snake that we want to know died or not
        :param depth: During minimax, things get complicated when we call this function right after making a move for
            our snake but before the opponent snakes have made moves. We only want to return True when a complete turn
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
            is_safe, _ = self.board.is_pos_safe(snake.head, snake_id, turn="done" if depth % 2 == 0 else "ours")
            snake_monitor[snake_id] = is_safe

        # Game is over if there's only one snake remaining or if our snake died
        game_over = True if (sum(snake_monitor.values()) == 1 or not snake_monitor[self.you.id]) else False
        # See if a specific snake is alive or not
        snake_still_alive = snake_monitor[for_snake_id if for_snake_id is not None else self.you.id]

        return game_over, snake_still_alive

    def simulate_move(self, move_dict: dict, evaluate_deaths: Optional[bool] = False) -> Battlesnake:
        """
        Create a new Battlesnake instance that simulates a game turn and makes moves for a set of desired snake IDs. To
        increase speed, this function builds a new game_state dictionary from scratch to generate the new instance
        without affecting the original instance.

        :param move_dict: A dictionary containing moves that we'd like to simulate for a set of snake IDs e.g.
            {self.you.id: "left", other_snake_id: "right"}
        :param evaluate_deaths: If True, remove any snakes that died as a result of the simulated move

        :return: A Battlesnake instance incorporating the simulated moves in a new game state
        """
        you_dict = self.you.as_dict()

        # Loop through all snakes and simulate a move if provided
        all_snakes: list[dict] = []
        for snake_id, snake in self.all_snakes.items():
            snake_dict = snake.as_dict()  # TODO add this into the Snake class?
            if snake_id in move_dict:
                # Update the head, body, and health of the snake to reflect the simulated move
                new_head = snake.head.moved_to(move_dict[snake_id])
                # Skip the snake if it died
                valid_move, _ = self.board.is_pos_safe(new_head, snake_id,
                                                       turn="ours" if not evaluate_deaths else "opponents")
                new_head_dict = new_head.as_dict()
                if valid_move:
                    snake_dict["health"] = snake.health - 1
                    snake_dict["body"] = [new_head_dict] + snake.body_dict[:-1]
                    snake_dict["head"] = new_head_dict
                    snake_dict["food_eaten"] = new_head_dict if new_head in self.board.food else None
                    all_snakes.append(snake_dict)
                # Repeat for our snake's specific attributes
                if snake_id == self.you.id:
                    you_dict["health"] = self.you.health - 1
                    you_dict["body"] = [new_head_dict] + self.you.body_dict[:-1]
                    you_dict["head"] = new_head_dict
                    you_dict["food_eaten"] = new_head_dict if new_head in self.board.food else None
            else:
                # Add the snake without any changes
                all_snakes.append(snake_dict)

        board = {
            "height": self.board.height,
            "width": self.board.width,
            "food": [xy.as_dict() for xy in self.board.food],
            "hazards": [xy.as_dict() for xy in self.board.hazards],
            "snakes": all_snakes
        }

        # Check if any snakes died via head-to-head collisions and remove them from the game
        if evaluate_deaths:
            # First update snake lengths from any food eaten
            for snake_num, snake_dict in enumerate(all_snakes):
                if snake_dict["food_eaten"] is not None:
                    all_snakes[snake_num]["length"] += 1
                    all_snakes[snake_num]["health"] = 100
                    all_snakes[snake_num]["body"] += [all_snakes[snake_num]["body"][-1]]
                    board["food"] = [food for food in board["food"]  # Remove the food from the board
                                     if not (food["x"] == snake_dict["food_eaten"]["x"]
                                             and food["y"] == snake_dict["food_eaten"]["y"])]
                    if snake_dict["id"] == self.you.id:
                        you_dict["length"] += 1
                        you_dict["body"] += [you_dict["body"][-1]]
                        you_dict["health"] = 100
                    # Reset the food tracker
                    all_snakes[snake_num]["food_eaten"] = None

            # Did any snakes die from head-to-head collisions?
            all_heads = [(snake["head"]["x"], snake["head"]["y"]) for snake in all_snakes]
            count_heads = Counter(all_heads)
            butt_heads = [k for k, v in count_heads.items() if v > 1]  # Any square where > 1 heads collided
            rm_snake_indices = []
            for butt_head in butt_heads:
                overlapping_snakes = np.array([  # Array of (id, length) for colliding snakes
                    (snake["id"], snake["length"]) for snake in all_snakes
                    if (snake["head"]["x"] == butt_head[0] and snake["head"]["y"] == butt_head[1])
                ])
                lengths = overlapping_snakes[:, 1].astype(int)
                # If our snake died, don't remove it just yet
                if not (self.you.id in overlapping_snakes[:, 0]):
                    indices_largest_snakes = np.argwhere(lengths == lengths.max()).flatten().tolist()
                    if len(indices_largest_snakes) > 1:  # No winner if the snakes are the same length
                        winner_id = None
                    else:
                        winner_id = overlapping_snakes[:, 0][indices_largest_snakes[0]]
                    # Remove any dead snakes
                    for rm_id in overlapping_snakes[:, 0]:
                        if rm_id != winner_id:  # Grab the snake index to remove later
                            rm_snake_indices.extend([i for i in range(len(all_snakes)) if all_snakes[i]["id"] == rm_id])

            for i in sorted(rm_snake_indices, reverse=True):
                del all_snakes[i]

        new_game = Battlesnake({"turn": self.turn, "board": board, "you": you_dict}, debugging=self.debugging)
        new_game.og_snakes = self.og_snakes
        new_game.og_length = self.og_length
        return new_game

    def edge_kill_detection(self, snake_id, us_killing: Optional[bool] = False) -> bool:
        """
        Determine if a snake is in a position where it can get edge-killed. Assumes that trap_detection ran first.

        :param snake_id: The ID of the desired snake we want to detect a possible edge kill for
        :param us_killing: For cases where an opponent snake is inputted, and we want to see if we can edge-kill them

        :return: True if the snake can get edge-killed, False otherwise
        """
        # Establish who the snake is and who the possible killers are
        snake = self.all_snakes[snake_id]
        opponents = [self.you] if us_killing else [opp for opp in self.all_snakes.values() if snake.id != opp.id]
        possible_moves = self.get_obvious_moves(snake.id, risk_averse=True)
        direction = snake.facing_direction()

        # A small database that covers different edge kill scenarios
        dir_dict = {
            "vertical": {
                "bounds": [0, self.board.width],  # Dimensions of the board
                "escape_dirs": ["left", "right"],  # We're getting edge-killed if we can't move in either direction
                "axis": "x",  # The axis used to scan for edge kills (e.g. we should look left/right in the x-direction)
                "axis_dir": "y",  # The axis we're moving along (e.g. vertical movement means going along the y-axis)
                "scan_dir": +1 if direction == "up" else -1  # +1 if we're moving in the positive x-direction, else -1
            },
            "horizontal": {
                "bounds": [0, self.board.height],
                "escape_dirs": ["down", "up"],
                "axis": "y",
                "axis_dir": "x",
                "scan_dir": +1 if direction == "right" else -1
            },
        }
        # Select the appropriate edge kill variables based on our snake's direction
        dir_data = dir_dict["horizontal"] if direction in ["left", "right"] else dir_dict["vertical"]
        bounds = dir_data["bounds"]
        escape_dirs = dir_data["escape_dirs"]
        ax = dir_data["axis"]
        ax_dir = dir_data["axis_dir"]
        scan_dir = dir_data["scan_dir"]

        # Determine if we can possibly get edge-killed via a longer snake in front of us, behind us, or two over from us
        board = self.board.board
        trapped_sides = [False, False]
        if len(set(escape_dirs).intersection(possible_moves)) == 0:
            # Scan the column/row to each side of us in ascending order
            for num, escape_dir in enumerate(escape_dirs):
                look = -1 if num == 0 else +1
                esc_move = getattr(snake.head, ax) + look
                # Off-limits if it's outside the board
                if bounds[0] <= esc_move < bounds[1]:
                    # Check the space in the column/row ahead of us
                    if ax == "x":
                        strip = board[esc_move, getattr(snake.head, ax_dir):] if scan_dir == +1 \
                            else board[esc_move, :(getattr(snake.head, ax_dir) + 1)][::-1]
                    else:
                        strip = board[getattr(snake.head, ax_dir):, esc_move] if scan_dir == +1 \
                            else board[:(getattr(snake.head, ax_dir) + 1), esc_move][::-1]
                    # If there's an opponent head in front of us, we might be getting edge-killed
                    if "H" in strip:
                        # Focus on the portion preceded by an opponent head
                        danger_strip = strip[:np.where(strip == "H")[0][0]]
                        # Identify the killer
                        if ax == "x":
                            opp_loc = Pos({"x": esc_move,
                                           "y": getattr(snake.head.moved_to(direction, len(danger_strip)), ax_dir)})
                        else:
                            opp_loc = Pos({"x": getattr(snake.head.moved_to(direction, len(danger_strip)), ax_dir),
                                           "y": esc_move})
                        opp_killer = self.board.identify_snake(opp_loc)

                        # Check if the opponent is bound to turn around and collide with us (not an edge kill)
                        opp_next_dirs = self.get_obvious_moves(opp_killer.id, risk_averse=False)
                        if len(opp_next_dirs) == 1 and sorted([opp_next_dirs[0], escape_dir]) == sorted(escape_dirs):
                            pass
                        # Check if the opponent is going the same direction as us (it's not an edge kill yet if not)
                        elif opp_killer.facing_direction() == direction:
                            # Check if there are gaps ahead of us before the killer, we're dead if there's none
                            if np.count_nonzero(danger_strip == " ") == 0:
                                trapped_sides[num] = True
                                break
                    else:
                        # If there's no opponent head, just check to see if there's free space for us to escape to
                        if np.count_nonzero(strip == " ") == 0 and self.trapped:
                            trapped_sides[num] = True
                            break

                    # Check the space directly behind and to the side of us
                    if ax == "x":
                        threat_behind = Pos({"x": esc_move, "y": getattr(snake.head, ax_dir) - 1}) if scan_dir == +1 \
                            else Pos({"x": esc_move, "y": getattr(snake.head, ax_dir) + 1})
                    else:
                        threat_behind = Pos({"x": getattr(snake.head, ax_dir) - 1, "y": esc_move}) if scan_dir == +1 \
                            else Pos({"x": getattr(snake.head, ax_dir) + 1, "y": esc_move})
                    # Also check if there's a snake two columns/rows over from us
                    esc_move_x2 = snake.head.as_dict()[ax] + (look * 2)
                    if ax == "x":
                        threat_two_over = Pos({"x": esc_move_x2, "y": getattr(snake.head, ax_dir)})
                    else:
                        threat_two_over = Pos({"x": getattr(snake.head, ax_dir), "y": esc_move_x2})
                    # If there's a longer snake in either of those two locations, we might be getting edge-killed
                    opp_killers = [opp.id for opp in opponents if opp.length > snake.length and (
                                   (opp.head == threat_behind and direction in self.get_obvious_moves(opp.id)) or
                                   (opp.head == threat_two_over))]
                    if len(opp_killers) > 0:
                        trapped_sides[num] = True
                else:
                    trapped_sides[num] = True

        # If both sides of the snake are blocked in, then we're trapped
        return True if sum(trapped_sides) == 2 else False

    def trap_detection(self) -> bool:
        """
        Determines if our snake is trapped based on the space it has left and possible escape routes

        :return: True if our snake's trapped, False otherwise
        """
        trapped = False
        # E.g. if we have 5 remaining squares to go to, determine if our space changed if all tails were set back by 5
        collision_square = None
        if self.board.space_all <= 15:
            # Check if we're trapped along with another snake
            if len(self.board.touch_opps) > 0:
                dist_to_trapped_opp, path_to_trapped_opp = self.board.dijkstra_shortest_path(
                    self.you.head, self.board.touch_opps[0], get_path=True)
                trapped_opp = self.board.identify_snake(self.board.touch_opps[0])
                # We'll win the incoming collision if we're longer and colliding on the same square
                trapped = not (dist_to_trapped_opp % 2 == 1 and self.you.length > trapped_opp.length)
                collision_square = path_to_trapped_opp[len(path_to_trapped_opp) // 2] if trapped else None
            else:
                trapped = True

        # If space frees up after X moves, identify where the opening in our flood fill is
        openings_in_boundary = []
        moves_until_opening = None
        for move_num in range(1, round(self.board.space_all) + 1):
            found_opening = False
            # Simulate each snake's new position if its tail were moved forward by one
            for snake in self.all_snakes.values():
                new_tail = snake.body[max(-snake.length + 1, -move_num)]
                # Until we detect a hole in our flood fill boundary
                if new_tail in self.board.ff_bounds:
                    openings_in_boundary.append(new_tail)
                    found_opening = True
            # We found an opening! Keep track of how many moves it took to appear
            if found_opening:
                moves_until_opening = move_num
                break
        # We're not actually trapped if we can reach the opening in our flood fill before space runs out!
        if len(openings_in_boundary) > 0:
            # If there are multiple openings, select the one closest to our snake
            if len(openings_in_boundary) > 1:
                openings_in_boundary = sorted(openings_in_boundary, key=lambda op: self.you.head.manhattan_dist(op))
            # Find the longest path to reach the opening (in case we're running out of space and need to stall)
            opening = openings_in_boundary[0]
            longest_path_till_opening = self.board.longest_path(self.you.head, opening)
            # If there's another trapped snake approaching us, see if we can reach the opening before a collision
            if collision_square is not None:
                if (self.board.shortest_dist(self.you.head, opening) <
                        self.board.shortest_dist(self.you.head, Pos({"x": collision_square[0], "y": collision_square[1]}))):
                    trapped = True
            else:
                trapped = longest_path_till_opening < moves_until_opening

        return trapped

    def heuristic(self, tree_depth: Optional[int] = 4) -> tuple[float, dict]:
        """
        Evaluate the current board for our snake (the higher the heuristic, the better)

        :param tree_depth: The current depth our snake is at in the minimax search tree

        :return:
            The computed heuristic value
            A dictionary of select metrics to be used for debugging
        """
        # How many layers deep in the game tree are we? (Reward longevity)
        current_depth = self.minimax_search_depth - tree_depth
        current_depth_weight = 25

        # Did any opponent snakes die or increase in length?
        tot_opp_length = sum([opp.length for opp in self.opponents.values()])
        tot_opp_length_weight = 1000

        # How much space do we have?
        space_ra, space_all, ff_bounds, touch_opps = self.board.flood_fill(self.you.id, full_package=True)
        space_ra_weight = 1

        # Determine the closest safe distance to food
        dist_food, best_food = self.board.closest_dist_to_food(self.you.id)
        if best_food is not None:
            logging.info(f"Closest distance to food = {dist_food, best_food.as_dict()}")
        # Determine how important food is
        opp_lengths = [opp.length for opp in self.opponents.values()]
        longest_flag = False
        if self.you.health < 40:  # Low health alert
            food_weight = 250
        elif self.you.length <= max(opp_lengths):  # If we're not the longest snake
            food_weight = 200
        elif self.you.length > max(opp_lengths):  # If we're the longest snake
            food_weight = 25
            longest_flag = True
        elif dist_food <= 3:  # Guarantee eating food the closer we are to it
            food_weight = 300 / dist_food
        else:
            food_weight = 50

        # How much space do we have in our peripheral?
        periph_ra, periph_all, periph_bounds, _ = self.board.flood_fill(self.you.id, confined_area="auto", full_package=True)
        periph_all_weight = 2

        # Size of our peripheral
        periph_penalty = 0
        next_moves = self.get_obvious_moves(snake_id=self.you.id, risk_averse=True)
        necessary_moves = self.you.head.direction_to(Pos({"x": self.board.width // 2, "y": self.board.height // 2}))
        xs, ys, _ = self.you.peripheral_vision("auto", dist=3, width=self.board.width, height=self.board.height)
        if (periph_all <= self.board.width // 2 and not (dist_food < 2 or self.og_length < self.you.length) and
                sum([n in necessary_moves for n in next_moves]) == 0):
            if xs[1] - xs[0] <= self.board.width // 3 or ys[1] - ys[0] <= self.board.height // 3:
                periph_penalty = -100

        # How cramped on space are we?
        space_penalty = 0
        if space_all <= 3:
            space_penalty = -1500
        elif space_ra <= 3:
            space_penalty = -250

        # Are we trapped? (With no incoming opponents trapped with us)
        if space_all <= 15:
            self.trapped = self.trap_detection()
            # Penalise entrapment (-1e7) more than getting killed by an opponent (-1e6)
            space_penalty = -1e7 if self.trapped and len(touch_opps) == 0 else space_penalty
        else:
            self.trapped = False

        # Are we in danger of getting edge-killed?
        edge_killed = self.edge_kill_detection(self.you.id)
        space_penalty = -1e7 if edge_killed else space_penalty



        # # Are we cornering ourselves?
        # next_moves = self.get_obvious_moves(snake_id=self.you.id, risk_averse=True)
        # next_moves_with_three_edges = []
        # for next_move in next_moves:
        #     with_three_edges = False
        #     for i in range(1, 3):
        #         node_ahead = self.you.head.moved_to(next_move, distance=i)
        #         node_ahead_edges = len(self.board.graph.edges(node_ahead.as_tuple())) - 1
        #         if node_ahead_edges == 3:
        #             with_three_edges = True
        #             break
        #     next_moves_with_three_edges.append(with_three_edges)
        # if sum(next_moves_with_three_edges) == 0:
        #     corner_penalty = -500

        aggression_okay = self.you.length >= 6  # TODO BROKE EVERYTHING

        # We want to minimise available space for our opponents via flood fill (but only when there are fewer snakes in
        # our vicinity)
        dist_from_enemies = sorted(
            [self.board.shortest_dist(self.you.head, opp.head) for opp in self.opponents.values()])
        djikstra_flag = sum([dist <= 3 for dist in dist_from_enemies]) >= 1
        dist_from_enemies_manhattan = sorted(
            [self.you.head.manhattan_dist(opp.head) for opp in self.opponents.values()])
        manhattan_flag = sum([dist <= 5 for dist in dist_from_enemies_manhattan]) >= 1
        if len(self.opponents) <= 3 or djikstra_flag or manhattan_flag:
            self.peripheral_size = 4
            if djikstra_flag:
                closest_enemy = sorted(self.opponents.keys(), key=lambda opp_id: self.board.shortest_dist(self.you.head,
                                                                                                         self.opponents[
                                                                                                             opp_id].head))[
                    0]
            else:
                closest_enemy = sorted(self.opponents.keys(), key=lambda opp_id: self.you.head.manhattan_dist(self.opponents[
                                                                                                             opp_id].head))[
                    0]

            if len(move := self.get_obvious_moves(self.all_snakes[closest_enemy].id)) == 1:
                confined_area = move[0]
            else:
                confined_area = "auto"

            decide_risk = True if self.you.length > self.all_snakes[closest_enemy].length else False

            # enemy_space_ra, enemy_space_all, _, _ = self.board.flood_fill(closest_enemy, full_package=True)
            available_enemy_space = self.board.flood_fill(closest_enemy, risk_averse=True, confined_area=confined_area)
            available_enemy_space_ra = self.board.flood_fill(closest_enemy, risk_averse=True)
            available_enemy_space_all = self.board.flood_fill(closest_enemy, risk_averse=False)

            if periph_ra > available_enemy_space or space_all > available_enemy_space_all:
                if available_enemy_space_ra <= 5:
                    kill_bonus = 2000

                elif available_enemy_space < 4:
                    kill_bonus = 1000
                elif available_enemy_space_ra <= 15 and space_ra > available_enemy_space_ra + 2:  # Yay but only if we're not gonna be doo-doo
                    kill_bonus = 750
                    space_penalty = 0  # restore our space advantage hehe
                elif available_enemy_space < self.opponents[closest_enemy].length / 2.75:  # Used to be 4
                    kill_bonus = 500
                else:
                    kill_bonus = 0
            else:
                kill_bonus = 0
            if kill_bonus > 0:
                if kill_bonus != 2000:  # When it's not guaranteed yet
                    # Reward getting closer, but only if it doesn't trap us
                    kill_bonus += (1000 / self.board.shortest_dist(self.you.head, self.all_snakes[closest_enemy].head) if not self.trapped else 0)
                else:  # Guaranteed
                    space_penalty = space_penalty / 2
                # Reward if the opponent is getting least space
                kill_bonus += (1000 / max(1, available_enemy_space_ra) if not self.trapped else 0)

        else:
            available_enemy_space = -2
            kill_bonus = 0

        # Did we kill any opponents previously?  # TODO NOT ROBUST ENOUGH
        if len(self.og_snakes) > len(self.all_snakes):
            dead_snakes = set(self.og_snakes.keys()) - set(self.all_snakes)
            likely_kill = [self.you.head.manhattan_dist(self.og_snakes[opp_id].head) <= 3 for opp_id in dead_snakes]
            kill_bonus += sum([kill * 10000 for kill in likely_kill])

        # Get closer to enemy snakes if we're longer
        if 2 >= len(self.opponents) == sum([self.you.length >= s.length + 1 for s in self.opponents.values()]):
            dist_from_enemies = sorted(
                [self.board.shortest_dist(self.you.head, opp.head) for opp in self.opponents.values()])
            dist_to_enemy = dist_from_enemies[0]
        else:
            dist_to_enemy = 0
        if dist_to_enemy > 0 and len(self.opponents) == 1:
            aggression_weight = 1500
        elif dist_to_enemy > 0:
            aggression_weight = 250
        else:
            aggression_weight = 0

        # If we're getting too close to enemy snakes that are longer, RETREAT
        threats = [self.board.shortest_dist(self.you.head, opp.head) for opp in self.opponents.values() if
                   opp.length > self.you.length and opp.head.within_bounds(
                       self.you.peripheral_vision(return_pos_only=True))]
        num_threats = (np.count_nonzero(np.array(threats) <= 2) * 2
                       + np.count_nonzero(np.array(threats) == 3) * 1)


        # Are we in the centre of the board? Maximise control
        centre = range(self.board.width // 2 - 2, self.board.width // 2 + 3)
        in_centre = self.you.head.x in centre and self.you.head.y in centre and (
                len(self.opponents) <= 2 or num_threats == 0) and best_food is None
        # Are we on the edge? Try to stay away if possible
        on_edge = self.you.head.x in [0, self.board.width - 1] or self.you.head.y in [0, self.board.height - 1]

        collision_inbound = False
        me = self.get_obvious_moves(snake_id=self.you.id)
        closest_enemy = sorted(self.opponents.keys(), key=lambda opp_id: self.board.shortest_dist(self.you.head,
                                                                                                 self.opponents[
                                                                                                     opp_id].head))[0]
        them = self.get_obvious_moves(snake_id=closest_enemy)
        diff_lengths = self.all_snakes[closest_enemy].length - self.you.length
        if diff_lengths > 0:
            connection = self.all_snakes[closest_enemy].head.direction_to(self.you.head)
            # This means they're headed towards us
            if self.all_snakes[closest_enemy].facing_direction() in connection:
                # If we have no choice but to head towards the opponent as well  (e.g. if the enemy is heading up and left, we have no choice but to move down or right)
                if sum([esc in me for esc in connection]) == 0:
                    collision_inbound = True
        if collision_inbound:
            danger_penalty = -15 * diff_lengths - 15/self.you.head.manhattan_dist(self.all_snakes[closest_enemy].head)
        else:
            danger_penalty = 0

        # Can we cut off our opponents?
        closest_opp = sorted(self.opponents.values(),
                             key=lambda opp: self.board.shortest_dist(self.you.head, opp.head))[0]

        # TODO corner edge case
        cutoff_bonus = 0
        if kill_bonus >= 2000:
            cutoff_bonus = kill_bonus
        elif (self.you.head.within_bounds(closest_opp.peripheral_vision(return_pos_only=True)) and
                not closest_opp.head.within_bounds(
                    self.you.peripheral_vision(direction=self.you.facing_direction(), return_pos_only=True)) and
                (on_edge or (not on_edge and self.you.facing_direction() in me))):  # continue to cutoff, unless we're on the edge for an edge kill?
            cutting_off = self.board.flood_fill(closest_opp.id, opp_cutoff=self.you.id)
            if cutting_off <= 15:
                cutoff_bonus = 2500
            elif cutting_off <= self.board.width * self.board.height / 6:
                cutoff_bonus = 1000
            elif cutting_off <= self.board.width * self.board.height / 4:
                cutoff_bonus = 250
            else:
                cutoff_bonus = 0

            if cutoff_bonus > 0:
                cutoff_bonus += (cutoff_bonus / (1 + cutting_off))

        # Can we get cut off?
        if len(self.opponents) == 1:
            us_cutoff = self.board.flood_fill(closest_opp.id, opp_cutoff=self.you.id)
            opp_cutoff = self.board.flood_fill(self.you.id, opp_cutoff=closest_opp.id)
            if self.you.length < closest_opp.length:
                if opp_cutoff < 15:
                    if space_penalty == 0:
                        space_penalty = -500
            else:
                if opp_cutoff <= 15 and us_cutoff > opp_cutoff:  # Penalise if we're in a worse position
                    if space_penalty == 0:
                        space_penalty = -500
                    if cutoff_bonus > 0:  # Reduce the cutoff if we're the ones getting cut off lol
                        cutoff_bonus = 0

        length_weight = 1250
        # if space_penalty < 0:
        #     length_weight = 100

        # Heuristic formula
        enemy_restriction_weight = 0 if available_enemy_space == -2 else 75 if len(self.opponents) > 2 else 200
        if self.trapped or edge_killed:
            enemy_restriction_weight = 0

        if kill_bonus > 0:
            food_weight = 10
            periph_all_weight = 0.5
        # Get more aggressive if we're longer and there's only one snake left!
        if len(self.opponents) == 1 and longest_flag:
            periph_all_weight = 0.5

        centre_control_weight = 20 if not (self.trapped or edge_killed) else 0
        threat_proximity_weight = -25

        if len(threats) == 0 and kill_bonus == 0 and cutoff_bonus == 0:
            if not longest_flag:  # We're chilling tbh but need FOOD
                food_weight = 350
            else:  # compete for food
                opp_dist_food, opp_best_food = self.board.closest_dist_to_food(closest_enemy, risk_averse=False)
                if len(self.opponents) == 1 and best_food is not None and opp_best_food is not None:
                    if opp_best_food == best_food and opp_dist_food <= dist_food + 2:
                        food_weight = 250


        logging.info(f"Available space: {space_ra}")
        logging.info(f"Space penalty: {space_penalty}")
        logging.info(f"Available peripheral: {periph_all} {periph_penalty}")
        logging.info(f"Enemy length total: {tot_opp_length}")
        logging.info(f"Threats within 3 squares of us: {num_threats}")
        logging.info(f"Incoming collision penalty: {danger_penalty}")
        logging.info(f"Distance to nearest enemy: {dist_to_enemy}")
        logging.info(f"Actual dist: {self.board.shortest_dist(self.you.head, self.all_snakes[closest_enemy].head)  }")
        logging.info(f"Distance to nearest food: {dist_food}")
        logging.info(f"Layers deep in search tree: {current_depth}")
        logging.info(f"Available enemy space: {available_enemy_space}")
        logging.info(f"Cutoff bonus: {cutoff_bonus}")
        logging.info(f"Kill bonus: {kill_bonus}")
        logging.info(f"In centre: {in_centre}; On edge: {on_edge}")
        logging.info(f"Length: {self.you.length}")

        h = (space_ra * space_ra_weight) + space_penalty + \
            (periph_all_weight * periph_all) + periph_penalty + \
            (tot_opp_length_weight / (tot_opp_length + 1)) + \
            (threat_proximity_weight * num_threats) + danger_penalty + \
            (food_weight / (dist_food + 1)) + \
            (current_depth * current_depth_weight) + \
            (self.you.length * length_weight) + \
            in_centre * centre_control_weight + \
            on_edge * -centre_control_weight + \
            aggression_weight / (dist_to_enemy + 1) + cutoff_bonus + \
            (enemy_restriction_weight / (available_enemy_space + 1)) + kill_bonus

        return h, {"Score": round(h, 2),
                   "Space | Pen": f"{space_ra} | {space_penalty} => {(space_ra * space_ra_weight) + space_penalty}",
                   "Centre | Edge": f"{in_centre * centre_control_weight} | {on_edge * -centre_control_weight}",
                   "Periph | Pen": f"{periph_all} | {periph_penalty} => {periph_all_weight * periph_all + periph_penalty}",
                   "Food | Opp Dist": f"{dist_food} {dist_to_enemy} | => {round(food_weight / (dist_food + 1), 2)} | {round((aggression_weight / (dist_to_enemy + 1)), 2)}",
                   "Opp Space | Len": f"{available_enemy_space} | {tot_opp_length} => {round((enemy_restriction_weight / (available_enemy_space + 1)), 2)} | {round(tot_opp_length_weight / (tot_opp_length + 1), 2)}",
                   "Danger | Kill | Cutoff": f"{danger_penalty} | {kill_bonus} | {cutoff_bonus}",
                   "Threats": f"{num_threats} => {(threat_proximity_weight * num_threats) + danger_penalty}",
                   "Length": f"{self.you.length} => {(self.you.length * length_weight)}"}

    def minimax(self, depth: int, alpha: float, beta: float, maximising_snake: bool) -> tuple[float, Any, dict]:
        """
        Implement the minimax algorithm with alpha-beta pruning!

        :param depth: The current depth in the minimax search tree
        :param alpha: The best value for our maximising snake (us)
        :param beta: The best value for our minimising snakes (opponents)
        :param maximising_snake: If True, it's our snake's turn and the minimax algorithm wants to maximise the score.
            If False, it's the opponents' turn and the algorithm wants to minimise the score.

        :return:
            The best heuristic score for the node
            The best move associated with the best heuristic for the node
            A dictionary compiling select metrics to construct an informative tree visualisation for debugging
        """
        # If we're not at the bottom of the search tree, check if our snake died
        if depth != self.minimax_search_depth:
            game_over, alive = self.is_game_over(depth=depth)
            if not alive:
                logging.info("Our snake died...")
                # Check if we got killed by an enemy snake
                possible_killers = [opp for opp in self.opponents.values() if opp.head == self.you.head]
                killer_penalty = 0
                if len(possible_killers) > 0:
                    killer = sorted(possible_killers, key=lambda op: op.length, reverse=True)[0]
                    # We'd prefer to get killed by a smaller snake in case we're the same length and can kill them too
                    killer_length = killer.length
                    # How likely is the killer going to deliver the coup de grâce? E.g. he could get distracted by food
                    distraction = self.board.closest_dist_to_food(killer.id)[0]
                    # If we got immediately killed, then it's much worse than an edge kill down the line
                    immediately_killed = -1e8 if depth >= self.minimax_search_depth - 2 else 0
                    # Add a killer penalty score to give higher weight to more advantageous deaths
                    killer_penalty = immediately_killed - killer_length + (distraction if distraction <= 4 else 0)
                # Big idea: reward slower deaths, penalise immediate death, account for dumb opponents not killing
                heuristic = -1e6 + (self.minimax_search_depth - depth) + killer_penalty
                return heuristic, None, {"Score": heuristic}
            # If our snake is the winner :)
            elif game_over:
                logging.info("Our snake won!!")
                heuristic = 1e6 + depth  # Reward faster kills
                return heuristic, None, {"Score": heuristic}

        # If we're at the bottom of the decision tree
        if depth == 0:
            logging.info("=" * 75)
            logging.info(f"DEPTH = {depth}")
            score, score_metrics = self.heuristic(tree_depth=depth)
            logging.info(f"Heuristic = {score} at terminal node")
            return score, None, score_metrics

        if maximising_snake:  # Our turn
            logging.info("=" * 75)
            logging.info(f"DEPTH = {depth} OUR SNAKE")
            logging.info(f"alpha = {alpha} | beta = {beta}")

            clock_in = time.time_ns()
            # Determine our snake's possible moves, sorted by the amount of immediate space it'd give us
            possible_moves = self.get_obvious_moves(self.you.id, risk_averse=self.you.length <= 5,
                                                    sort_by_peripheral=True)
            # In the early stages of the game, if we're out of risk-averse moves, accept risk
            if len(possible_moves) == 0 and self.you.length <= 5:
                possible_moves = self.get_obvious_moves(self.you.id, risk_averse=False, sort_by_peripheral=True)
            if len(possible_moves) == 0:  # RIP we're going to die
                possible_moves = ["down"]
            logging.info(f"Our possible moves: {possible_moves}")

            # Initialise variables to store information on the best detected move
            best_score, best_move, best_node_data, best_edge = -np.inf, None, None, None
            # Each child node will be a new board simulating a possible move
            for num, move in enumerate(possible_moves):
                simulation = self.simulate_move({self.you.id: move})
                logging.info(f"Visiting {num + 1} of {len(possible_moves)} child nodes: {move}")
                if self.debugging:
                    logging.info(simulation.board.display(show=False))
                    logging.info(simulation.dict)

                # Add the move to the minimax tree plot as a node and create an edge to its parent node
                node_added = self.update_tree_graphic(add_nodes=True, depth=depth - 1, node_data=move)
                edge_added = self.update_tree_graphic(add_edges=True, depth=depth - 1)
                # Run minimax on the new simulated board
                clock_in2 = time.time_ns()
                node_score, node_move, node_data = simulation.minimax(depth - 1, alpha, beta, False)
                # Update the node we just added with text to display some heuristic information for debugging
                self.update_tree_graphic(add_nodes=True, depth=depth - 1, node_data=node_data, insert_at=node_added)

                logging.info("=" * 75)
                logging.info(f"Back at DEPTH = {depth} OUR SNAKE")
                logging.info(f"alpha = {alpha} | beta = {beta}")

                # If we found a better score with a different move, update the best move and best edge
                if np.argmax([best_score, node_score]) == 1:
                    best_move, best_node_data, best_edge = move, node_data, edge_added
                best_score = max(best_score, node_score)
                old_alpha, alpha = alpha, max(alpha, best_score)
                logging.info(f"Updated alpha from {old_alpha} to {alpha}")
                logging.info(f"Identified best move so far = {best_move} in "
                             f"{round((time.time_ns() - clock_in2) / 1000000, 3)} ms")

                # Check to see if we can prune the branch
                if alpha >= beta:
                    logging.info(f"PRUNED!!! alpha = {alpha} >= beta = {beta}")
                    break

            self.update_tree_graphic(update_best_edge=best_edge)
            logging.info(f"Finished minimax layer on our snake in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
            return best_score, best_move, best_node_data

        else:  # Opponents' turn
            logging.info("=" * 75)
            logging.info(f"DEPTH = {depth} OPPONENT SNAKES")
            logging.info(f"alpha = {alpha} | beta = {beta}")

            # Simulate full set of opponent moves only if they're within a certain distance of our snake
            if len(self.opponents) == 1:
                focus_within = self.board.width * self.board.height
            elif len(self.opponents) <= 3:
                focus_within = self.board.width
            else:
                focus_within = self.board.width // 2

            opps_moves: dict[str, list] = {}  # Store possible moves for each opponent by their snake ID
            opps_scores: list[tuple[str, float]] = []  # Estimate the quality of the move with a simple heuristic
            for opp_num, (opp_id, opp_snake) in enumerate(self.opponents.items()):
                opp_moves = self.get_obvious_moves(opp_id, risk_averse=False)
                if len(opp_moves) == 0:  # If the opponent has no legal moves, move down and die
                    opp_moves = ["down"]
                # Assume our opponents are smart - for each possible move, compute how beneficial it'd be for them
                # Opponent heuristic => favours proximity to our snake, more space, longer length, and penalises death
                opp_scores = []
                for move in opp_moves:
                    moved_head = opp_snake.head.moved_to(move)
                    dist_from_us = self.board.shortest_dist(self.you.head, moved_head)
                    opp_space = self.board.flood_fill(opp_id, risk_averse=False, confined_area=move)
                    opp_dist_to_food = min([1e6] + [moved_head.manhattan_dist(food) for food in self.board.food])
                    our_dist_to_food, _ = self.board.closest_dist_to_food(self.you.id, risk_averse=False)
                    opp_aggression = (opp_snake.length > self.you.length and
                                      (moved_head.manhattan_dist(self.you.head) <= self.board.width // 2 or
                                      opp_dist_to_food * 3 < our_dist_to_food))
                    opp_food = 0 if opp_dist_to_food >= 3 or opp_aggression \
                        else -2 if opp_dist_to_food == 2 else -5
                    opp_penalty = 100 if dist_from_us == 1 and opp_snake.length <= self.you.length else 0
                    opp_scores.append(
                        (opp_id,
                         dist_from_us + opp_food + opp_penalty + ((1 / opp_space) if opp_space >= 1 else 0))
                    )
                    # print(f"Dist: {dist_from_us}, Food: {opp_food}, Space: {round(((1 / opp_space) if opp_space >= 1 else 0), 2)}, Pen: {opp_penalty})")
                # Sort the opponent moveset by the computed heuristics
                opp_moves = [x for _, x in sorted(zip([s[1] for s in opp_scores], opp_moves))]
                opp_scores = sorted(opp_scores, key=lambda sc: sc[1])
                # Save time by cutting down the opponent's possible moves to 1 if they're too far to be a threat
                if self.you.head.manhattan_dist(opp_snake.head) > focus_within:
                    cut_opp_moves = [opp_moves[0]]
                    cut_opp_scores = [opp_scores[0]]
                else:
                    cut_opp_moves = None
                    cut_opp_scores = None
                if cut_opp_moves is not None:
                    opps_moves[opp_id] = cut_opp_moves
                    opps_scores.extend(cut_opp_scores)
                    logging.info(f"Snake {opp_num + 1} possible moves: {opp_moves} -> "                
                                 f"{[round(score[1], 2) for score in opp_scores[-len(opp_moves):]]} "
                                 f"but cut to {cut_opp_moves}")
                else:
                    opps_moves[opp_id] = opp_moves
                    opps_scores.extend(opp_scores)
                    logging.info(f"Snake {opp_num + 1} possible moves: {opp_moves} -> "
                                 f"{[round(score[1], 2) for score in opp_scores[-len(opp_moves):]]}")

            # Now that we have ranked moves for each opponent, we need to create move combinations in order of how
            # threatening they are. The idea is to centre movesets around the "worst" move that ANY opponent can make
            # and fill in moves for the rest of the opponents in order of how bad they are
            threat_opps = sorted(opps_scores, key=lambda combo: combo[1])  # Sort all opponent moves by their heuristic
            worst_opp_tracker = {}  # Keep track of which opponent moves we've finished building move combos around
            sim_move_combos = []  # Append simulations for final move combinations (each one is a child node)
            sim_movesets = []  # For each simulation, keep track of the move combination, so we don't repeat any
            num_sims = 3  # The maximum number of move combinations
            clock_in = time.time_ns()
            for worst_threat in threat_opps:
                # Stop simulating movesets after a cutoff
                if len(sim_move_combos) >= num_sims:
                    break

                worst_opp_id = worst_threat[0]
                if worst_opp_id not in worst_opp_tracker.keys():
                    worst_opp_tracker[worst_opp_id] = []
                # Start the move combo with the most threatening move possible for any opponent
                move_combo = {
                    worst_opp_id: [move for move in opps_moves[worst_opp_id] if not (
                            move in worst_opp_tracker[worst_opp_id] and len(opps_moves[worst_opp_id]) > 1)][0]
                }
                worst_opp_tracker[worst_opp_id].append(opps_moves[worst_opp_id][0])
                # Fill in the rest of the moveset with the most threatening move for each opponent
                for rest_opp_id in self.opponents.keys():
                    if rest_opp_id != worst_opp_id:
                        move_combo[rest_opp_id] = opps_moves[rest_opp_id][0]
                # Avoid adding the same move combination
                if move_combo in sim_movesets:
                    continue
                # Now simulate a board with the newly created opponent moveset combo!
                simulation = self.simulate_move(move_combo, evaluate_deaths=True)
                sim_move_combos.append(simulation)
                sim_movesets.append(move_combo)

            # Rewrite the move combinations into a user-friendly form for debugging
            if self.debugging:
                by_number = []
                for move_combo in sim_movesets:
                    by_number.append([f"{num + 1}: {move_combo[opp]}" for num, opp in enumerate(self.opponents.keys())])
                sim_movesets = by_number

            logging.info(f"Simulated {len(sim_move_combos)} possible move combos in "
                         f"{round((time.time_ns() - clock_in) / 1000000, 3)} ms")

            clock_in = time.time_ns()
            best_score, best_move, best_node_data, best_edge = np.inf, None, None, None
            # Each child node will be a new board simulating a possible opponent move combination
            for num, simulation in enumerate(sim_move_combos):
                logging.info(f"Visiting {num + 1} of {len(sim_move_combos)} child nodes: {sim_movesets[num]}")
                if self.debugging:
                    logging.info(simulation.board.display(show=False))
                    logging.info(simulation.dict)

                    # Add the move to the minimax tree plot as a node and create an edge to its parent node
                node_added = self.update_tree_graphic(add_nodes=True, depth=depth - 1, node_data=sim_movesets[num])
                edge_added = self.update_tree_graphic(add_edges=True, depth=depth - 1)
                # Run minimax on the new simulated board
                clock_in2 = time.time_ns()
                node_score, node_move, node_data = simulation.minimax(depth - 1, alpha, beta, True)
                # Update the node we just added with text to display some heuristic information for debugging
                self.update_tree_graphic(add_nodes=True, depth=depth - 1, node_data=node_data, insert_at=node_added)

                logging.info("=" * 75)
                logging.info(f"BACK AT DEPTH = {depth} OPPONENT SNAKES")
                logging.info(f"alpha = {alpha} | beta = {beta}")

                # If we found a better score with a different move, update the best move and best edge
                if np.argmin([best_score, node_score]) == 1:
                    best_move, best_node_data, best_edge  = sim_movesets[num], node_data, edge_added
                best_score = min(best_score, node_score)
                old_beta, beta = beta, min(beta, best_score)
                logging.info(f"Updated beta from {old_beta} to {beta}")
                logging.info(f"Identified best move so far = {best_move} in "
                             f"{round((time.time_ns() - clock_in2) / 1000000, 3)} ms")

                # Check to see if we can prune the branch
                if beta <= alpha:
                    logging.info(f"PRUNED!!! alpha = {alpha} >= beta = {beta}")
                    break

            self.update_tree_graphic(update_best_edge=best_edge)
            logging.info(f"Finished minimax layer on opponents in {(time.time_ns() - clock_in) // 1000000} ms")
            return best_score, best_move, best_node_data

    def optimal_move(self) -> str:
        """Main function to identify the most optimal move for our snake"""
        if self.turn <= 3:
            depth = 3
        else:
            depth = self.minimax_search_depth

        logging.info("STARTING POSITION")
        logging.info(self.board.display(show=False))

        tree_tracker[depth].append(0)  # Add our initial node
        _, best_move, _ = self.minimax(depth=depth, alpha=-np.inf, beta=np.inf, maximising_snake=True)

        # Output a visualisation of the minimax decision tree for debugging
        self.update_tree_graphic(create_plot=True)
        return best_move

    def update_tree_graphic(
            self,
            add_nodes: Optional[bool] = False,
            add_edges: Optional[bool] = False,
            depth: Optional[int] = None,
            node_data: Optional[Any] = None,
            insert_at: Optional[int] = None,
            update_best_edge: Optional[int] = None,
            create_plot: Optional[bool] = False,
    ):
        """
        Utility function that constructs a minimax tree visualisation for debugging purposes. Makes use of 4 global
        variables to gather nodes and edges in a structured, organised manner while we traverse the minimax search tree.

        :param add_nodes: If True, add a new node at the "tree_node_counter" position and update the "tree_tracker"
        :param add_edges: If True, add an edge between the current "tree_node_counter" node and a child node
        :param depth: Keeps track of what depth to add a node or edge
        :param node_data: Used with add_nodes=True. Holds the heuristic metrics to add
        :param insert_at: Used with add_nodes=True. Insert node heuristic metrics at a certain node index
        :param update_best_edge: Feeds in an index to the "tree_edge" variable. Outline the best edge for a node in red
        :param create_plot: If True, create the final visualisation and save it as a PNG
        """
        if not self.debugging:
            return None

        global tree_tracker
        global tree_node_counter
        global tree_nodes
        global tree_edges

        if add_nodes:
            if insert_at is not None:  # Do we have to update any node with heuristic metrics?
                node_move = tree_nodes[insert_at][1]
                formatted_dict = str(node_data).replace(", ", "\n").replace("{", "").replace(
                    "}", "").replace("'", "")
                tree_nodes[insert_at] = (tree_tracker[depth][-1], node_move + "\n" + formatted_dict)
                return
            else:
                tree_tracker[depth].append(tree_node_counter)  # Add the node to our tree dictionary at the right depth
                tree_nodes.append((tree_tracker[depth][-1], str(node_data)))
                return len(tree_nodes) - 1

        if add_edges:
            # Tuple of (node_1, node_2, node_attributes) where the edge is created between node_1 and node_2
            tree_edges.append((tree_tracker[depth + 1][-1], tree_tracker[depth][-1], {"colour": "k", "width": 1}))
            tree_node_counter += 1  # Now we're on the next node
            return len(tree_edges) - 1  # Keep track of where we added the edge

        if update_best_edge is not None:
            tree_edges[update_best_edge][2]["colour"] = "r"
            tree_edges[update_best_edge][2]["width"] = 5

        if create_plot:
            G = nx.Graph()
            G.add_node(0)
            node_labels = {0: ""}
            for node in tree_nodes:
                G.add_node(node[0])
                node_labels[node[0]] = node[1]
            G.add_edges_from(tree_edges)
            pos = hierarchy_pos(G, 0)
            edge_colours = [G[u][v]["colour"] for u, v in G.edges()]
            edge_widths = [G[u][v]["width"] for u, v in G.edges()]
            # Plot the minimax diagram as a hierarchical tree
            plt.figure(figsize=(100, 25))
            nx.draw(G, pos=pos, node_color=["white"] * G.number_of_nodes(), edge_color=edge_colours, width=edge_widths,
                    labels=node_labels, with_labels=True, node_size=40000, font_size=20)
            plt.savefig("minimax_tree.png", bbox_inches="tight", pad_inches=0)
