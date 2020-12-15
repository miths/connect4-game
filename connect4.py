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
    while(r < rowCount and count < 4 and board[r][c] == piece):
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
    while(c < colCount and count < 4 and board[r][c] == piece):
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
    while(c < colCount and r < rowCount and count < 4 and board[r][c] == piece):
        c += 1
        r += 1
        count += 1

    if (count == 4):
        return True

    # checking for diagonal2
    r = row
    c = col
    count = 0
    while(c >= 0 and r < rowCount and count < 4 and board[r][c] == piece):
        c -= 1
        r += 1
        count += 1

    r = row
    c = col
    count -= 1
    while(c < colCount and r >= 0 and count < 4 and board[r][c] == piece):
        c += 1
        r -= 1
        count += 1

    if (count == 4):
        return True
    pass


def draw_board(board):
    # print(board)
    board = np.flip(board, 0)
    # print(board)
    for c in range(colCount):
        for r in range(rowCount):
            pygame.draw.rect(screen, blue, (c*sqSize, r *
                                            sqSize + sqSize, sqSize, sqSize))
            if (board[r][c] == 0):
                pygame.draw.circle(screen, black, (int(
                    c*sqSize+sqSize/2), int(r * sqSize + sqSize+sqSize/2)), radius)
            elif (board[r][c] == 1):
                pygame.draw.circle(screen, red, (int(
                    c*sqSize+sqSize/2), int(r * sqSize + sqSize+sqSize/2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (int(
                    c*sqSize+sqSize/2), int(r * sqSize + sqSize+sqSize/2)), radius)


board = create_board()
game_over = False
turn = 0
print_board(board)

pygame.init()

sqSize = 100

width = colCount * sqSize
height = (rowCount+1) * sqSize

size = (width, height)

radius = int(sqSize/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, sqSize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(sqSize/2)), radius)
            else:
                pygame.draw.circle(
                    screen, yellow, (posx, int(sqSize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, sqSize))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/sqSize))

                if is_valid_loc(board, col):
                    row = get_next_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1, row, col):
                        # draw_board(board)
                        label = myfont.render("Player 1 wins!!", 1, red)
                        screen.blit(label, (20, 10))
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/sqSize))

                if is_valid_loc(board, col):
                    row = get_next_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2, row, col):
                        # draw_board(board)
                        label = myfont.render("Player 2 wins!!", 1, yellow)
                        screen.blit(label, (20, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            pygame.display.update()

            turn += 1
            turn %= 2

            if game_over:
                pygame.time.wait(5000)

    # if turn == 0:
    #     col = int(input("player 1 make your selection: "))
    # else:
    #     col = int(input("player 2 make your selection: "))
    # if is_valid_loc(board, col):
    #     row = get_next_row(board, col)
    #     board = drop_piece(board, row, col, turn+1)
    #     if (winning_move(board, turn+1, row, col)):
    #         game_over = True
    #         print("\n player ", turn+1, " wins \n")
    # turn += 1
    # turn = turn % 2
    # print_board(board)
