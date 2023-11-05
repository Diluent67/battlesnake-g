from __future__ import annotations
import itertools
import logging
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from collections import Counter
from networkx_tree import hierarchy_pos
from typing import Optional
from Board import Board
from Pos import Pos
from Snake import Snake

my_name = "Nightwing"
# Use these global variables to add data for visualising the minimax decision tree
tree_tracker = {6: [], 5: [], 4: [], 3: [], 2: [], 1: [], 0: []}
tree_edges = []
tree_nodes = []
tree_node_counter = 1


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

        :return: A list of possible moves for the given snake
        """
        # Loop through possible moves and remove from consideration if it's invalid
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
                                        key=lambda move2: self.board.closest_dist(head2, head.moved_to(move2)))
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

    def is_game_over(self, for_snake_id: str | list, depth: Optional[int] = None) -> tuple[bool, bool]:
        """
        Determine if the game ended for certain snakes or not. Mostly used to know whether our snake died, but can
        optionally be used to determine any number of opponent snakes' statuses.

        :param for_snake_id: The ID of the desired snake we want to know died or not
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
            # Check if each snake's head is in a safe square, depending on if we're at a depth where only we made a move
            is_safe, _ = self.board.is_pos_safe(snake.head, snake_id, turn="done" if depth % 2 == 0 else "ours")
            snake_monitor[snake_id] = is_safe

        # Game is over if there's only one snake remaining or if our snake died
        game_over = True if (sum(snake_monitor.values()) == 1 or not snake_monitor[self.you.id]) else False
        # See if a specific snake is alive or not
        if isinstance(for_snake_id, list):
            snake_still_alive = [snake_monitor[snake_id] for snake_id in for_snake_id]
        else:
            snake_still_alive = snake_monitor[for_snake_id]

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
            snake_dict = snake.as_dict()
            if snake_id in move_dict:
                # Update the head, body, and health of the snake to reflect the simulated move
                new_head = snake.head.moved_to(move_dict[snake_id])
                # Skip the snake if it died
                valid_move, _ = self.board.is_pos_safe(new_head, snake_id,
                                                       turn="ours" if not evaluate_deaths else "opponents")
                new_head = new_head.as_dict()
                if valid_move:
                    snake_dict["health"] = snake.health - 1
                    snake_dict["body"] = [new_head] + snake.body_dict[:-1]
                    snake_dict["head"] = new_head
                    snake_dict["food_eaten"] = new_head if Pos(new_head) in self.board.food else None
                    all_snakes.append(snake_dict)
                # Repeat for our snake's specific attributes
                if snake_id == self.you.id:
                    you_dict["health"] = self.you.health - 1
                    you_dict["body"] = [new_head] + self.you.body_dict[:-1]
                    you_dict["head"] = new_head
                    you_dict["food_eaten"] = new_head if Pos(new_head) in self.board.food else None
            else:
                # Add the snake without any changes
                all_snakes.append(snake_dict)

        board = {
            "height": self.board.height,
            "width": self.board.width,
            "food": [xy.as_dict() for xy in self.board.food],
            "hazards": self.board.hazards.copy(),
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
        return new_game

    def edge_kill_detection(self, snake_id, us_killing: Optional[bool] = False) -> bool:
        """
        Determine if a snake is in a position where it can get edge-killed

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
                "bounds": [0, self.board.width],
                "escape_dirs": ["left", "right"],
                "axis": "x",
                "axis_dir": "y",
                "scan_dir": +1 if direction == "up" else -1
            },
            "horizontal": {
                "bounds": [0, self.board.height],
                "escape_dirs": ["down", "up"],
                "axis": "y",
                "axis_dir": "x",
                "scan_dir": +1 if direction == "right" else -1
            },
        }
        dir_data = dir_dict["horizontal"] if direction in ["left", "right"] else dir_dict["vertical"]
        bounds = dir_data["bounds"]
        escape_dirs = dir_data["escape_dirs"]
        ax = dir_data["axis"]
        ax_dir = dir_data["axis_dir"]
        scan_dir = dir_data["scan_dir"]

        # Determine if we can't escape (e.g. we're heading right, but can't move up or down)
        board = self.board.board
        trapped_sides = [False, False]
        if len(set(escape_dirs).intersection(possible_moves)) == 0:
            # Scan the column/row to each side of us in ascending order
            for num, escape_dir in enumerate(escape_dirs):
                look = -1 if num == 0 else +1
                esc_attempt = getattr(snake.head, ax) + look
                # Off-limits if it's outside the board
                if bounds[0] <= esc_attempt < bounds[1]:
                    # Look at the space in the column/row ahead of us
                    strip = board[esc_attempt, getattr(snake.head, ax_dir):] if scan_dir == +1 \
                        else board[esc_attempt, :(getattr(snake.head, ax_dir) + 1)][::-1]
                    # If there's an opponent head in front of us, we might be getting edge-killed
                    if "H" in strip:
                        # Focus on the portion preceded by an opponent head to determine if we're being edge-killed
                        danger_strip = strip[:np.where(strip == "H")[0][0]]
                        # Identify the possible killer
                        opp_loc = Pos(esc_attempt, getattr(snake.head.moved_to(direction, len(danger_strip)), ax_dir))
                        opp_killer = self.board.identify_snake(opp_loc)
                        # Check if the opponent is bound to turn around and collide with us
                        opp_next_dirs = self.get_obvious_moves(opp_killer.id, risk_averse=False)
                        if len(opp_next_dirs) == 1 and sorted([opp_next_dirs[0], escape_dir]) == sorted(escape_dirs):
                            pass
                        # Check if the opponent is going the same direction as us - it's not an edge kill yet if not
                        elif opp_killer.facing_direction() == direction:
                            # Check if there's free space ahead of us before the killer, we're trapped if there's none
                            if np.count_nonzero(danger_strip == " ") == 0:
                                trapped_sides[num] = True
                    else:
                        # If there's no opponent head, just check to see if there's free space for us to escape to
                        if np.count_nonzero(strip == " ") == 0:
                            trapped_sides[num] = True

                    # Check if there's a snake two columns/rows over that can kill us
                    esc_attempt_x2 = snake.head.as_dict()[ax] + (look * 2)
                    future_threat_pos = Pos(esc_attempt_x2, getattr(snake.head, ax_dir))
                    future_threat_opp = [opp_snake.id for opp_snake in opponents if opp_snake.head == future_threat_pos]
                    if len(future_threat_opp) > 0:
                        threat_id = future_threat_opp[0]
                        if (self.all_snakes[threat_id].length >= snake.length and
                                direction in self.get_obvious_moves(threat_id)):
                            trapped_sides[num] = True
                else:
                    trapped_sides[num] = True
        # If both sides of the snake are blocked in, then we're trapped
        return True if sum(trapped_sides) == 2 else False

    def trap_detection(self, available_space):
        """
        Determines if our snake is trapped based on the space it has left and possible escape routes

        :param available_space: Our snake's flood fill (risk_averse=False)

        :return: True if our snake's trapped, False otherwise
        """
        trapped = False
        # If we have 5 remaining squares to go to, determine if our space changed if all snakes' tails were removed by 5
        space_left, opps = self.board.flood_fill(self.you.id, return_touching_opps=True)
        collision_square = None
        if space_left <= 15:
            # Situations where we're trapped along with another snake
            if len(opps) > 0:
                dist_to_trapped_opp, path_to_trapped_opp = self.board.dijkstra_shortest_dist(self.you.head, opps[0], get_path=True)
                trapped_opp = self.board.identify_snake(opps[0])
                # We'll win the incoming collision if we're longer and colliding on the same square
                trapped = not (dist_to_trapped_opp % 2 == 1 and self.you.length > trapped_opp.length)
                collision_square = path_to_trapped_opp[len(path_to_trapped_opp) // 2] if trapped else None
            else:
                trapped = True

        # If space frees up after X moves, identify where the opening in our flood fill is
        _, boundaries = self.board.flood_fill(self.you.id, return_boundaries=True)
        openings_in_boundary = []
        for move_num in range(1, round(available_space)):
            found_opening = False
            # Move all snakes' tails forward by one until we detect a hole in our flood fill boundary
            for snake in self.all_snakes.values():
                new_tail = snake.body[max(-snake.length + 1, -move_num)]
                if new_tail in boundaries:
                    openings_in_boundary.append(new_tail)
                    found_opening = True
            # We found an opening! Keep track of how many moves it took to appear
            if found_opening:
                moves_until_opening = move_num
                break

        if len(openings_in_boundary) > 0:
            # If there are multiple openings, select the one closest to our snake
            if len(openings_in_boundary) > 1:
                openings_in_boundary = sorted(openings_in_boundary, key=lambda op: self.you.head.manhattan_dist(op))

            opening = openings_in_boundary[0]
            longest_path_till_opening = self.board.stall_path(self.you.head, opening)
            # We need to make sure we reach the opening before we run out of space
            if collision_square is None:
                trapped = longest_path_till_opening < moves_until_opening
            else:
                if self.board.closest_dist(self.you.head, opening) < self.board.closest_dist(self.you.head, Pos(collision_square)):
                    trapped = True

        return trapped

    def heuristic(self, depth_number: int) -> tuple[float, dict]:
        """
        Evaluate the current board for our snake (the higher the heuristic, the better)

        :param depth_number: The current depth our snake is at in the minimax search tree

        :return:
            The computed heuristic value
            A dictionary of select metrics to be used for debugging
        """
        # Determine how many layers deep in the game tree we are
        layers_deep = self.minimax_search_depth - depth_number

        # If an opponent snake dies :)
        opponents_left = sum([opp.length for opp in self.opponents.values()])

        # Determine available space via flood fill
        available_space = self.board.flood_fill(self.you.id, risk_averse=True)
        available_space_ra, boundaries = self.board.flood_fill(self.you.id, risk_averse=False, return_boundaries=True)
        if available_space_ra < 4:
            space_penalty = -500
        elif available_space < 4:
            space_penalty = -250
        else:
            space_penalty = 0

        # Are we trapped?
        if available_space_ra <= 15:
            trapped = self.trap_detection(available_space)
            _, opps = self.board.flood_fill(self.you.id, return_touching_opps=True)
            space_penalty = -1e7 if trapped and len(opps) == 0 else 0  # Penalise entrapment more than getting killed by an opponent

        # Are we in danger of getting edge-killed?
        edge_killed = self.edge_kill_detection(self.you.id)
        space_penalty = -1e7 if edge_killed else space_penalty

        # Estimate the space we have in our peripheral vision
        available_peripheral = self.board.flood_fill(self.you.id, confined_area="auto")

        # We want to minimise available space for our opponents via flood fill (but only when there are fewer snakes in
        # our vicinity)
        dist_from_enemies = sorted(
            [self.board.closest_dist(self.you.head, opp.head) for opp in self.opponents.values()])
        if len(self.opponents) <= 3 or sum([dist <= 3 for dist in dist_from_enemies]) >= 1:
            # and sum([dist < (self.board.width // 2) for dist in self.dist_from_enemies()]) <= 3 \
            # and len(self.opponents) == sum([self.you.length > s["length"] for s in self.opponents.values()]):
            self.peripheral_size = 4
            closest_enemy = sorted(self.opponents.keys(), key=lambda opp_id: self.board.closest_dist(self.you.head,
                                                                                                     self.opponents[
                                                                                                         opp_id].head))[
                0]
            if len(move := self.get_obvious_moves(self.all_snakes[closest_enemy].id)) == 1:
                confined_area = move[0]
            else:
                confined_area = "auto"

            decide_risk = True if self.you.length > self.all_snakes[closest_enemy].length else False
            available_enemy_space = self.board.flood_fill(closest_enemy, risk_averse=True, confined_area=confined_area)
            available_enemy_space_full = self.board.flood_fill(closest_enemy, risk_averse=True)

            available_me_space = self.board.flood_fill(self.you.id, risk_averse=True, confined_area=confined_area)
            if available_me_space > available_enemy_space:
                if available_enemy_space_full <= 5:
                    kill_bonus = 2000
                elif available_enemy_space < 4:
                    kill_bonus = 1000
                elif available_enemy_space < self.opponents[closest_enemy].length / 2.75:  # Used to be 4
                    kill_bonus = 500
                else:
                    kill_bonus = 0
            else:
                kill_bonus = 0
            if kill_bonus > 0:
                # Reward getting closer
                kill_bonus += 1000 / self.board.closest_dist(self.you.head, self.all_snakes[closest_enemy].head)
        else:
            available_enemy_space = -2
            kill_bonus = 0



        # Get closer to enemy snakes if we're longer
        if 2 >= len(self.opponents) == sum([self.you.length >= s.length + 1 for s in self.opponents.values()]):
            dist_from_enemies = sorted(
                [self.board.dijkstra_shortest_dist(self.you.head, opp.head) for opp in self.opponents.values()])
            dist_to_enemy = dist_from_enemies[0]
        else:
            dist_to_enemy = 0
        if dist_to_enemy > 0 and len(self.opponents) == 1:
            aggression_weight = 1000
        elif dist_to_enemy > 0:
            aggression_weight = 250
        else:
            aggression_weight = 0

        # If we're getting too close to enemy snakes that are longer, RETREAT
        threats = [self.board.dijkstra_shortest_dist(self.you.head, opp.head) for opp in self.opponents.values() if
                   opp.length > self.you.length and opp.head.within_bounds(
                       self.you.peripheral_vision(return_pos_only=True))]
        num_threats = (np.count_nonzero(np.array(threats) <= 2) * 2
                       + np.count_nonzero(np.array(threats) == 3) * 1)

        collision_inbound = False
        me = self.get_obvious_moves(snake_id=self.you.id)
        closest_enemy = sorted(self.opponents.keys(), key=lambda opp_id: self.board.closest_dist(self.you.head,
                                                                                                 self.opponents[
                                                                                                     opp_id].head))[0]
        them = self.get_obvious_moves(snake_id=closest_enemy)
        diff_lengths = self.all_snakes[closest_enemy].length - self.you.length
        if diff_lengths > 0:
            connection = self.all_snakes[closest_enemy].head.direction_to(self.you.head)
            # This means they're headed towards us
            if self.all_snakes[closest_enemy].facing_direction() in connection:
                if sum([esc in me for esc in connection]) != len(connection):
                    collision_inbound = True
        if collision_inbound:
            danger_penalty = -15 * diff_lengths
        else:
            danger_penalty = 0

        # Can we cut off our opponents?
        closest_opp = sorted(self.opponents.values(),
                             key=lambda opp: self.board.closest_dist(self.you.head, opp.head))[0]
        if self.you.head.within_bounds(closest_opp.peripheral_vision(return_pos_only=True)) and \
                not closest_opp.head.within_bounds(
                    self.you.peripheral_vision(direction=self.you.facing_direction(), return_pos_only=True)) and \
                self.you.facing_direction() in me:
            cutting_off = self.board.flood_fill(closest_opp.id, cutoff=self.you.id)
            if cutting_off <= 15:
                cutoff_bonus = 2500
            elif cutting_off <= self.board.width * self.board.height / 6:
                cutoff_bonus = 1000
            elif cutting_off <= self.board.width * self.board.height / 4:
                cutoff_bonus = 250
            else:
                cutoff_bonus = 0
        else:
            cutoff_bonus = 0

        # Determine the closest safe distance to food
        dist_food, best_food = self.board.dist_to_nearest_food(self.you.id)
        if best_food is not None:
            logging.info(f"Closest distance to food = {dist_food, best_food.as_dict()}")
        health_flag = True if self.you.health < 40 else False
        shortest_flag = True if sum([self.you.length <= snake.length for snake in self.opponents.values()]) >= min(
            [2, len(self.opponents)]) else False
        longest_flag = True if sum([self.you.length > snake.length for snake in self.opponents.values()]) == len(
            self.opponents) else False

        # Are we in the centre of the board? Maximise control
        centre = range(self.board.width // 2 - 2, self.board.width // 2 + 3)
        in_centre = (self.you.head.as_dict()["x"] in centre and self.you.head.as_dict()["x"] in centre) and (
                len(self.opponents) <= 2)

        # Heuristic formula
        depth_weight = 25
        enemy_left_weight = 1000

        space_weight = 1
        peripheral_weight = 2
        enemy_restriction_weight = 0 if available_enemy_space == -2 else 75 if len(self.opponents) > 2 else 200
        food_weight = 250 if health_flag else 200 if shortest_flag else 25 if longest_flag else 50

        length_weight = 300
        centre_control_weight = 10
        threat_proximity_weight = -25

        logging.info(f"Available space: {available_space}")
        logging.info(f"Space penalty: {space_penalty}")
        logging.info(f"Available peripheral: {available_peripheral}")
        logging.info(f"Enemy length total: {opponents_left}")
        logging.info(f"Threats within 3 squares of us: {num_threats}")
        logging.info(f"Incoming collision penalty: {danger_penalty}")
        logging.info(f"Distance to nearest enemy: {dist_to_enemy}")
        logging.info(f"Distance to nearest food: {dist_food}")
        logging.info(f"Layers deep in search tree: {layers_deep}")
        logging.info(f"Available enemy space: {available_enemy_space}")
        logging.info(f"Cutoff bonus: {cutoff_bonus}")
        logging.info(f"Kill bonus: {kill_bonus}")
        logging.info(f"In centre: {in_centre}")
        logging.info(f"Length: {self.you.length}")

        h = (available_space * space_weight) + space_penalty + \
            (peripheral_weight * available_peripheral) + \
            (enemy_left_weight / (opponents_left + 1)) + \
            (threat_proximity_weight * num_threats) + danger_penalty + \
            (food_weight / (dist_food + 1)) + \
            (layers_deep * depth_weight) + \
            (self.you.length * length_weight) + \
            in_centre * centre_control_weight + \
            aggression_weight / (dist_to_enemy + 1) + cutoff_bonus + \
            (enemy_restriction_weight / (available_enemy_space + 1)) + kill_bonus

        return h, {"Heur": round(h, 2),
                   "Space": available_space,
                   "Penalty": space_penalty,
                   "Periph": available_peripheral,
                   "Food Dist": dist_food,
                   "Enemy Dist": dist_to_enemy,
                   "Enemy Kill": available_enemy_space + kill_bonus,
                   "Threats": num_threats,
                   "Length": self.you.length}

    def minimax(self, depth, alpha, beta, maximising_snake):
        """
        Implement the minimax algorithm with alpha-beta pruning

        :param depth:
        :param alpha:
        :param beta:
        :param maximising_snake:

        :return:
        """
        if depth != self.minimax_search_depth:
            # Check if our snake died
            game_over, still_alive = self.is_game_over(for_snake_id=self.you.id, depth=depth)
            if not still_alive:
                logging.info("Our snake died...")
                killer_snake = sorted([opp for opp in self.opponents.values() if opp.head == self.you.head], key=lambda op: op.length)
                killer_penalty = killer_snake[0].length if len(killer_snake) > 0 else 0
                # How likely is the killer going to deliver the coup de grâce? E.g. if he'd rather get food
                likelihood_kill = self.board.dist_to_nearest_food(killer_snake[0].id)[0] if len(killer_snake) > 0 else 0
                distraction = likelihood_kill if likelihood_kill <= 4 else 0
                heuristic = -1e6 + (self.minimax_search_depth - depth) - killer_penalty + distraction * 2  # Reward slower deaths and penalise worse killers
                return heuristic, None, {"Heur": heuristic}
            # Otherwise, if our snake is ALIVE and is the winner :)
            elif game_over:
                logging.info("OUR SNAKE WON")
                heuristic = 1e6 + depth  # Reward faster kills
                return heuristic, None, heuristic

        # At the bottom of the decision tree or if we won/lost the game
        if depth == 0:
            logging.info("=" * 50)
            logging.info(f"DEPTH = {depth}")
            heuristic, heuristic_data = self.heuristic(depth_number=depth)
            logging.info(f"Heuristic = {heuristic} at terminal node")
            return heuristic, None, heuristic_data

        global tree_edges
        # Minimax on our snake
        if maximising_snake:
            logging.info("=" * 50)
            logging.info(f"DEPTH = {depth} OUR SNAKE")
            logging.info(f"alpha = {alpha} | beta = {beta}")

            clock_in = time.time_ns()
            possible_moves = self.get_obvious_moves(  # If > 6 opponents, we'll do depth = 2 and risk_averse = True
                self.you.id, risk_averse=(len(self.opponents) > 6), sort_by_peripheral=True)
            if len(possible_moves) == 0 and len(self.opponents) > 6:  # Try again, but do any risky move
                possible_moves = self.get_obvious_moves(self.you.id, risk_averse=False, sort_by_peripheral=True)
            if len(possible_moves) == 0:  # RIP
                possible_moves = ["down"]
            logging.info(f"Possible moves: {possible_moves}")

            best_val, best_move = -np.inf, None
            best_node_data, best_edge = None, None
            for num, move in enumerate(possible_moves):
                SIMULATED_BOARD_INSTANCE = self.simulate_move({self.you.id: move})

                logging.info(f"Visiting {num + 1} of {len(possible_moves)} child nodes: {move}")
                if self.debugging:
                    logging.info(SIMULATED_BOARD_INSTANCE.board.__str__())
                    logging.info(SIMULATED_BOARD_INSTANCE.dict)

                clock_in2 = time.time_ns()
                edge_added = self.update_tree_visualisation(add_edges=True, depth=depth - 1)
                node_added = self.update_tree_visualisation(add_nodes=True, depth=depth - 1, node_data=move)
                node_val, node_move, node_data = SIMULATED_BOARD_INSTANCE.minimax(depth - 1, alpha, beta, False)
                self.update_tree_visualisation(add_nodes=True, depth=depth - 1, node_data=node_data,
                                               insert_index=node_added)

                logging.info("=" * 50)
                logging.info(f"BACK AT DEPTH = {depth} OUR SNAKE")
                logging.info(f"alpha = {alpha} | beta = {beta}")

                # Update best score and best move
                if np.argmax([best_val, node_val]) == 1:
                    best_move = move
                    best_node_data, best_edge = node_data, edge_added
                best_val = max(best_val, node_val)
                old_alpha = alpha
                alpha = max(alpha, best_val)

                logging.info(f"Updated ALPHA from {old_alpha} to {alpha}")
                logging.info(
                    f"Identified best move so far = {best_move} in {round((time.time_ns() - clock_in2) / 1000000, 3)} ms")

                # Check to see if we can prune
                if alpha >= beta:
                    logging.info(f"PRUNED!!! Alpha = {alpha} >= Beta = {beta}")
                    break

            tree_edges[best_edge][2]["colour"] = "r"
            tree_edges[best_edge][2]["width"] = 4
            logging.info(f"FINISHED MINIMAX LAYER on our snake in {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
            return best_val, best_move, best_node_data

        # Minimax on opponent snakes
        else:
            logging.info("=" * 50)
            logging.info(f"DEPTH = {depth} OPPONENT SNAKES")
            logging.info(f"alpha = {alpha} | beta = {beta}")

            # Choose to simulate full set of opponent moves only if they're within a certain distance of our snake
            if len(self.opponents) == 1:
                search_within = self.board.width * self.board.height
            elif len(self.opponents) == 2:
                search_within = self.board.width
            else:
                search_within = self.board.width // 2

            # Store possible moves for each snake id
            opps_moves = {}
            opps_scores = []
            for opp_num, (opp_id, opp_snake) in enumerate(self.opponents.items()):
                opp_moves = self.get_obvious_moves(opp_id, risk_averse=False, sort_by_dist_to=self.you.id)
                # If the snake has no legal moves, move down and die
                if len(opp_moves) == 0:
                    opp_moves = ["down"]
                # Save time by only using full opponent move sets if they're within a certain range
                dist_to_opp = self.you.head.manhattan_dist(opp_snake.head)
                if dist_to_opp <= search_within:
                    # opps_moves[opp_id] = opp_moves
                    # For each possible move, estimate how close that brings the opponent to our snake
                    opp_scores = [
                        (opp_id,
                         self.board.closest_dist(self.you.head, opp_snake.head.moved_to(move)) +
                         (1 / (opp_snake.length + (1 if opp_snake.head.moved_to(move) in self.board.food else 0))) +
                         ((1 / self.board.flood_fill(opp_id, confined_area=move)) if self.board.flood_fill(opp_id, confined_area=move) >= 1 else 0)
                         ) for move in opp_moves]
                    opps_scores.extend(opp_scores)
                    opp_moves = [x for _, x in sorted(zip([s[1] for s in opp_scores], opp_moves))]
                    opps_moves[opp_id] = opp_moves
                    logging.info(f"Snake {opp_num + 1} possible moves: {opp_moves} -> "
                                 f"{[round(score[1], 2) for score in opps_scores[-len(opp_moves):]]}")
                else:
                    opps_moves[opp_id] = [opp_moves[0]]
                    opps_scores.extend([
                        (opp_id,
                         self.board.closest_dist(self.you.head, opp_snake.head.moved_to(move)) +
                         (1 / (opp_snake.length + (1 if opp_snake.head.moved_to(move) in self.board.food else 0))) +
                         ((1 / self.board.flood_fill(opp_id, confined_area=move)) if self.board.flood_fill(opp_id, confined_area=move) >= 1 else 0)
                         ) for move in opp_moves])
                    logging.info(f"Snake {opp_num + 1} possible moves: {opp_moves} but cut down to {opp_moves[0]} ->"
                                 f"{[round(score[1], 2) for score in opps_scores[-len(opp_moves):]]}")

            # A list of tuples, with each tuple storing (opp_id, threat_score)
            threat_opps = sorted(opps_scores, key=lambda combo: combo[1])
            # Aggregate a list of move dictionaries for each snake
            # Each board will pivot around one snake's move, with the other opponents filling in with their best moves
            sim_move_combos = []
            opp_focus_tracker = {}
            num_sims = 3
            for worst_combo in threat_opps:
                worst_move_combos = {}
                worst_opp = worst_combo[0]  # The snake ID of the perpetrator
                if worst_opp not in opp_focus_tracker.keys():
                    opp_focus_tracker[worst_opp] = []
                worst_move_combos[worst_opp] = [move for move in opps_moves[worst_opp]
                                                if not (len(opps_moves[worst_opp]) > 1 and move in opp_focus_tracker[worst_opp])][0]

                opp_focus_tracker[worst_opp].append(opps_moves[worst_opp][0])

                # Select the most threatening move for the rest of the opponent snakes
                for rest_opp in self.opponents.keys():
                    if rest_opp != worst_opp:
                        worst_move_combos[rest_opp] = opps_moves[rest_opp][0]

                # Avoid accidentally adding the same move combination
                if worst_move_combos not in sim_move_combos:
                    sim_move_combos.append(worst_move_combos)

                # Stop simulating movesets after a cutoff value
                if len(sim_move_combos) >= num_sims:
                    break

            # # Sort opponents by proximity to our snake, and then applying sorting to opponent movesets
            # sorted_by_dists = sorted(self.opponents.keys(),
            #                          key=lambda opp_id2: self.board.closest_dist(
            #                              self.you.head, self.opponents[opp_id2].head))
            # opps_moves = dict(sorted(opps_moves.items(), key=lambda pair: sorted_by_dists.index(pair[0])))
            #
            clock_in = time.time_ns()
            # # If >= 3 board simulations, then randomly sample 3 of them based on how threatening the position is to our
            # # snake to cut down on runtime
            # all_opp_combos = list(itertools.product(*opps_moves.values()))
            # if len(all_opp_combos) > 2:
            #     logging.info(f"FOUND {len(all_opp_combos)} BOARDS BUT CUTTING DOWN TO 3")
            #     cutoff = 3
            # else:
            #     cutoff = 3
            #
            # if len(opps_moves) > 0 and len(all_opp_combos) > cutoff:
            #     covered_ids = [list(opps_moves.keys())[0]]
            #     all_opp_combos2 = []
            #     while len(all_opp_combos2) < cutoff:
            #         combo_counter = 1
            #         for s_id, s in opps_moves.items():
            #             if s_id not in covered_ids:
            #                 combo_counter = combo_counter * len(s)
            #         index_getter = np.arange(len(covered_ids) - 1, len(all_opp_combos), combo_counter)
            #         getter = [all_opp_combos[i] for i in index_getter]
            #         all_opp_combos2.extend(getter)
            #
            #     all_opp_combos = all_opp_combos2[:cutoff]

            possible_movesets = []
            possible_sims = []
            # Get all possible boards by simulating moves for each opponent snake, one at a time
            for move_combo in sim_move_combos:
                SIMULATED_BOARD_INSTANCE2 = self.simulate_move(move_combo, evaluate_deaths=True)
                possible_sims.append(SIMULATED_BOARD_INSTANCE2)
                possible_movesets.append(list(move_combo.values()))

            logging.info(f"Simulated {len(possible_sims)} possible move combos in "
                         f"{round((time.time_ns() - clock_in) / 1000000, 3)} ms")

            clock_in = time.time_ns()
            best_val, best_move = np.inf, None
            best_node_data, best_edge = None, None
            for num, SIMULATED_BOARD_INSTANCE in enumerate(possible_sims):
                logging.info(f"Visiting {num + 1} of {len(possible_sims)} child nodes: {possible_movesets[num]}")
                if self.debugging:
                    logging.info(SIMULATED_BOARD_INSTANCE.board.__str__())
                    logging.info(SIMULATED_BOARD_INSTANCE.dict)
                clock_in2 = time.time_ns()
                edge_added = self.update_tree_visualisation(add_edges=True, depth=depth - 1)
                node_added = self.update_tree_visualisation(add_nodes=True, depth=depth - 1,
                                                            node_data=str(possible_movesets[num]))
                node_val, node_move, node_data = SIMULATED_BOARD_INSTANCE.minimax(depth - 1, alpha, beta, True)
                self.update_tree_visualisation(add_nodes=True, depth=depth - 1, node_data=node_data,
                                               insert_index=node_added)

                logging.info("=" * 50)
                logging.info(f"BACK AT DEPTH = {depth} OPPONENT SNAKES")
                logging.info(f"alpha = {alpha} | beta = {beta}")

                # Update best score and best move
                if np.argmin([best_val, node_val]) == 1:
                    best_move = possible_movesets[num]
                    best_node_data, best_edge = node_data, edge_added
                best_val = min(best_val, node_val)
                old_beta = beta
                beta = min(beta, best_val)

                logging.info(f"Updated BETA from {old_beta} to {beta}")
                logging.info(
                    f"Identified best move so far = {best_move} in {round((time.time_ns() - clock_in2) / 1000000, 3)} ms")

                # Check to see if we can prune
                if beta <= alpha:
                    logging.info(f"PRUNED!!! Beta = {beta} <= Alpha = {alpha}")
                    break

            tree_edges[best_edge][2]["colour"] = "r"
            tree_edges[best_edge][2]["width"] = 4
            logging.info(f"FINISHED MINIMAX LAYER on opponents in {(time.time_ns() - clock_in) // 1000000} ms")
            return best_val, best_move, best_node_data

    def optimal_move(self):
        """Let's run the minimax algorithm with alpha-beta pruning!"""
        # Compute the best score of each move using the minimax algorithm with alpha-beta pruning
        if self.turn < 3:  # Our first 3 moves are super self-explanatory tbh
            search_depth = 4
        elif len(self.opponents) > 6:
            search_depth = 4  # TODO should be risk-averse
        elif len(self.opponents) >= 4:
            search_depth = 4
        else:
            search_depth = 4

        tree_tracker[search_depth].append(0)

        logging.info("STARTING POSITION")
        logging.info(self.board.__str__())
        _, best_move, _ = self.minimax(depth=search_depth, alpha=-np.inf, beta=np.inf, maximising_snake=True)

        # Output a visualisation of the minimax decision tree for debugging
        if self.debugging:
            import networkx as nx
            G = nx.Graph()
            node_labels = {}
            for node in tree_nodes:
                G.add_node(node[0])
                node_labels[node[0]] = node[1]
            G.add_node(0)
            node_labels[0] = ""
            G.add_edges_from(tree_edges)
            pos = hierarchy_pos(G, 0)
            edge_colours = [G[u][v]["colour"] for u, v in G.edges()]
            edge_widths = [G[u][v]["width"] for u, v in G.edges()]

            plt.figure(figsize=(50, 25))
            nx.draw(G, pos=pos, node_color=["white"] * G.number_of_nodes(), edge_color=edge_colours, width=edge_widths,
                    labels=node_labels, with_labels=True, node_size=40000, font_size=20)
            plt.savefig("minimax_tree.png", bbox_inches="tight", pad_inches=0)

        return best_move

    @staticmethod
    def update_tree_visualisation(depth, add_edges=False, add_nodes=False, node_data=None, insert_index=None):
        global tree_node_counter
        global tree_tracker
        if add_edges:
            # Add the node that we'll be creating the edge to
            tree_tracker[depth].append(tree_node_counter)
            # Tuple of (node_1, node_2, node_attributes) where the edge is created between node_1 and node_2
            global tree_edges
            tree_edges.append((tree_tracker[depth + 1][-1], tree_tracker[depth][-1], {"colour": "k", "width": 1}))
            # Now we're going to be on the next node
            tree_node_counter += 1
            return len(tree_edges) - 1

        if add_nodes:
            global tree_nodes
            if insert_index is not None:
                node_move = tree_nodes[insert_index][1]
                formatted_dict = str(node_data).replace(", ", "\n").replace("{", "").replace("}", "").replace("'", "")
                tree_nodes[insert_index] = (tree_tracker[depth][-1], node_move + "\n" + formatted_dict)
            else:
                tree_nodes.append((tree_tracker[depth][-1], str(node_data).replace("'", "")))
            return len(tree_nodes) - 1
