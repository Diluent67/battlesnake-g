import pytest
from Board import Board
from Pos import Pos
from Snake import Snake

one = {"game":{"id":"0eecf020-5cc2-4da5-adb4-33d2fabc580b","ruleset":{"name":"standard","version":"cli","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":14,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":25},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":""},"turn":63,"board":{"height":11,"width":11,"snakes":[{"id":"63f6454f-3f0b-4959-a46a-b6173bf97d9f","name":"JonK","latency":"24","health":85,"body":[{"x":6,"y":1},{"x":7,"y":1},{"x":8,"y":1},{"x":9,"y":1},{"x":10,"y":1},{"x":10,"y":2},{"x":10,"y":3},{"x":10,"y":4},{"x":10,"y":5}],"head":{"x":6,"y":1},"length":9,"shout":"","squad":"","customizations":{"color":"#B7410E","head":"sleepy","tail":"offroad"}},{"id":"73ec1a21-05e9-40da-854d-70e7562141ba","name":"Rick2","latency":"138","health":90,"body":[{"x":3,"y":4},{"x":4,"y":4},{"x":5,"y":4},{"x":6,"y":4},{"x":6,"y":3},{"x":7,"y":3},{"x":7,"y":2}],"head":{"x":3,"y":4},"length":7,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"e995934c-190f-4e1f-ae73-9623eae1ad42","name":"Nightwing","latency":"88","health":95,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":4,"y":1},{"x":3,"y":1},{"x":3,"y":0},{"x":2,"y":0}],"head":{"x":3,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}},{"id":"ac9551aa-67aa-403e-bdea-68637eafa25e","name":"Rick","latency":"138","health":49,"body":[{"x":3,"y":6},{"x":3,"y":5},{"x":4,"y":5},{"x":5,"y":5},{"x":5,"y":6},{"x":5,"y":7}],"head":{"x":3,"y":6},"length":6,"shout":"","squad":"","customizations":{"color":"#00ff00","head":"shark","tail":"coffee"}},{"id":"5ef4a0b9-14fe-49e5-9614-4a045cc95a15","name":"Matt","latency":"37","health":94,"body":[{"x":1,"y":2},{"x":1,"y":3},{"x":1,"y":4},{"x":1,"y":5},{"x":0,"y":5},{"x":0,"y":4}],"head":{"x":1,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#1f9490","head":"default","tail":"default"}}],"food":[{"x":6,"y":5}],"hazards":[]},"you":{"id":"e995934c-190f-4e1f-ae73-9623eae1ad42","name":"Nightwing","latency":"88","health":95,"body":[{"x":3,"y":2},{"x":4,"y":2},{"x":4,"y":1},{"x":3,"y":1},{"x":3,"y":0},{"x":2,"y":0}],"head":{"x":3,"y":2},"length":6,"shout":"","squad":"","customizations":{"color":"#3333ff","head":"ski","tail":"mystic-moon"}}}

@pytest.mark.parametrize(argnames="game_state", argvalues=[one])
def test_board(game_state):
    board = Board(game_state["board"])
    print("\n\n\n")
    print(board.__str__())

    me = list(board.all_snakes.keys())[3]
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="auto")
    board.crop_board(xs, ys)
    print("\n")
    print(board.__str__())


    board = Board(game_state["board"])
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="left")
    board.crop_board(xs, ys)
    print("\n")
    print("LEFT")
    board.board[head.x, head.y] = "!"
    print(board.__str__())

    board = Board(game_state["board"])
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="right")
    board.crop_board(xs, ys)
    print("\n")
    print("RIGHT")
    board.board[head.x, head.y] = "!"
    print(board.__str__())

    board = Board(game_state["board"])
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="up")
    board.crop_board(xs, ys)
    print("\n")
    print("UP")
    board.board[head.x, head.y] = "!"
    print(board.__str__())

    board = Board(game_state["board"])
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="down")
    board.crop_board(xs, ys)
    print("\n")
    print("DOWN")
    board.board[head.x, head.y] = "!"
    print(board.__str__())

    board = Board(game_state["board"])
    xs, ys, head = board.all_snakes[me].peripheral_vision(direction="other")
    board.crop_board(xs, ys)
    print("\n")
    print("OTHER")
    board.board[head.x, head.y] = "!"
    print(board.__str__())
