#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Anthony Saieva (Narin) an2804
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

# global dictionary for values and boards
board_values = {}

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    for_count = 0
    against_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == color:
                for_count += 1
            elif board[i][j] != color and board[i][j] != 0:
                against_count += 1
    return for_count-against_count


############ MINIMAX ###############################

def switch_color(color):
    '''switches the color'''
    if color != 1 and color != 2:
        raise Exception("Invalid Color")

    if color == 1:
        return 2
    return 1

def is_leaf_node(board, color):
    '''Determines end state if no legal moves left for color on board'''
    if get_possible_moves(board, color):
        return False
    return True

def minimax_min_node(board, color):
    '''returns the value of the min node'''
    opponent = switch_color(color)
    min_val = 1000

    if is_leaf_node(board, opponent):
        if board not in board_values:
            board_values[board] = compute_utility(board, color)
        return board_values[board]

    # if not a leaf node compute minimum of children's maximum
    moves = get_possible_moves(board, opponent)
    successors = []
    #play the moves and get the states
    map(lambda x: successors.append(play_move(board, opponent, x[0], x[1])), moves)
    successors.sort(key=lambda x: compute_utility(x, color))

    for successor in successors:
        if successor not in board_values:
            board_values[successor] = minimax_max_node(successor, color)
        val = board_values[successor]

        min_val = min(min_val, val)

    return min_val

def minimax_max_node(board, color):
    '''returns the value of the node'''
    max_val = -1000

    if is_leaf_node(board, color):
        if board not in board_values:
            board_values[board] = compute_utility(board, color)
        return board_values[board]


    # if not a leaf node. Need to compute the maximum of the mimimum of the children nodes
    moves = get_possible_moves(board, color)
    successors = []

    map(lambda x: successors.append(play_move(board, color, x[0], x[1])), moves)
    successors.sort(key=lambda x: compute_utility(x, color), reverse=True)

    for successor in successors:
        if successor not in board_values:
            board_values[successor] = minimax_min_node(successor, color)
        val = board_values[successor]
        max_val = max(max_val, val)

    return max_val

def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    if is_leaf_node(board, color):
        raise Exception("No legal moves allowed")
    else:
        moves = get_possible_moves(board, color)
        successors_moves = {}

        for move in moves:
            successors_moves[play_move(board, color, move[0], move[1])] = move
        sorted_successors = sorted(successors_moves.keys(), key=lambda x: compute_utility(x, color), reverse=True)
        max_val = -1000
        max_move = ()
        for successor in sorted_successors:
            # successor = play_move(board, color, move[0], move[1])
            val = minimax_min_node(successor, color)
            if val > max_val:
                max_val = val
                max_move = successors_moves[successor]

    return max_move


############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    '''returns the value of the min node'''
    opponent = switch_color(color)
    min_val = 1000

    if is_leaf_node(board, opponent) or level == limit:
        if board not in board_values:
            board_values[board] = compute_utility(board, color)
        return board_values[board]

    # if not a leaf node compute minimum of children's maximum
    moves = get_possible_moves(board, opponent)

    successors = []
    #play the moves and get the states
    map(lambda x: successors.append(play_move(board, opponent, x[0], x[1])), moves)
    successors.sort(key=lambda x: compute_utility(x, color))

    for successor in successors:
        # successor = play_move(board, opponent, move[0], move[1])
        if successor not in board_values:
            board_values[successor] = alphabeta_max_node(successor, color, alpha, beta, level+1, limit)
        val = board_values[successor]

        min_val = min(min_val, val)
        if min_val <= alpha:
            return min_val
        beta = min(beta, min_val)

    return min_val


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    '''returns the value of the node'''
    max_val = -1000

    if is_leaf_node(board, opponent) or level==limit:
        if board not in board_values:
            board_values[board] = compute_utility(board, color)
        return board_values[board]

    # if not a leaf node. Need to compute the maximum of the mimimum of the children nodes
    moves = get_possible_moves(board, color)
    successors = []

    map(lambda x: successors.append(play_move(board, color, x[0], x[1])), moves)
    successors.sort(key=lambda x: compute_utility(x, color), reverse=True)

    for successor in successors:
        # successor = play_move(board, color, move[0], move[1])
        if successor not in board_values:
            board_values[successor] = alphabeta_min_node(successor, color, alpha, beta, level+1, limit)
        val = board_values[successor]


        max_val = max(max_val, val)
        if max_val >= beta:
            return max_val
        alpha = max(alpha, max_val)

    return max_val

def select_move_alphabeta(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    if is_leaf_node(board, color):
        raise Exception("No legal moves allowed")
    else:
        alpha = -1000
        beta = 1000
        moves = get_possible_moves(board, color)
        moves = get_possible_moves(board, color)
        successors_moves = {}

        for move in moves:
            successors_moves[play_move(board, color, move[0], move[1])] = move
        sorted_successors = sorted(successors_moves.keys(), key=lambda x: compute_utility(x, color), reverse=True)

        max_val = -1000
        max_move = ()

        for successor in sorted_successors:
            # successor = play_move(board, color, move[0], move[1])
            val = alphabeta_min_node(successor, color, alpha, beta, 0, 16)
            if val > max_val:
                max_val = val
                max_move = successors_moves[successor]

    return max_move



####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            movei, movej = select_move_minimax(board, color)
            # movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
