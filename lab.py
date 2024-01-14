"""
6.1010 Lab 4:
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.

    Representation:
    Dictionary: {player position, target positions, computer positions, wall positions}
    """
    level = {}
    level["size"] = (len(level_description), len(level_description[0]))
    level["targets"] = set()
    level["computers"] = set()
    level["walls"] = set()
    for r in range(len(level_description)):
        for c in range(len(level_description[0])):
            if "player" in level_description[r][c]:
                level["player"] = (r, c)
            if "target" in level_description[r][c]:
                level["targets"].add((r, c))
            if "computer" in level_description[r][c]:
                level["computers"].add((r, c))
            if "wall" in level_description[r][c]:
                level["walls"].add((r, c))
    return level


def empty_level(game):
    """
    Input:
    game state

    Returns:
    a 2D list of empty values, the same size as game["level"]
    """
    ret_level = []

    for r in range(game["size"][0]):
        ret_level.append([])
        for c in range(game["size"][1]):
            ret_level[r].append([])

    return ret_level


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    if game["targets"] == set():
        return False
    victory = True

    for target in game["targets"]:
        if target not in game["computers"]:
            victory = False
    return victory


def new_position(object, direction):
    """
    Input:
    Takes in a tuple object with two values, the first being an x coordinate
    and the second being a y coordinate. Also takes in a direction.

    Returns:
    a new tuple with the coordinates of the object updated to move one space
    in the direction of direction.
    """
    row = object[0]
    col = object[1]
    if direction == "up":
        row -= 1
    elif direction == "down":
        row += 1
    elif direction == "left":
        col -= 1
    elif direction == "right":
        col += 1

    return (row, col)


def game_copy(game):
    '''
    Input:
    game state

    Returns:
    a copy of the same game state
    '''
    ret = {}
    ret["size"] = (game["size"][0], game["size"][1])
    ret["player"] = game["player"]
    ret["targets"] = game["targets"].copy()
    ret["computers"] = game["computers"].copy()
    ret["walls"] = game["walls"].copy()
    return ret


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    ret_game = game_copy(game)
    can_move = True
    computer = False

    check_loc = new_position(ret_game["player"], direction)
    if check_loc in game["walls"]:
        can_move = False
    elif check_loc in game["computers"]:
        computer = True
        check_loc_two = new_position(check_loc, direction)
        if check_loc_two in game["walls"] or check_loc_two in game["computers"]:
            can_move = False
    if can_move:
        new_pos = new_position(ret_game["player"], direction)
        ret_game["player"] = new_pos
        if computer:
            for position in ret_game["computers"]:
                if position == new_pos:
                    ret_game["computers"].remove(new_pos)
                    ret_game["computers"].add(new_position(new_pos, direction))
    return ret_game


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    ret_level = empty_level(game)
    for r in range(game["size"][0]):
        for c in range(game["size"][1]):
            if (r, c) in game["walls"]:
                ret_level[r][c].append("wall")
            if (r, c) in game["targets"]:
                ret_level[r][c].append("target")
            if (r, c) in game["computers"]:
                ret_level[r][c].append("computer")
            if (r, c) == game["player"]:
                ret_level[r][c].append("player")
    return ret_level


def equal_states(game_one, game_two):
    '''
    Input:
    two game states

    Returns:
    a boolean that is True if both game states are the same and false if 
    the game states are not.
    '''
    return game_one["size"] == game_two["size"] and game_one["player"] == game_two["player"] and game_one["targets"] == game_two["targets"] and game_one["computers"] == game_two["computers"] and game_one["walls"] == game_two["walls"]


def get_neighboring_states(game):
    '''
    Input:
    a game state

    Returns:
    a list of possible game states that could result from moving the player
    up, fight, down, or left.
    '''
    ret_states = []
    step_up = step_game(game, "up")
    if not equal_states(step_up, game):
        ret_states.append((step_up, "up"))

    step_right = step_game(game, "right")
    if not equal_states(step_right, game):
        ret_states.append((step_right, "right"))

    step_down = step_game(game, "down")
    if not equal_states(step_down, game):
        ret_states.append((step_down, "down"))

    step_left = step_game(game, "left")
    if not equal_states(step_left, game):
        ret_states.append((step_left, "left"))

    return ret_states


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    if victory_check(game):
        return []
    visited = {(tuple(game["player"]), tuple(game["computers"]))}
    possible_state_paths = [[game]]
    direction_paths = [[]]
    while direction_paths:
        current_path = possible_state_paths.pop(0)
        direct_path = direction_paths.pop(0)
        neighbors = get_neighboring_states(current_path[len(current_path) - 1])
        for state, direction in neighbors:
            if (tuple(state["player"]), tuple(state["computers"])) not in visited and not victory_check(state):
                possible_state_paths.append(
                    current_path + [state])
                direction_paths.append(direct_path + [direction])
                visited.add((tuple(state["player"]),
                            tuple(state["computers"])))
            elif victory_check(state):
                return direct_path + [direction]
    return None


if __name__ == "__main__":
    pass
