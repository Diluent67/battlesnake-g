from __future__ import annotations
import logging
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import time
from networkx_tree import hierarchy_pos
from typing import Any, Optional
from Board import Board
from Pos import Pos
from Snake import Snake

my_name = ["Nightwing", "#22aa34"]
# Use these global variables to add data for visualising the minimax decision tree
tree_tracker = {6: [], 5: [], 4: [], 3: [], 2: [], 1: [], 0: []}
tree_node_counter = 1
tree_edges = []
tree_nodes = []


class Battlesnake:
    def __init__(
            self,
            game_state: dict,
            debugging: Optional[bool] = False,
            og_length: Optional[bool] = None,
            kill_count: Optional[list] = None
    ):
        """
        Represents our Battlesnake game and includes all our decision-making methods

        :param game_state: The move API request (https://docs.battlesnake.com/api/example-move#move-api-response)
        :param debugging: Display a detailed log while traversing the minimax search tree
        """
        self.you = Snake(game_state["you"])
        # Weird edge case when running locally where the "you" snake is not our actual snake
        if self.you.name not in my_name:
            right_you = [snake_dict for snake_dict in game_state["board"]["snakes"] if snake_dict["name"] in my_name][0]
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
        # For opponent-only lookups
        self.opponents = self.all_snakes.copy()
        self.opponents.pop(self.you.id)

        # Populate our Battlesnake board
        self.board = Board(game_state["board"], all_snakes=self.all_snakes)

        # General game data
        self.turn = game_state["turn"]
        # Keep track of our original length and the number of snakes we've killed while traversing the search tree
        self.og_length = self.you.length if og_length is None else og_length
        self.kill_count = [] if kill_count is None else kill_count
        self.killer_intel = None  # Info on which snake we got killed by

        # Finish up our constructor
        self.dict = game_state
        self.minimax_search_depth = 4  # Depth for minimax algorithm
        self.peripheral_size = 3  # Length of our snake's "peripheral vision"
        self.debugging = debugging
        logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
        if not self.debugging:
            logging.disable(logging.INFO)

    def get_moveset(
            self,
            snake_id: str,
            risk_averse: Optional[bool] = True,
            turn: Optional[str] = None,
            sort_by_dist_to: Optional[str] = None,
            sort_by_periph: Optional[bool] = False,
            both_risk_options: Optional[bool] = False
    ) -> list | tuple[list, list]:
        """
        Return a list of valid moves for any hypothetical snake. The given moveset can omit risky moves that result in
            losing head-to-head collisions (risk_averse=True) or include them (risk_averse=False).

        :param snake_id: The ID of the desired snake we want to find moves for
        :param risk_averse: Avoid any chance of a death-inducing collision (we're assuming our opponents are out to get
            us, but only if they're longer). Set False to include these risky moves in our final moveset.
        :param turn: Either "ours", "opponents", "done", or "basic". Addresses nuances with running this function during
            the minimax algorithm or independently. Refer to the docstring in Board.is_pos_safe for more details.
        :param sort_by_dist_to: Input any snake ID here. This will return all possible moves, but sort the moves by the
            distance from this snake (after making the move) to the head of the snake whose ID was inputted. Very useful
            for discerning which moves are more threatening or bring us closer to a different snake.
        :param sort_by_periph: If True, sort the possible moves by the resulting amount of space in our "peripheral
            vision". Very useful for discerning which moves allow us more immediate space.
        :param both_risk_options: Option to return both the normal moveset and the risk-averse moveset

        :return: A (possibly) sorted list of candidate moves
        """
        head = self.all_snakes[snake_id].head
        # Loop through possible moves and remove from consideration if it's invalid + keep track of risky moves
        moveset = ["up", "down", "left", "right"]
        risky_moves = []
        if turn is None:
            turn = "ours" if snake_id == self.you.id else "opponents"
        for move in moveset.copy():
            is_safe, is_risky = self.board.is_pos_safe(head.moved_to(move), snake_id, turn=turn)
            if not is_safe:
                moveset.remove(move)
            elif is_risky:
                risky_moves.append(move)

        # Sort the possible moves if needed
        if len(moveset) > 1:
            if sort_by_dist_to is not None:
                head2 = self.all_snakes[sort_by_dist_to].head
                moveset = sorted(moveset, key=lambda m: self.board.shortest_dist(head2, head.moved_to(m)))
            if sort_by_periph:
                moveset = sorted(moveset, key=lambda m: self.board.flood_fill(snake_id, confine_to=m), reverse=True)

        # Generate a risk-averse moveset
        moveset_ra = moveset.copy()
        for risky_move in risky_moves:
            moveset_ra.remove(risky_move)
            # De-prioritise any risky moves from the normal moveset and send them to the back
            moveset.append(moveset.pop(moveset.index(risky_move)))

        if both_risk_options:
            return moveset_ra if len(moveset_ra) > 0 else moveset
        else:
            return moveset_ra if risk_averse else moveset

    def simulate_move(self, move_dict: dict, evaluate_deaths: Optional[bool] = False, depth: Optional[int] = 4) -> Battlesnake:
        """
        Create a new Battlesnake instance to simulate a game turn and make moves for a set of desired snakes. To improve
        speed, this function builds a new "game_state" dictionary from scratch to avoid affecting the original instance.

        :param move_dict: A dictionary containing candidate moves for a set of snake IDs, e.g. {self.you.id: "left",
            other_snake_id: "right"}
        :param evaluate_deaths: Option to remove any snakes that died as a result of the simulation

        :return: A fresh Battlesnake instance representing the simulated turn
        """
        you_dict = self.you.as_dict()
        # Loop through all snakes and simulate a move if provided
        all_snakes: list[dict] = []
        for snake_id, snake in self.all_snakes.items():
            if snake_id in move_dict:
                new_snake_dict = snake.make_move(move_dict[snake_id], food_list=self.board.food, return_dict=True)
                all_snakes.append(new_snake_dict)
                # Repeat for our snake's specific attributes
                if snake_id == self.you.id:
                    you_dict = new_snake_dict
            else:
                all_snakes.append(snake.as_dict())

        board = {
            "height": self.board.height,
            "width": self.board.width,
            "food": [xy.as_dict() for xy in self.board.food],
            "hazards": [xy.as_dict() for xy in self.board.hazards],
            "snakes": all_snakes
        }

        new_game = Battlesnake(
            game_state={"turn": self.turn, "board": board, "you": you_dict},
            debugging=self.debugging,
            og_length=self.og_length,
            kill_count=self.kill_count.copy()
        )

        # Check if any snakes died as a result of the simulation
        if evaluate_deaths:
            for snake_id, snake in new_game.all_snakes.items():
                valid_move, _ = new_game.board.is_pos_safe(snake.head, snake_id, turn="done")
                if not valid_move:  # TODO any snake that died can technically be a free space?
                    snake.dead = True
                    # Check if we got killed by an enemy snake and gather intel to compute a killer penalty score later
                    if snake_id == self.you.id:
                        possible_killers = [opp for opp in new_game.opponents.values() if opp.head == new_game.you.head]
                        if len(possible_killers) > 0:
                            killer = sorted(possible_killers, key=lambda op: op.length, reverse=True)[0]
                            distraction_score = new_game.board.closest_dist_to_food(killer.id)[0]
                            new_game.killer_intel = (killer.length, distraction_score)
                    # Keep track if our snake was the killer
                    if snake_id != self.you.id and snake.head.manhattan_dist(new_game.you.head) <= 2:
                        new_game.kill_count.append(depth)
                # Update snake length from any food eaten and remove the food from the board
                if (consumed_food := snake.food_eaten) is not None:
                    new_game.all_snakes[snake_id].ate_food()
                    new_game.board.food = [food for food in new_game.board.food if food != consumed_food]

            # Remove dead snakes from the game except for our own (since all Battlesnake games need a "you" field)
            rm_ids = [rm_id for rm_id, rm_snake in new_game.opponents.items() if rm_snake.dead]
            for rm_id in rm_ids:
                new_game.all_snakes.pop(rm_id, None)
                new_game.opponents.pop(rm_id, None)

        new_game.board.update_board()
        return new_game

    def trap_detection(self) -> tuple[bool, float | None]:
        """
        Determine if our snake is trapped based on its possible escape routes

        :return:
            True if our snake's trapped, False otherwise
            A heuristic to inform how dangerous our potential escape route would be
        """
        trapped = False
        esc_penalty = None

        # Check if we're trapped along with another snake
        collision_sq = None
        if len(self.board.touch_opps) > 0:
            dist_to_trapped_opp, path_to_trapped_opp = self.board.dijkstra_shortest_path(
                self.you.head, self.board.touch_opps[0], from_snake=self.you.id, get_path=True)
            trapped_opp = self.board.identify_snake(self.board.touch_opps[0])
            trapped_opp_moveset = self.get_moveset(trapped_opp.id, risk_averse=True)
            trapped_with_us = True
            for move in trapped_opp_moveset:
                min_x, max_x = min([pos.x for pos in self.board.ff_bounds]), max([pos.x for pos in self.board.ff_bounds])
                min_y, max_y = min([pos.y for pos in self.board.ff_bounds]), max(
                    [pos.y for pos in self.board.ff_bounds])
                moved = trapped_opp.head.moved_to(move)
                if not (min_x <= moved.x <= max_x and min_y <= moved.y <= max_y):
                    trapped_with_us = False
                    self.board.touch_opps.remove(trapped_opp.head)
                    break
            # We'll win the incoming collision if we're longer and colliding on the same square
            if trapped_with_us and dist_to_trapped_opp % 2 == 1 and self.you.length > trapped_opp.length:
                return False, None
            elif trapped_with_us:
                collision_sq = path_to_trapped_opp[len(path_to_trapped_opp) // 2]

        # If space frees up after X moves, identify where the opening in our flood fill is
        openings_in_boundary = []
        found_opening = False
        moves_until_opening = None
        for move_num in range(1, round(self.board.space_all) + 2):
            # Simulate each snake's new position if its tail were moved forward by 1
            for snake in self.all_snakes.values():
                new_tail = snake.body[max(-snake.length + 1, -move_num)]
                # Until we detect a hole in our flood fill boundary
                if new_tail in self.board.ff_bounds:
                    found_opening = True
                    openings_in_boundary.append(new_tail)
            # We found an opening! Keep track of how many moves it took to appear
            if found_opening:
                moves_until_opening = move_num
                break

        # We're not trapped if we can reach the opening in our flood fill before space runs out!
        if len(openings_in_boundary) > 0:
            # If there are multiple openings, select the one closest to our snake
            openings_in_boundary = sorted(openings_in_boundary, key=lambda op: self.you.head.manhattan_dist(op))
            opening = openings_in_boundary[0]
            longest_path_to_opening, shortest_path_to_opening = self.board.longest_path(
                self.you.head, opening, threshold=moves_until_opening)

            # See if we can successfully stall until the opening forms
            if collision_sq is None:
                trapped = longest_path_to_opening < moves_until_opening
                # If we found an opening, consider whether there's an opponent snake waiting for us there
                if not trapped:
                    snakes_near = [opp for opp in self.opponents.values() if (
                            opp.head.manhattan_dist(opening) <= shortest_path_to_opening)]
                    # Give more weight to enemy snakes that can kill us
                    threats_near = [opp for opp in snakes_near if opp.length >= self.you.length]
                    # Our escape heuristic penalises longer escape routes and routes with a possible opponent waiting
                    esc_penalty = -(shortest_path_to_opening + 5 * len(snakes_near) + 10 * len(threats_near))
            # If there's another trapped snake approaching us, see if we can reach the opening before a collision
            elif self.board.shortest_dist(self.you.head, opening) >= self.board.shortest_dist(
                    self.you.head, Pos({"x": collision_sq[0], "y": collision_sq[1]})):
                trapped = True
        else:
            trapped = True

        return trapped, esc_penalty

    def edge_kill_detection(self, snake_id) -> bool:
        """
        Determine if a snake is in a position where it can get edge-killed. Assumes that trap_detection ran first.

        :param snake_id: The ID of the desired snake we want to detect a possible edge kill for

        :return: True if the snake can get edge-killed, False otherwise
        """
        # Establish who the snake is and who the possible killers are
        snake = self.all_snakes[snake_id]
        opponents = [opp for opp in self.all_snakes.values() if snake.id != opp.id]
        possible_moves = self.get_moveset(snake.id, risk_averse=True, turn="basic")
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

        # Determine if we can get edge-killed by a longer snake in front of us, behind us, or two over from us
        board = self.board.board
        trapped_sides = [False, False]
        edge_killers = [None, None]
        trapped_by_ourselves = False
        trapped_by_edge = False
        if len(set(escape_dirs).intersection(possible_moves)) == 0:
            # Scan the column/row to each side of us in ascending order
            for num, escape_dir in enumerate(escape_dirs):
                look = -1 if num == 0 else +1
                esc_move = getattr(snake.head, ax) + look
                # Off-limits if it's outside the board
                if bounds[0] <= esc_move < bounds[1]:
                    # Check the space in the column/row to the side and ahead of us
                    if ax == "x":
                        strip = board[esc_move, getattr(snake.head, ax_dir):] if scan_dir == +1 \
                            else board[esc_move, :(getattr(snake.head, ax_dir) + 1)][::-1]
                    else:
                        strip = board[getattr(snake.head, ax_dir):, esc_move] if scan_dir == +1 \
                            else board[:(getattr(snake.head, ax_dir) + 1), esc_move][::-1]
                    # Check if we're trapped by our own body
                    if strip[0] == "0" and snake_id == self.you.id:
                        # First check if our body's blocking our path ahead
                        if ax == "x":
                            our_strip = board[getattr(snake.head, ax), getattr(snake.head, ax_dir):] if scan_dir == +1 \
                                else board[getattr(snake.head, ax), :(getattr(snake.head, ax_dir) + 1)][::-1]
                        else:
                            our_strip = board[getattr(snake.head, ax_dir):, getattr(snake.head, ax)] if scan_dir == +1 \
                                else board[:(getattr(snake.head, ax_dir) + 1), getattr(snake.head, ax)][::-1]
                        if "0" in our_strip:
                            self_collision_dist = our_strip.tolist().index("0")
                            self_collision_pos = self.you.head.moved_to(direction, distance=self_collision_dist)
                            # If our tail doesn't get out of our way in time, we're doomed
                            if len(self.you.body) - self.you.body.index(self_collision_pos) > self_collision_dist:
                                trapped_sides[num] = True
                                trapped_by_ourselves = True
                                continue
                        # esc_square = [num for num, sq in enumerate(strip) if sq != "0"][0]
                        # idx_body_obstacle = self.you.body.index(self.you.head.moved_to(escape_dir))
                        # if len(self.you.body[idx_body_obstacle:]) >= 5:
                        #     trapped_sides[num] = True
                        #     trapped_by_ourselves = True
                        #     continue
                    # If there's an opponent head there, we might be getting edge-killed
                    elif "H" in strip:
                        # Examine the portion preceded by the opponent head (verify there aren't any gaps)
                        danger_strip = strip[:np.where(strip == "H")[0][0]]
                        # Identify the killer
                        if ax == "x":
                            opp_loc = Pos({"x": esc_move,
                                           "y": getattr(snake.head.moved_to(direction, len(danger_strip)), ax_dir)})
                        else:
                            opp_loc = Pos({"x": getattr(snake.head.moved_to(direction, len(danger_strip)), ax_dir),
                                           "y": esc_move})
                        opp_killer = self.board.identify_snake(opp_loc)

                        # Check if the opponent is bound to turn around and collide with us (which is not an edge kill)
                        opp_next_dirs = self.get_moveset(opp_killer.id, risk_averse=False)
                        if len(opp_next_dirs) == 1 and set(escape_dirs) == {opp_next_dirs[0], escape_dir}:
                            pass  # TODO entrapment?
                        # Check if the opponent is going the same direction as us (it's not yet an edge kill if not)
                        elif opp_killer.facing_direction() == direction:
                            # Check if there are gaps between us and the killer, we're dead if there's none
                            if np.count_nonzero(danger_strip == " ") == 0:
                                trapped_sides[num] = True
                                edge_killers[num] = opp_killer
                                continue
                    else:
                        # Check to see if there's free space for us to escape to or if we're trapped
                        if self.trapped and np.count_nonzero(strip == " ") == 0:
                            trapped_sides[num] = True
                            continue

                    # Check the space directly behind and to the side of us for any possible edge-killers
                    if ax == "x":
                        threat_behind = Pos({"x": esc_move, "y": getattr(snake.head, ax_dir) - 1}) if scan_dir == +1 \
                            else Pos({"x": esc_move, "y": getattr(snake.head, ax_dir) + 1})
                        threat_strip = board[esc_move, getattr(snake.head, ax_dir) - 1:] if scan_dir == +1 \
                            else board[esc_move, :(getattr(snake.head, ax_dir) + 2)][::-1]
                    else:
                        threat_behind = Pos({"x": getattr(snake.head, ax_dir) - 1, "y": esc_move}) if scan_dir == +1 \
                            else Pos({"x": getattr(snake.head, ax_dir) + 1, "y": esc_move})
                        threat_strip = board[getattr(snake.head, ax_dir) - 1:, esc_move] if scan_dir == +1 \
                            else board[:(getattr(snake.head, ax_dir) + 2), esc_move][::-1]
                    # Also check if there's a possible edge-killer 2 columns/rows over from us
                    esc_move_x2 = snake.head.as_dict()[ax] + (look * 2)
                    if ax == "x":
                        threat_two_over = Pos({"x": esc_move_x2, "y": getattr(snake.head, ax_dir)})
                        if not getattr(threat_two_over, ax) >= self.board.width:
                            threat_strip = board[esc_move_x2, getattr(snake.head, ax_dir):] if scan_dir == +1 \
                                else board[esc_move_x2, :(getattr(snake.head, ax_dir) + 1)][::-1]
                    else:
                        threat_two_over = Pos({"x": getattr(snake.head, ax_dir), "y": esc_move_x2})
                        if not getattr(threat_two_over, ax) >= self.board.height:
                            threat_strip = board[getattr(snake.head, ax_dir):, esc_move_x2] if scan_dir == +1 \
                                else board[:(getattr(snake.head, ax_dir) + 1), esc_move_x2][::-1]
                    # If there's a longer snake in either of those two locations, we might be getting edge-killed
                    opp_killers = [opp for opp in opponents if (  # TODO cleanup
                            opp.length > snake.length or (opp.length == snake.length and "f" in threat_strip)) and (
                            (opp.head == threat_behind and direction in self.get_moveset(opp.id)) or
                            opp.head == threat_two_over)]
                    if len(opp_killers) > 0:
                        trapped_sides[num] = True
                        edge_killers[num] = sorted(opp_killers, key=lambda op: op.length, reverse=True)[0]
                else:
                    trapped_sides[num] = True
                    trapped_by_edge = True

        # If both sides of the snake are blocked in, then we're trapped
        if trapped_by_edge and trapped_by_ourselves:
            return False
        else:
            return True if sum(trapped_sides) == 2 else False  # TODO return edge-killers too

    def heuristic(self, tree_depth: Optional[int] = 4) -> tuple[float, dict]:
        """
        Evaluate the current board for our snake (the higher the heuristic, the better).

        :param tree_depth: The current depth our snake is at in the minimax search tree

        :return:
            The computed heuristic value
            A dictionary of select metrics to be used for debugging
        """
        # How many layers deep in the game tree are we? (Reward longevity)
        current_depth = self.minimax_search_depth - tree_depth
        current_depth_weight = 25

        # Did we increase in length? (Reward any food eaten)
        incr_length = self.you.length - self.og_length
        incr_length_weight = 1250

        opp_periphs = {}
        for opp_id in self.opponents.keys():
            opp_periphs[opp_id] = self.board.flood_fill(opp_id, risk_averse=False, confine_to="auto")

        # Did any opponent snakes die or increase in length? (Higher opponent total => worse for us)
        leftover_opps = [opp for opp in self.opponents.values() if opp_periphs[opp.id] >= 3]
        tot_opp_length = sum([opp.length for opp in leftover_opps])
        tot_opp_length_weight = 25 if len(leftover_opps) == len(self.opponents) else 500

        # Remove other snakes that we're not edge-killing who's def dead
        if len(self.opponents) >= 2:
            basically_dead_opps = [opp.id for opp in self.opponents.values() if opp_periphs[opp.id] < 1 and self.you.head.manhattan_dist(opp.head) >= 5]
            self.board.remove_snake(basically_dead_opps)
            for dead_opp in basically_dead_opps:
                # self.all_snakes.pop(dead_opp)
                self.opponents.pop(dead_opp)

        next_moves = self.get_moveset(snake_id=self.you.id, risk_averse=True)
        ff_split =  set(next_moves) == {"left", "right"}
        # How much space do we have?
        self.board.whiteout(crop_centre=self.you.head)
        space_ra, space_all, ff_bounds, touch_opps = self.board.flood_fill(self.you.id, full_package=True, ff_split=ff_split)
        space_ra_weight = 1

        # How cl
        dist_from_enemies = sorted(
            [self.board.shortest_dist(self.you.head, opp.head) for opp in self.opponents.values()])

        # Determine the closest safe distance to food
        dist_food, best_food = self.board.closest_dist_to_food(self.you.id)
        if best_food is not None:
            logging.info(f"Closest distance to food = {dist_food, best_food.as_dict()}")
        # Determine how important food is
        opp_lengths = [opp.length for opp in self.opponents.values()]
        longest_flag = False
        if self.you.health < 40:  # Low health alert
            food_weight = 300
        elif self.you.length <= max(opp_lengths):  # If we're not the longest snake
            food_weight = 200
        elif self.you.length > max(opp_lengths):  # If we are the longest snake
            longest_flag = True
            if self.you.length > max(opp_lengths) + 10:
                food_weight = 1
                incr_length_weight = 1
            elif dist_food < min(dist_from_enemies):  # Might as well get food if convenient
                food_weight = 100
            else:  # Food isn't that important at the moment
                food_weight = 25
        elif dist_food <= 3:  # Guarantee eating food the closer we are to it
            food_weight = 300 / dist_food
        else:
            food_weight = 50

        # How much space do we have in our peripheral?
        periph_ra, periph_all, periph_bounds, _ = self.board.flood_fill(self.you.id, confine_to="auto", full_package=True)
        periph_all_weight = 2

        # Size of our peripheral
        periph_penalty = 0
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
        elif space_ra <= 1:  # Basically trapped
            space_penalty = -1500
        elif space_ra <= 3:
            space_penalty = -500

        # Are we trapped? (With no incoming opponents trapped with us)
        if space_all <= 15:
            self.trapped, esc_penalty = self.trap_detection()
            # Penalise entrapment (-1e7) more than getting killed by an opponent (-1e6)
            space_penalty = -1e7 if self.trapped and len(self.board.touch_opps) == 0 else space_penalty
            space_penalty += esc_penalty if not self.trapped and esc_penalty is not None else 0
            periph_all_weight = 0.5
        else:
            self.trapped = False

        # Are we in danger of getting edge-killed?
        edge_killed = self.edge_kill_detection(self.you.id)
        space_penalty = -1e7 if edge_killed else space_penalty

        # # Are we cornering ourselves?
        # next_moves = self.get_moveset(snake_id=self.you.id, risk_averse=True)
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

            if len(move := self.get_moveset(self.all_snakes[closest_enemy].id)) == 1:
                confine_to = move[0]
            else:
                confine_to = "auto"

            available_enemy_space_ra, available_enemy_space_all, _, _ = self.board.flood_fill(closest_enemy, full_package=True)
            available_enemy_space = self.board.flood_fill(closest_enemy, risk_averse=True, confine_to=confine_to)

            aggression_okay = self.you.length >= 6 and space_ra >= 5 or (self.you.length < 6 and
                                                      ( self.all_snakes[closest_enemy].head.x in [0, 1, self.board.width - 2, self.board.width - 1] and
                                                       self.all_snakes[closest_enemy].head.y in [0, 1, self.board.height - 2, self.board.height - 1])) # TODO BROKE EVERYTHING

            if aggression_okay and ( periph_ra > available_enemy_space or space_all > available_enemy_space_all):
                if available_enemy_space_ra <= 5:
                    kill_bonus = 2000

                elif available_enemy_space < 4:
                    kill_bonus = 1000
                elif available_enemy_space_ra <= 15 and space_ra > available_enemy_space_ra + 2:  # Yay but only if we're not gonna be doo-doo
                    kill_bonus = 750
                    space_penalty = 0  # restore our space advantage hehe
                elif available_enemy_space_ra < self.opponents[closest_enemy].length / 2.75:  # Used to be 4
                    kill_bonus = 500
                else:
                    kill_bonus = 0
            else:
                kill_bonus = 0

            if kill_bonus < 2000:
                edge_killed = self.edge_kill_detection(closest_enemy)
                if edge_killed and space_ra >= 5:  # only if we're not trapped lmao
                    kill_bonus = 2000

            if kill_bonus > 0:
                if kill_bonus != 2000:  # When it's not guaranteed yet
                    # Reward getting closer, but only if it doesn't trap us
                    kill_bonus += (1000 / self.board.shortest_dist(self.you.head, self.all_snakes[closest_enemy].head) if not self.trapped else 0)
                else:  # Guaranteed
                    space_penalty = space_penalty / 2
                # Reward if the opponent is getting the least space
                kill_bonus += (1000 / max(1, available_enemy_space_ra) if not self.trapped else 0)

        else:
            available_enemy_space = -2
            kill_bonus = 0

        # Did we kill any opponents previously? Reward quicker kills
        kill_bonus += 10000 * len(self.kill_count) + 2 * sum(self.kill_count)

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
        threats = []
        for opp in self.opponents.values():
            if opp.length > self.you.length and opp.head.within_bounds(self.you.peripheral_vision(return_pos_only=True)):
                threats.append(self.board.shortest_dist(self.you.head, opp.head))
            elif opp.length == self.you.length and self.board.closest_dist_to_food(opp.id)[0] <= 3 and opp.head.within_bounds(
                       self.you.peripheral_vision(return_pos_only=True)):
                threats.append(self.board.shortest_dist(self.you.head, opp.head))

        num_threats = (np.count_nonzero(np.array(threats) <= 2) * 2
                       + np.count_nonzero(np.array(threats) == 3) * 1)


        # Are we in the centre of the board? Maximise control
        centre = range(self.board.width // 2 - 2, self.board.width // 2 + 3)
        in_centre = self.you.head.x in centre and self.you.head.y in centre and (
                len(self.opponents) <= 2 or num_threats == 0) and best_food is None
        # Are we on the edge? Try to stay away if possible
        on_edge = self.you.head.x in [0, self.board.width - 1] or self.you.head.y in [0, self.board.height - 1]

        collision_inbound = False
        me = self.get_moveset(snake_id=self.you.id)
        closest_opp = sorted(self.opponents.values(),
                             key=lambda opp: self.board.shortest_dist(self.you.head, opp.head))[0]

        them = self.get_moveset(snake_id=closest_opp.id)
        diff_lengths = closest_opp.length - self.you.length
        if diff_lengths > 0:
            connection = closest_opp.head.direction_to(self.you.head)
            # This means they're headed towards us
            if closest_opp.facing_direction() in connection:
                # If we have no choice but to head towards the opponent as well  (e.g. if the enemy is heading up and left, we have no choice but to move down or right)
                if sum([esc in me for esc in connection]) == 0:  # TODO code flood fill for the esc direction in case they're trapping us
                    collision_inbound = True
        if collision_inbound:
            danger_penalty = -15 * diff_lengths - 15/self.you.head.manhattan_dist(closest_opp.head)
        else:
            danger_penalty = 0

        # Can we cut off our opponents?


        # TODO corner edge case
        cutoff_bonus = 0
        cutting_off = None
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
        opps_nearby = [opp for opp in self.opponents.values() if self.you.head.manhattan_dist(opp.head) <= 4]
        if 0 < len(opps_nearby) <= 2 or len(self.opponents) == 1:
            # if cutting_off is not None:
            #     us_cutoff = cutting_off
            # else:
            #     us_cutoff = self.board.flood_fill(closest_opp.id, opp_cutoff=self.you.id)
            # opp_cutoff = self.board.flood_fill(self.you.id, opp_cutoff=closest_opp.id)

            if len(self.opponents) == 1:
                if cutting_off is not None:
                    us_cutoff = cutting_off
                else:
                    us_cutoff = self.board.flood_fill(closest_opp.id, opp_cutoff=self.you.id)
                opp_cutoff = self.board.flood_fill(self.you.id, opp_cutoff=closest_opp.id)
            else:
                us_cutoff = self.board.flood_fill(opps_nearby[0].id, opp_cutoff=self.you.id)
                opp_cutoff = self.board.flood_fill(self.you.id, opp_cutoff=opps_nearby[0].id)
            if self.you.length < closest_opp.length:
                if opp_cutoff < 15:
                    if space_penalty == 0:
                        space_penalty = -500
            else:
                if opp_cutoff <= 15 and us_cutoff > opp_cutoff:  # Penalise if we're in a worse position
                    if space_penalty == 0:
                        space_penalty = -500
                        if aggression_weight > 500:
                            aggression_weight /= 10
                        if incr_length_weight > 1000:
                            incr_length_weight /= 10
                        if kill_bonus > 0 and opp_cutoff <= 5:  # If we kill but get killed anyways
                            kill_bonus = 0
                    if cutoff_bonus > 0:  # Reduce the cutoff if we're the ones getting cut off lol
                        cutoff_bonus = 0

        # if space_penalty < 0:
        #     length_weight = 100

        # Heuristic formula
        enemy_restriction_weight = 0 if available_enemy_space == -2 else 75 if len(self.opponents) > 2 else 200
        if self.trapped or edge_killed:
            enemy_restriction_weight = 0

        if dist_to_enemy >= self.board.width * 2:  # Enemy is wayyy too far away for it to matter
            enemy_restriction_weight = 0


        if kill_bonus > 0:
            food_weight = 10
            periph_all_weight = 0.5
        # Get more aggressive if we're longer and there's only one snake left!
        if len(self.opponents) == 1 and longest_flag:
            periph_all_weight = 0.5

        centre_control_weight = 20 if not (self.trapped or edge_killed) else 0
        on_edge_penalty = -20 if not (self.trapped or edge_killed) else 0
        # if sum([n in necessary_moves for n in next_moves]) < len(necessary_moves):  # Don't penalise being on the edge if we've no other choice
        #     on_edge_penalty = 0
        threat_proximity_weight = -25

        if len(threats) == 0 and kill_bonus == 0 and cutoff_bonus == 0:
            if not longest_flag:  # We're chilling tbh but need FOOD
                food_weight = 350
            else:  # compete for food
                opp_dist_food, opp_best_food = self.board.closest_dist_to_food(closest_opp.id, risk_averse=False)
                if len(self.opponents) == 1 and best_food is not None and opp_best_food is not None:
                    if opp_best_food == best_food and opp_dist_food <= dist_food + 2:
                        food_weight = 250

        h = (space_ra * space_ra_weight) + space_penalty + \
            (periph_all_weight * periph_all) + periph_penalty + \
            (tot_opp_length_weight / (tot_opp_length + 1)) + \
            (threat_proximity_weight * num_threats) + danger_penalty + \
            (food_weight / (dist_food + 1)) + \
            (current_depth * current_depth_weight) + \
            (incr_length * incr_length_weight) + \
            in_centre * centre_control_weight + \
            on_edge * on_edge_penalty + \
            aggression_weight / (dist_to_enemy + 1) + cutoff_bonus + \
            (enemy_restriction_weight / (available_enemy_space + 1)) + kill_bonus

        h_dict = {
            "Heuristic": round(h, 2),
            "Space | Pen": f"{space_ra} | {round(space_penalty, 2)} => {round((space_ra * space_ra_weight) + space_penalty, 2)}",
            "Centre | Edge": f"{in_centre * centre_control_weight} | {on_edge * on_edge_penalty}",
            "Periph | Pen": f"{periph_all} | {periph_penalty} => {periph_all_weight * periph_all + periph_penalty}",
            "Food | Opp Dist": f"{dist_food} {dist_to_enemy} | => {round(food_weight / (dist_food + 1), 2)} | {round((aggression_weight / (dist_to_enemy + 1)), 2)}",
            "Opp Space | Len": f"{available_enemy_space} | {tot_opp_length} => {round((enemy_restriction_weight / (available_enemy_space + 1)), 2)} | {round(tot_opp_length_weight / (tot_opp_length + 1), 2)}",
            "Danger | Kill | Cutoff": f"{round(danger_penalty, 2)} | {round(kill_bonus, 2)} | {round(cutoff_bonus, 2)}",
            "Threats": f"{num_threats} => {(threat_proximity_weight * num_threats) + danger_penalty}",
            "+Length": f"{incr_length} => {(incr_length * incr_length_weight)}"
        }

        for key, value in h_dict.items():
            logging.info(f"{key:<30}{value}")

        return h, h_dict

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
        if depth != self.minimax_search_depth and self.turn > 0:
            alive = not self.you.dead  # self.board.is_pos_safe(self.you.head, self.you.id, turn="done" if depth % 2 == 0 else "ours")
            game_over = len(self.opponents) == 0
            if not alive:
                killer_penalty = 0
                if self.killer_intel is not None:
                    # We'd prefer to get killed by a smaller snake in case we're the same length and can kill them too
                    # How likely is the killer going to deliver the coup de grâce? E.g. it could get distracted by food
                    killer_length, distraction = self.killer_intel
                    # If we got immediately killed, then it's much worse than an edge kill down the line
                    immediately_killed = -1e8 if depth >= self.minimax_search_depth - 2 else 0
                    # Add a killer penalty score to give higher weight to more advantageous deaths
                    killer_penalty = (immediately_killed if distraction >= 5 else 0) - killer_length + (distraction * 2 if distraction <= 4 else 0)
                # Big idea: reward slower deaths, penalise immediate death, account for dumb opponents not killing
                heuristic = -1e6 + (self.minimax_search_depth - depth) + killer_penalty
                logging.info(f"Our snake died...\nHeuristic = {heuristic}")
                return heuristic, None, {"Score": heuristic}
            # If our snake is the winner :)
            elif game_over:
                heuristic = 1e6 + depth  # Reward faster kills
                logging.info(f"Our snake won!!\nHeuristic = {heuristic}")
                return heuristic, None, {"Score": heuristic}

        # If we're at the bottom of the decision tree
        if depth == 0:
            logging.info("=" * 75)
            logging.info(f"DEPTH = {depth}")
            score, score_metrics = self.heuristic(tree_depth=depth)
            return score, None, score_metrics

        if maximising_snake:  # Our turn
            logging.info("=" * 75)
            logging.info(f"DEPTH = {depth} OUR SNAKE")
            logging.info(f"alpha = {alpha} | beta = {beta}")

            clock_in = time.time_ns()
            # Determine our snake's possible moves, sorted by the amount of immediate space it'd give us
            possible_moves = self.get_moveset(self.you.id, risk_averse=self.you.length <= 5, sort_by_periph=True)
            # In the early stages of the game, if we're out of risk-averse moves, accept risk
            if len(possible_moves) == 0 and self.you.length <= 5:
                possible_moves = self.get_moveset(self.you.id, risk_averse=False, sort_by_periph=True)
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
                opp_moves = self.get_moveset(opp_id, both_risk_options=True)
                if len(opp_moves) == 0:  # If the opponent has no legal moves, move down and die
                    opp_moves = ["down"]
                # Assume our opponents are smart - for each possible move, compute how beneficial it'd be for them
                # Opponent heuristic => favours proximity to our snake, more space, longer length, and penalises death
                opp_scores = []
                for move in opp_moves:
                    moved_head = opp_snake.head.moved_to(move)
                    dist_from_us = self.board.shortest_dist(self.you.head, moved_head)
                    opp_space = self.board.flood_fill(opp_id, risk_averse=False, confine_to=move)
                    opp_dist_to_food = min([1e6] + [moved_head.manhattan_dist(food) for food in self.board.food])
                    our_dist_to_food, _ = self.board.closest_dist_to_food(self.you.id, risk_averse=False)
                    opp_aggression = (opp_snake.length > self.you.length and
                                      (moved_head.manhattan_dist(self.you.head) <= self.board.width // 2 or
                                      opp_dist_to_food * 3 < our_dist_to_food))
                    opp_food = 0 if opp_dist_to_food >= 3 or opp_aggression \
                        else -2 if opp_dist_to_food == 2 else -5
                    opp_penalty = 100 if dist_from_us == 1 and opp_snake.length <= self.you.length else 0
                    aggressor = dist_from_us if not opp_aggression else dist_from_us
                    if dist_from_us >= 8 and moved_head.manhattan_dist(self.you.head) >= 7 and len(self.opponents) > 1:
                        aggressor *= 2
                    opp_scores.append(
                        (opp_id,
                         aggressor + opp_food + opp_penalty + ((10 / opp_space) if opp_space >= 1 else 0))
                    )
                    # print(f"Dist: {dist_from_us}, Aggro: {aggressor}, Food: {opp_food}, Space: {round(((10 / opp_space) if opp_space >= 1 else 0), 2)}, Pen: {opp_penalty})")
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

            # Determine the maximum number of move combinations
            opps_nearby = [opp for opp in self.opponents.values() if self.you.head.manhattan_dist(opp.head) <= 5]
            if len(opps_nearby) >= 3:
                num_sims = 3
            else:
                num_sims = 3

            # Now that we have ranked moves for each opponent, we need to create move combinations in order of how
            # threatening they are. The idea is to centre movesets around the "worst" move that ANY opponent can make
            # and fill in moves for the rest of the opponents in order of how bad they are
            threat_opps = sorted(opps_scores, key=lambda combo: combo[1])  # Sort all opponent moves by their heuristic
            worst_opp_tracker = {}  # Keep track of which opponent moves we've finished building move combos around
            sim_move_combos = []  # Append simulations for final move combinations (each one is a child node)
            sim_movesets = []  # For each simulation, keep track of the move combination, so we don't repeat any
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
                simulation = self.simulate_move(move_combo, evaluate_deaths=True, depth=depth)
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
        """Main function to identify the most optimal move for our snake."""
        if self.turn <= 3:
            depth = 3
        else:
            depth = self.minimax_search_depth

        logging.info("STARTING POSITION")
        self.board.update_board()
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
            plt.figure(figsize=(50, 25))
            nx.draw(G, pos=pos, node_color=["white"] * G.number_of_nodes(), edge_color=edge_colours, width=edge_widths,
                    labels=node_labels, with_labels=True, node_size=40000, font_size=20)
            plt.savefig("minimax_tree.png", bbox_inches="tight", pad_inches=0)
