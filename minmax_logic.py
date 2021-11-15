import sys
import numpy as np
from connect4_controller import *
# Author: Karl Emil, Simon Søborg, Kristoffer Baumgarten

# denne scorestone er hvad leafnode returner for vi ved hvilken "gren" vi skal tag under vores minMax-algoritme
SCORE_STONES = 22
ROW_COUNT = 6
COLUMN_COUNT = 7

# ----------------------------------- MinMax algoritme -----------------------------------
# vi vil gerne return vores move (hvilket column stenen skal sættes) og værdieren er moven(så vi ved den move, er den som giver mest)

# Her kan vi tæller spillerne sten på banen.


def count_turns_stone(board, turns):
    turns_score = 0

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if(turns+1 == board[r][c]):
                turns_score += 1
    return turns_score


# Redigeret version af Keith Galli til en temp_drop
def temp_drop_piece(temp_board, row, col, piece):
    temp_board[row][col] = piece


def returnMoves(board, turn, c):

    list_moves = []
    temp_board = np.array(board)

    row = get_next_open_row(temp_board, c)
    temp_drop_piece(temp_board, row, c, turn+1)
    list_moves.append(temp_board)

    return list_moves


# her er et tjek for, hvis spillet skulle blive uafgjord
def is_a_draw(board):
    for c in range(COLUMN_COUNT):
        if(is_valid_location(board, c)):
            return False
    return True

# vores minMax skal returnere den bedste column for det givende move den skal lægge i.


def minMax(board, stone_count_AI, stone_count_player, boolTurnAI):

    currentBoard = np.array(board)
    # Hvis det skulle ende i en draw - sætter den forrest da den måske kunne komme out of bounds hvis den køre til slut
    if(is_a_draw(currentBoard)):
        return (None, 0)

    # hvis AI kan vinde 22 - sten (giver plus i return)
    if(winning_move(currentBoard, 2)):
        return (None, (SCORE_STONES - stone_count_AI))

    # hvis Spilleren kan vinde sten - 22 (giver minus i return)
    if(winning_move(currentBoard, 1)):
        return (None, (stone_count_player - SCORE_STONES))

    # for den givende state minmax er på, skal den lave en liste med alle de mulige seperate moves.
    list_of_minMax_board_moves = []
    column_move = []
    temp_list = []

    # isMax for AI - Men at vi også ved at det er AI's tur isMax == AITurn
    if(boolTurnAI):
        boolTurnAI = False
        currentBestCol = 0
        # AI
        for c in range(COLUMN_COUNT):
            if(is_valid_location(currentBoard, c)):
                column_move.append(c)
                temp_list.append(
                    returnMoves(currentBoard, 1, c))
        list_of_minMax_board_moves = np.array(temp_list)

        # currentMaxVal = -∞
        currentMaxVal = -sys.maxsize-1
        while(len(list_of_minMax_board_moves) != 0):
            bestCol, maxVal = minMax(
                list_of_minMax_board_moves, stone_count_AI+1, stone_count_player, boolTurnAI)

            if(maxVal > currentMaxVal):
                currentMaxVal = maxVal
                currentBestCol = bestCol
            column_move.pop(0)
        return (currentBestCol, currentMaxVal)

    # Husk ændre under.......................................
    else:
        boolTurnAI = True
        currentMinCol = 0
        # Player
        for c in range(COLUMN_COUNT):
            if(is_valid_location(currentBoard, c)):
                column_move.append(c)
                temp_list = []
                temp_list.append(
                    returnMoves(currentBoard, 0, c)
                )
                list_of_minMax_board_moves.append(temp_list)

        # currentMinVal = ∞
        currentMinVal: sys.maxsize
        while(not list_of_minMax_board_moves):
            minCol, minVal = minMax(
                list_of_minMax_board_moves, stone_count_AI, stone_count_player+1, boolTurnAI)

            if(minVal < currentMinVal):
                currentMinVal = minVal
                currentMinCol = minCol
            column_move.pop(0)
        return (currentMinCol, currentMinVal)
