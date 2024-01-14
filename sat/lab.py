"""
6.101 Lab 8:
SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def update_formula(formula, assign):
    """
    Given a formla and a list of tuples of variables we'd like to
    define the state of, returns a simplified formula with the given
    values omitted.
    """
    output = []
    for clause in formula:
        output.append(clause.copy())
        for variable in clause:
            if variable[0] == assign[0]:
                if assign[1] == variable[1]:
                    output.pop()
                    break
                else:
                    output[-1].remove(variable)

    return output


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    """
    test_form = formula
    for clause in test_form:
        if len(clause) == 1:
            test_form = update_formula(test_form, clause[0])
            test_out = satisfying_assignment(test_form)
            if test_out is not None:
                return {clause[0][0]: clause[0][1]} | test_out
            else:
                return None

    if not test_form:
        return {}
    if [] in test_form:
        return None

    variable = test_form[0][0][0]
    assign = (variable, True)
    true_form = update_formula(test_form, assign)
    true_out = satisfying_assignment(true_form)
    if true_out is not None:
        return {variable: True} | true_out

    assign = (variable, False)
    false_form = update_formula(test_form, assign)
    false_out = satisfying_assignment(false_form)
    if false_out is not None:
        return {variable: False} | false_out

    return None


def single_cell_at_least_one(board):
    """
    Given a board state, returns a CNF that checks if there is at least
    one value in each cell.
    """
    cnf = []
    row_num = len(board)
    col_num = len(board[0])
    n = len(board)
    # check at least one in cell
    for row in range(row_num):
        for col in range(col_num):
            cnf.append([])
            for vp in range(1, n+1):
                cnf[-1].append([(row, col, vp), True])

    return cnf


def single_cell_at_most_one(board):
    """
    Given a board state, returns a CNF that checks if there is at most
    one value in each cell.
    """
    cnf = []
    row_num = len(board)
    col_num = len(board[0])
    for row in range(row_num):
        for col in range(col_num):
            for v in range(1, row_num + 1):
                for vp in range(v + 1, row_num + 1):
                    cnf.append([])
                    cnf[-1].append([(row, col, v), False])
                    cnf[-1].append([(row, col, vp), False])
    return cnf


def check_row(board):
    """
    Given a board state, returns a cnf that checks if there is
    every number in a single row
    """
    cnf = []
    row_num = len(board)
    col_num = len(board[0])
    for row in range(row_num):
        for v in range(1, row_num + 1):
            cnf.append([])
            for col in range(col_num):
                cnf[-1].append([(row, col, v), True])
            for col in range(col_num):
                for rowp in range(row + 1, row_num + 1):
                    cnf.append([])
                    cnf[-1].append([(row, col, v), False])
                    cnf[-1].append([(rowp, col, v), False])
    print(cnf)
    return cnf


def check_col(board):
    """
    Given a board state, returns a cnf that checks if there is
    every number in a single column
    """
    cnf = []
    row_num = len(board)
    col_num = len(board[0])
    for col in range(col_num):
        for v in range(1, row_num + 1):
            cnf.append([])
            for row in range(row_num):
                cnf[-1].append([(row, col, v), True])
            for row in range(row_num):
                for colp in range(col + 1, col_num + 1):
                    cnf.append([])
                    cnf[-1].append([(row, col, v), False])
                    cnf[-1].append([(row, colp, v), False])
    return cnf


def check_box(board):
    cnf = []
    row_num = int(len(board) ** (1/2))
    col_num = int(len(board[0]) ** (1/2))
    n = len(board)

    for row in range(row_num):
        for col in range(col_num):
            for v in range(1, n + 1):
                cnf.append([])
                for row2 in range(row*row_num, (row + 1)*row_num):
                    for col2 in range(col*col_num, (col + 1)*col_num):
                        cnf[-1].append([(row2, col2, v), True])
    # print(cnf)
    return cnf


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    state: [(c,r,v), True/False]
    """
    cnf_formula = []
    cnf_formula.extend(single_cell_at_least_one(sudoku_board))
    cnf_formula.extend(single_cell_at_most_one(sudoku_board))
    cnf_formula.extend(check_row(sudoku_board))
    cnf_formula.extend(check_col(sudoku_board))
    cnf_formula.extend(check_box(sudoku_board))

    assign = []
    for r in range(len(sudoku_board)):
        for c in range(len(sudoku_board[0])):
            if sudoku_board[r][c] != 0:
                assign.append([[(r, c, sudoku_board[r][c]), True]])
    cnf_formula.extend(assign)

    return cnf_formula


def empty_2d(n):
    """
    Given a value n, creates a square 2d list of dimensions (n,n)
    that is full of 0s
    """
    ret = []
    for i in range(n):
        ret.append([])
        for j in range(n):
            ret[-1].append(0)

    return ret


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    if assignments is None:
        return None

    output = empty_2d(n)
    for key in assignments:
        if assignments[key] is True:
            output[key[0]][key[1]] = key[2]

    return output


if __name__ == "__main__":
    pass
