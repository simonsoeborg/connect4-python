import sys
import random
import math
from pygame import register_quit
from connect4_controller import *
# Author: Karl Emil, Simon Søborg, Kristoffer Baumgarten

# denne scorestone er hvad leafnode returner for vi ved hvilken "gren" vi skal tag under vores minMax-algoritme
SCORE_STONES = 22
ROW_COUNT = 6
COLUMN_COUNT = 7
# vi vil gerne return vores move (hvilket column stenen skal sættes) og værdieren er moven(så vi ved den move, er den som giver mest)

# Her kan vi tæller spillerne sten på banen.


def count_turns_stone(temp_board, turns):
    turns_score = 0

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if(turns+1 == temp_board[r][c]):
                turns_score += 1
    return turns_score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# her er et tjek for, hvis spillet skulle blive uafgjord

def is_a_draw(board):
    for c in range(COLUMN_COUNT):
        if(is_valid_location(board, c)):
            return False
    return True


# Metode til at evaluere gamestate

def calc_score(board, bool_turn_AI):
    score = 0
    piece = 1
    line = []

    if(not bool_turn_AI):
        piece = 2

    # Det der er smart ved at definere en høj værdi for mid column. Er at den vil altid prior mid rækken på første move
    # Da den vil return højest point i mid column
    for r in range(ROW_COUNT):
        if(piece == board[r][3]):
            score += 1
    # for at AI ved det er smartest at lægge i midten
    score = score * 3

    # Check points vertical locations
    for c in range(COLUMN_COUNT):
        line.clear()
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                line.append(board[r][c])
                score += line.count(piece)
            elif (r < ROW_COUNT-1 and slice(board[r][c], board[r+1][c]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 2
            elif (r < ROW_COUNT-2 and slice(board[r][c], board[r+2][c]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 3

    # Check points horizontal locations
    for r in range(ROW_COUNT):
        line.clear()
        for c in range(COLUMN_COUNT):
            if (board[r][c] == piece):
                line.append(board[r][c])
                score += line.count(piece)
            elif (c < COLUMN_COUNT-1 and slice(board[r][c], board[r][c+1]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 2
            elif (c < COLUMN_COUNT-2 and slice(board[r][c], board[r][c+2]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 3

    # TODO: Check points diagonal locations
    for c in range(COLUMN_COUNT - 3):
        line.clear()

    return score

    # --------------------------------------------- MinMax algo ---------------------------------------------

    # vores minMax skal returnere den bedste column for det givende move den skal lægge i.


def minMax(minmax_board, bool_turn_AI, depth):
    currentBoard = minmax_board.copy()

    # Hvis AI vinder på en leaf
    if(winning_move(currentBoard, 2)):
        return (None, (10000000000000000))

    # hvis Spilleren vinder på en leaf
    if(winning_move(currentBoard, 1)):

        return (None, (-10000000000000000))

    # Hvis det skulle ende i en draw - sætter den forrest da den måske kunne komme out of bounds hvis den køre til slut
    if(is_a_draw(currentBoard)):
        return (None, 0)

    # når vi stopper den på en dybde
    if (depth == 0):
        return (None, calc_score(currentBoard, bool_turn_AI))

    # for den givende state minmax er på, skal den lave en liste med alle de mulige seperate moves.
    column_move = []
    # isMax for AI - Men at vi også ved at det er AI's tur isMax == AITurn
    if(bool_turn_AI):
        bool_turn_AI = False
        # AI # currentMaxVal = -∞
        currentMaxVal = -math.inf
        column_move = get_valid_locations(currentBoard)
        # random.shuffle(column_move)
        for c in column_move:

            r = get_next_open_row(currentBoard, c)
            newBoard = currentBoard.copy()
            # For each Column -> Calc score for each valid location -> Return highest / lowest Score, and best location board[c][r]
            # Create new Board -> Drop piece -> Run MinMax on new Board
            drop_piece(newBoard, r, c, 2)
            bestCol, maxVal = minMax(newBoard, bool_turn_AI, depth-1)

            if(maxVal > currentMaxVal):
                currentMaxVal = maxVal
                currentBestCol = c
                print("AI!: dette er maxVal : " + str(maxVal) + " for column: " +
                      str(c) + " og currentVal er: " + str(currentMaxVal))

        print("AI!: this is the best value: " + str(currentMaxVal) +
              " this is the best Col: " + str(currentBestCol))
        return (currentBestCol, currentMaxVal)

    else:  # _______________________________________min_max_player__________________________________________
        bool_turn_AI = True

        # Player # currentMinVal = ∞
        currentMinVal = math.inf

        column_move = get_valid_locations(currentBoard)
        for c in column_move:
            r = get_next_open_row(currentBoard, c)
            newBoard = currentBoard.copy()
            drop_piece(newBoard, r, c, 1)
            minCol, minVal = minMax(newBoard, bool_turn_AI, depth-1)

            if(minVal < currentMinVal):
                currentMinVal = minVal
                currentMinCol = c
                print("Spiller!: dette er maxVal : " + str(minVal) + " for column: " +
                      str(c) + " og currentVal er: " + str(currentMinVal))

        print("Spiller!: this is the best value: " + str(currentMinVal) +
              " this is the best Col: " + str(currentMinCol))
        return (currentMinCol, currentMinVal)
