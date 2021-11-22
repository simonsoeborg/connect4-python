# Author: Keith Galli
# Githun: https://github.com/KeithGalli/Connect4-Python

import numpy as np
import pygame
import sys
import math
from connect4_controller import *
from minmax_logic import *

BLUE = (0, 102, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def print_board(board):
    print(np.flip(board, 0))


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                                            SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

#turn = random.randint(0, 1)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            # print(event.pos)

            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            # # Ask for AI Input
        if turn == 1 and not game_over:
            # posx = event.pos[0]
            # col = int(math.floor(posx/SQUARESIZE)
            boolTurnAI = True
            minmax_board = board.copy()

            # vi vil gemme den column vi vil lægge i
            # <---------------------------------------(Her kaldes algoritmen)
            col, bestscore = minMax(
                minmax_board, boolTurnAI, 5)

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

        if game_over:
            pygame.time.wait(6000)
