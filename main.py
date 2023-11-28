# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

import time
import typing
from snake_engine import Battlesnake


def info() -> typing.Dict:
    """
    info is called when you create your Battlesnake on play.battlesnake.com
    and controls your Battlesnake's appearance
    TIP: If you open your Battlesnake URL in a browser you should see this data
    """
    print("INFO")

    return {
        "apiversion": "1",
        "author": "G",
        "color": "#1F51FF",
        "head": "workout",
        "tail": "curled",
    }


def start(game_state: typing.Dict):
    """start is called when your Battlesnake begins a game"""
    print("GAME START")


def end(game_state: typing.Dict):
    """end is called when your Battlesnake finishes a game"""
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:
    """
    move is called on every turn and returns your next move
    Valid moves are "up", "down", "left", or "right"
    See https://docs.battlesnake.com/api/example-move for available data
    """
    clock_in = time.time_ns()
    game = Battlesnake(game_state)
    optimal_move = game.optimal_move()
    print(f"Turn {game_state['turn']} took {round((time.time_ns() - clock_in) / 1000000, 3)} ms")
    print(f'Latency: {game_state["you"]["latency"]} for Game {game_state["game"]["id"]}')
    return {"move": optimal_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
