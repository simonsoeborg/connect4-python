import sys
import random
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
    scores = dict({})
    if(not bool_turn_AI):
        piece = 2

    # Check points horizontal locations
    for r in range(ROW_COUNT):
        line.clear()
        for c in range(COLUMN_COUNT):
            if (board[r][c] == piece):
                line.append(board[r][c])
                score += line.count(piece)
                scores[score] = str(str(r) + "," + str(c))
            elif (c < COLUMN_COUNT-1 and slice(board[r][c], board[r][c+1]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 2
                scores[score] = str(str(r) + "," + str(c))
            elif (c < COLUMN_COUNT-2 and slice(board[r][c], board[r][c+2]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 3
                scores[score] = str(str(r) + "," + str(c))

    # Check points vertical locations
    for c in range(COLUMN_COUNT):
        line.clear()
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                line.append(board[r][c])
                score += line.count(piece)
                scores[score] = str(str(r) + "," + str(c))
            elif (r < ROW_COUNT-1 and slice(board[r][c], board[r+1][c]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 2
                scores[score] = str(str(r) + "," + str(c))
            elif (r < ROW_COUNT-2 and slice(board[r][c], board[r+2][c]) == piece):
                line.append(board[r][c])
                score += line.count(piece) * 3
                scores[score] = str(str(r) + "," + str(c))

    # Check points diagonal locations
    for c in range(COLUMN_COUNT - 3):
        line.clear()

    # Check points negativ slope locations
    #print("player: " + str(piece) + " have the score " + str(score))

    if(piece == 1):
        if(len(scores) > 0):
            print("Best Score: " + str((-1 * max(scores))) +
                  " | Board Piece: " + str(scores[max(scores)]))
    else:
        if(len(scores) > 0):
            print("Best Score: " + str(max(scores)) +
                  " | Board Piece: " + str(scores[max(scores)]))

    if(len(scores) > 0):
        return str(max(scores)) + "|" + str(scores[max(scores)])
    else:
        return None
    # --------------------------------------------- MinMax algo ---------------------------------------------

    # vores minMax skal returnere den bedste column for det givende move den skal lægge i.


def minMax(minmax_board, stone_count_AI, stone_count_player, bool_turn_AI, depth):
    currentBoard = minmax_board.copy()

    # Hvis det skulle ende i en draw - sætter den forrest da den måske kunne komme out of bounds hvis den køre til slut
    if(is_a_draw(currentBoard)):
        return (None, 0)

    # Hvis AI vinder på en leaf
    if(winning_move(currentBoard, 2)):

        return (None, (10000000000000000))

    # hvis Spilleren vinder på en leaf
    if(winning_move(currentBoard, 1)):

        return (None, (-10000000000000000))

    # når vi stopper den på en dybde
    if (depth == 0):
        data = calc_score(currentBoard, bool_turn_AI)
        if(data != None):
            intScore = data.split("|")[0]
            return (None, int(intScore))
        else:
            return (None, 0)
    # for den givende state minmax er på, skal den lave en liste med alle de mulige seperate moves.
    column_move = []
    # isMax for AI - Men at vi også ved at det er AI's tur isMax == AITurn
    if(bool_turn_AI):
        bool_turn_AI = False
        currentBestCol = 0
        # AI # currentMaxVal = -∞

        column_move = get_valid_locations(currentBoard)
        random.shuffle(column_move)
        for c in column_move:

            # [ 0, 0, 0, 0, 0, 0, 0 ]
            # [ 0, 0, 0, 0, 0, 0, 0 ]
            # [ 0, 0, 0, 2, 0, 0, 0 ]
            # [ 1, 0, 0, 1, 1, 2, 0 ]
            # [ 1, 0, 0, 1, 2, 1, 0 ]
            # [ 1, 0, 1, 1, 2, 2, 1 ]

            currentMaxVal = -sys.maxsize-1

            r = get_next_open_row(currentBoard, c)
            newBoard = currentBoard.copy()
            # For each Column -> Calc score for each valid location -> Return highest / lowest Score, and best location board[c][r]
            # Create new Board -> Drop piece -> Run MinMax on new Board
            data = calc_score(newBoard, bool_turn_AI)
            if (data != None):
                placement = data.split("|")[1]
                renderPlacement_to_c = placement.split(",")[1]
                renderPlacement_to_r = placement.split(",")[0]
                print("c: " + str(renderPlacement_to_c))
                print("r: " + str(renderPlacement_to_r))
                drop_piece(newBoard, int(renderPlacement_to_r),
                           int(renderPlacement_to_c), 2)
                bestCol, maxVal = minMax(
                    newBoard, stone_count_AI+1, stone_count_player, bool_turn_AI, depth-1)

                if(maxVal > currentMaxVal):
                    currentMaxVal = maxVal
                    currentBestCol = c
            else:
                drop_piece(newBoard, r, c, 2)
                bestCol, maxVal = minMax(
                    newBoard, stone_count_AI+1, stone_count_player, bool_turn_AI, depth-1)

                if(maxVal > currentMaxVal):
                    currentMaxVal = maxVal
                    currentBestCol = c

        return (currentBestCol, currentMaxVal)

    else:
        # _______________________________________min_max_player__________________________________________

        bool_turn_AI = True

        # Player # currentMinVal = ∞
        currentMinVal = sys.maxsize

        column_move = get_valid_locations(currentBoard)
        random.shuffle(column_move)
        for c in column_move:
            currentMaxVal = -sys.maxsize-1
            r = get_next_open_row(currentBoard, c)
            newBoard = currentBoard.copy()
            drop_piece(newBoard, r, c, 1)
            minCol, minVal = minMax(
                newBoard, stone_count_AI, stone_count_player+1, bool_turn_AI, depth-1)

            if(minVal < currentMinVal):
                currentMinVal = minVal
                currentMinCol = c

        return (currentMinCol, currentMinVal)
