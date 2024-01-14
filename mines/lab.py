"""
6.101 Lab 7:
Six Double-Oh Mines
"""
#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION

def check_neighbors(board, row, col):
    """
    Given a 2D array, calculates how many mines are neighboring every point
    on the board.
    """
    if board[row][col] == ".":
        return None

    start_row = row - 1
    end_row = row + 2
    start_col = col - 1
    end_col = col + 2

    if row == 0:
        start_row = row
    if row == len(board) - 1:
        end_row = row + 1
    if col == 0:
        start_col = col
    if col == len(board[0]) - 1:
        end_col = col + 1

    mines = 0
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] == ".":
                mines += 1

    return mines


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((nrows, ncolumns), mines)


def all_neighbors(board, row, col):
    """
    Given a 2D array, calculates how many mines are neighboring every point
    on the board.
    """
    if board[row][col] == ".":
        return None

    start_row = row - 1
    end_row = row + 2
    start_col = col - 1
    end_col = col + 2

    if row == 0:
        start_row = row
    if row == len(board) - 1:
        end_row = row + 1
    if col == 0:
        start_col = col
    if col == len(board[0]) - 1:
        end_col = col + 1

    neighbors = []
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if r != row or c != col:
                neighbors.append((r, c))

    return neighbors


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'dig': 4}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing',
    ...         'dig': 4}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    return dig_nd(game, (row, col))


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, all_visible)


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    output = ""
    locations_list = render_2d_locations(game, all_visible)
    for r in range(len(locations_list)):
        for c in range(len(locations_list[0])):
            output += locations_list[r][c]
        if r != len(locations_list) - 1:
            output += "\n"
    return output


# N-D IMPLEMENTATION

def nd_empty(dimension, fill_value):
    """
    returns n-dimensional list filled with a certain value
    """
    if not dimension:
        return fill_value
    return [nd_empty(dimension[1:], fill_value) for i in range(dimension[0])]


def get_val(board, point):
    """
    returns value at point
    """
    if len(point) > 1:
        return get_val(board[point[0]], point[1:])
    return board[point[-1]]


def set_val(board, point, value):
    """
    """
    if len(point) > 1:
        set_val(board[point[0]], point[1:], value)
    else:
        board[point[0]] = value


def find_neighbors(dimensions, point):
    """
    Given dimensions of a board and a point on the board, returns a list of 
    neighboring point coordinates.
    """
    if len(point) == 1:
        # print("d,p", dimensions, point)
        # print(dimensions[0])
        checks = []
        start = -1
        end = 1
        if point[0] == 0:
            start = 0
        if point[0] == dimensions[0] - 1:
            end = 0
        for i in range(start, end + 1):
            checks.append((point[0] + i, ))
        return checks

    first = find_neighbors([dimensions[0]], (point[0],))
    rest = find_neighbors(dimensions[1:], point[1:])

    neighbors = []

    for val in first:
        for val2 in rest:
            neighbors.append(val + val2)

    return neighbors


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    board = nd_empty(dimensions, 0)
    visible = nd_empty(dimensions, False)
    for mine in mines:
        lst = []
        iter = 0
        for i in range(len(mine) - 1):
            if iter == 0:
                lst = board[mine[i]]
            else:
                lst = lst[mine[i]]
            iter += 1
        lst[mine[-1]] = "."

    for mine in mines:
        neighbors = find_neighbors(dimensions, mine)
        for neighbor in neighbors:
            val = get_val(board, neighbor)
            if val != ".":
                set_val(board, neighbor, val + 1)
    dig = dimensions[0]
    for i in range(1, len(dimensions)):
        dig *= dimensions[i]

    dig -= len(mines)

    return {
        "dimensions": dimensions,
        "board": board,
        "visible": visible,
        "state": "ongoing",
        "dig": dig,
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'dig': 13}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'dig': 13}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    revealed = 0
    board_val = get_val(game["board"], coordinates)
    vis_val = get_val(game["visible"], coordinates)

    if game["state"] == "defeat" or game["state"] == "victory" or vis_val is True:
        return revealed

    if board_val == ".":
        set_val(game["visible"], coordinates, True)
        game["state"] = "defeat"
        return 1

    set_val(game["visible"], coordinates, True)
    game["dig"] -= 1
    revealed = 1

    if board_val == 0:
        neighbors = find_neighbors(game["dimensions"], coordinates)
        for point in neighbors:
            if get_val(game["board"], point) != "." and get_val(game["visible"], point) is False:
                revealed += dig_nd(game, point)

    if game["dig"] == 0:
        game["state"] = "victory"
        return revealed
    else:
        game["state"] = "ongoing"
        return revealed


def find_all_points(dimensions):
    """
    Given a board, returns a list of all values in the board
    """
    if len(dimensions) == 1:
        checks = []
        end = dimensions[0]
        for i in range(end):
            checks.append((i, ))
        return checks

    first = find_all_points([dimensions[0]])
    rest = find_all_points(dimensions[1:])

    points = []

    for val in first:
        for val2 in rest:
            points.append(val + val2)

    return points


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    out_board = nd_empty(game["dimensions"], " ")
    coordinates = find_all_points(game["dimensions"])
    for point in coordinates:
        value_board = get_val(game["board"], point)
        value_vis = get_val(game["visible"], point)
        if value_vis is True or all_visible:
            if value_board != 0:
                set_val(out_board, point, str(value_board))
        else:
            set_val(out_board, point, "_")

    return out_board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
