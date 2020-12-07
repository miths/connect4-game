import numpy as np
import pygame
import sys   # for what?
import math

blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

rowCount = 6
colCount = 7


def create_board():
    board = np.zeros((rowCount, colCount))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board


def is_valid_loc(board, col):
    return board[rowCount-1][col] == 0


def get_next_row(board, col):
    for row in range(rowCount):
        if board[row][col] == 0:
            return row
    return -1


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece, row, col):
    # checking for vertical
    r = row
    c = col
    count = 0
    while(r >= 0 and count < 4 and board[r][c] == piece):
        r -= 1
        count += 1

    r = row
    c = col
    count -= 1
    while(r <= rowCount and count < 4 and board[r][c] == piece):
        r += 1
        count += 1
    print(count)
    if (count == 4):
        return True

    # checking for horizontal
    r = row
    c = col
    count = 0
    while(c >= 0 and count < 4 and board[r][c] == piece):
        c -= 1
        count += 1

    r = row
    c = col
    count -= 1
    while(c <= colCount and count < 4 and board[r][c] == piece):
        c += 1
        count += 1

    if (count == 4):
        return True

    # checking for diagonal1
    r = row
    c = col
    count = 0
    while(c >= 0 and r >= 0 and count < 4 and board[r][c] == piece):
        c -= 1
        r -= 1
        count += 1

    r = row
    c = col
    count -= 1
    while(c <= colCount and r <= rowCount and count < 4 and board[r][c] == piece):
        c += 1
        r += 1
        count += 1

    if (count == 4):
        return True

    # checking for diagonal2
    r = row
    c = col
    count = 0
    while(c >= 0 and r <= rowCount and count < 4 and board[r][c] == piece):
        c -= 1
        r += 1
        count += 1

    r = row
    c = col
    count -= 1
    while(c <= colCount and r >= 0 and count < 4 and board[r][c] == piece):
        c += 1
        r -= 1
        count += 1

    if (count == 4):
        return True
    pass


def draw_board(board):
    for c in range(colCount):
        for r in range(rowCount):
            pygame.draw.rect(screen, blue, (c*2))


board = create_board()
game_over = False
turn = 0
print(board)
while not game_over:
    if turn == 0:
        col = int(input("player 1 make your selection: "))
    else:
        col = int(input("player 2 make your selection: "))
    if is_valid_loc(board, col):
        row = get_next_row(board, col)
        board = drop_piece(board, row, col, turn+1)
        if (winning_move(board, turn+1, row, col)):
            game_over = True
            print("\n player ", turn+1, " wins \n")
    turn += 1
    turn = turn % 2
    print_board(board)
