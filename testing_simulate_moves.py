from snake_engine import Battlesnake


game_state = {'turn': 118, 'board': {'height': 11, 'width': 11, 'food': [{'x': 9, 'y': 10}, {'x': 1, 'y': 0}], 'hazards': [], 'snakes': [{'id': 'd5e07ec6-ad02-40ac-b718-07acc29d2585', 'name': 'Nightwing', 'health': 67, 'body': [{'x': 7, 'y': 4}, {'x': 7, 'y': 3}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}, {'x': 6, 'y': 5}, {'x': 7, 'y': 5}, {'x': 8, 'y': 5}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}], 'head': {'x': 7, 'y': 4}, 'length': 9, 'food_eaten': None}, {'id': 'cbb9ad4b-82a2-421b-a16a-1c98c3d61b2a', 'name': 'Rick2', 'health': 98, 'body': [{'x': 5, 'y': 2}, {'x': 4, 'y': 2}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}, {'x': 3, 'y': 4}, {'x': 3, 'y': 5}, {'x': 4, 'y': 5}], 'head': {'x': 5, 'y': 2}, 'length': 7, 'food_eaten': None}, {'id': 'e30f8f2d-802f-49c6-acee-44ed46d17975', 'name': 'JonK3', 'health': 98, 'body': [{'x': 6, 'y': 9}, {'x': 6, 'y': 10}, {'x': 5, 'y': 10}, {'x': 5, 'y': 9}, {'x': 5, 'y': 8}, {'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 3, 'y': 7}, {'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 6}, {'x': 0, 'y': 6}, {'x': 0, 'y': 7}, {'x': 0, 'y': 8}, {'x': 1, 'y': 8}], 'head': {'x': 6, 'y': 9}, 'length': 15, 'food_eaten': None}]}, 'you': {'id': 'd5e07ec6-ad02-40ac-b718-07acc29d2585', 'name': 'Nightwing', 'health': 67, 'body': [{'x': 7, 'y': 4}, {'x': 7, 'y': 3}, {'x': 6, 'y': 3}, {'x': 6, 'y': 4}, {'x': 6, 'y': 5}, {'x': 7, 'y': 5}, {'x': 8, 'y': 5}, {'x': 8, 'y': 4}, {'x': 8, 'y': 3}], 'head': {'x': 7, 'y': 4}, 'length': 9, 'food_eaten': None}}

b = Battlesnake(game_state, debugging=True)

# Choose to simulate full set of opponent moves only if they're within a certain distance of our snake
if len(b.opponents) == 1:
    search_within = b.board.width * b.board.height
elif len(b.opponents) == 2:
    search_within = b.board.width
else:
    search_within = b.board.width // 2

# Store possible moves for each snake id
opps_moves = {}
opps_scores = []
for opp_num, (opp_id, opp_snake) in enumerate(b.opponents.items()):
    opp_moves = b.get_obvious_moves(opp_id, risk_averse=False, sort_by_dist_to=b.you.id)
    # If the snake has no legal moves, move down and die
    if len(opp_moves) == 0:
        opp_moves = ["down"]
    # Save time by only using full opponent move sets if they're within a certain range
    dist_to_opp = b.you.head.manhattan_dist(opp_snake.head)
    if dist_to_opp <= search_within:
        # opps_moves[opp_id] = opp_moves
        # For each possible move, estimate how close that brings the opponent to our snake
        opp_scores = [
            (opp_id,
             b.board.closest_dist(b.you.head, opp_snake.head.moved_to(move)) +
             (1 / (opp_snake.length + (1 if opp_snake.head.moved_to(move) in b.board.food else 0))) +
             ((1 / b.board.flood_fill(opp_id, confined_area=move)) if b.board.flood_fill(opp_id, confined_area=move) >= 1 else 0)
             ) for move in opp_moves]
        opps_scores.extend(opp_scores)
        opp_moves = [x for _, x in sorted(zip([s[1] for s in opp_scores], opp_moves))]
        opps_moves[opp_id] = opp_moves
        print(f"Snake {opp_num + 1} possible moves: {opp_moves} -> "
                     f"{[round(score[1], 2) for score in opps_scores[-len(opp_moves):]]}")
    else:
        opps_moves[opp_id] = [opp_moves[0]]
        opps_scores.extend([
            (opp_id,
             b.board.closest_dist(b.you.head, opp_snake.head.moved_to(move)) +
             (1 / (opp_snake.length + (1 if opp_snake.head.moved_to(move) in b.board.food else 0))) +
             (1 / b.board.flood_fill(opp_id, confined_area=move))
             ) for move in opp_moves])
        print(f"Snake {opp_num + 1} possible moves: {opp_moves} but cut down to {opp_moves[0]} ->"
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
    for rest_opp in b.opponents.keys():
        if rest_opp != worst_opp:
            worst_move_combos[rest_opp] = opps_moves[rest_opp][0]

    # Avoid accidentally adding the same move combination
    if worst_move_combos not in sim_move_combos:
        sim_move_combos.append(worst_move_combos)

    # Stop simulating movesets after a cutoff value
    if len(sim_move_combos) >= num_sims:
        break


SIMULATED_BOARD_INSTANCE = b.simulate_move({b.you.id: "down"})