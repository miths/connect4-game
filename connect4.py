import numpy as np
import pygame
import sys   # for what?
import math
import random

blue = (117, 148, 124)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

rowCount = 6
colCount = 7

playerTurn = 0
aiTurn = 1

empty = 0
playerPiece = 1
aiPiece = 2

windowLen = 4


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
    # print(count)
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
    # pass


def evaluate_window(window, piece):
    score = 0
    opp_piece = playerPiece
    if piece == playerPiece:
        opp_piece = aiPiece
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 15
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(empty) == 1:
        score -= 14
    return score


def score_pos(board, piece):
    score = 0

    # score center column
    center_array = [int(i) for i in list(board[:, colCount//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # horizontal score
    for r in range(rowCount):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(colCount-(windowLen-1)):
            window = row_array[c:c+windowLen]
            score += evaluate_window(window, piece)+rowCount-r
    # +ive diag score
    for r in range(rowCount - (windowLen-1)):
        for c in range(colCount - (windowLen-1)):
            window = [board[r+i][c+i] for i in range(windowLen)]
            score += evaluate_window(window, piece)
    # -ve slope diag
    for r in range(rowCount - (windowLen-1)):
        for c in range(colCount - (windowLen-1)):
            window = [board[r+(windowLen-1)-i][c+i] for i in range(windowLen)]
            score += evaluate_window(window, piece)

    # vertival score
    for c in range(colCount):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rowCount - (windowLen-1)):
            window = col_array[r:r+windowLen]
            score += evaluate_window(window, piece)+colCount
    return score


def get_valid_locations(board):
    valid_loc = []
    for col in range(colCount):
        if is_valid_loc(board, col):
            valid_loc.append(col)
    return valid_loc


def is_terminal_node(board, row, col):
    return winning_move(board, playerPiece, row, col) or winning_move(board, aiPiece, row, col) or len(get_valid_locations(board)) == 0


def pick_best_move(board, piece):
    valid_loc = get_valid_locations(board)
    best_score = -math.inf
    best_col = random.choice(valid_loc)
    for col in valid_loc:
        row = get_next_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def minmax(board, depth, alpha, beta, maxPlayer, r, c):
    valid_loc = get_valid_locations(board)
    # print(valid_loc)
    if (r == -1 and c == -1):
        is_terminal = False
        # for c in valid_loc:
        #     r = get_next_row(board, c)
        #     is_terminal = is_terminal_node(board, r, c)
        #     # print(r, c, is_terminal)
        #     if (is_terminal):
        #         if winning_move(board, aiPiece, r, c):
        #             return (None, 10000000000)
        #         elif winning_move(board, playerPiece, r, c):
        #             print("danger!!!!!!!!")
        #             return (None, -10000000000)
        #         else:  # no valid moves, game over
        #             return (None, 0)

    else:
        is_terminal = is_terminal_node(board, r, c)
        if (is_terminal):
            if winning_move(board, aiPiece, r, c):
                # print_board(board)
                return (None, 10000000000)
            elif winning_move(board, playerPiece, r, c):
                print("danger!!!!!!!!")
                return (None, -10000000000)
            else:  # no valid moves, game over
                return (None, 0)

    if depth == 0:
        return (None, score_pos(board, aiPiece))

    # if (row != -1 and col != -1):
    #     is_terminal = is_terminal_node(board, row, col)
    # else:
    #     is_terminal = False
    # if depth == 0 or is_terminal:
    #     if is_terminal:
    #         if winning_move(board, aiPiece, row, col):
    #             return (None, 10000000000)
    #         elif winning_move(board, playerPiece, row, col, ):
    #             return (None, -10000000000)
    #         else:  # no valid moves, game over
    #             return (None, 0)
    #     else:   # depth == 0, return score
    #         return (None, score_pos(board, aiPiece))

    if maxPlayer:    # for aiPiece i.e. maximizing player
        value = -math.inf
        column = random.choice(valid_loc)
        for col in valid_loc:
            row = get_next_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col,  aiPiece)
            new_score = minmax(b_copy, depth-1, alpha,
                               beta, False, row, col)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # minimizing player
        value = math.inf
        column = random.choice(valid_loc)
        for col in valid_loc:
            row = get_next_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col,  playerPiece)
            new_score = minmax(b_copy, depth-1, alpha, beta, True, row, col)[1]
            if new_score < value:
                value = new_score
                column = col
            alpha = min(alpha, value)
            if alpha >= beta:
                break
        return column, value


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
# turn = 0
turn = random.randint(playerTurn, aiTurn)
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
            if turn == playerTurn:
                pygame.draw.circle(screen, red, (posx, int(sqSize/2)), radius)
            # else:
            #     pygame.draw.circle(
            #         screen, yellow, (posx, int(sqSize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == playerTurn:
            pygame.draw.rect(screen, black, (0, 0, width, sqSize))
            if turn == playerTurn:
                posx = event.pos[0]
                col = int(math.floor(posx/sqSize))

                if is_valid_loc(board, col):
                    row = get_next_row(board, col)
                    drop_piece(board, row, col, playerPiece)

                    if winning_move(board, playerPiece, row, col):
                        # draw_board(board)
                        label = myfont.render("Player 1 wins!!", 1, red)
                        screen.blit(label, (20, 10))
                        game_over = True

                    turn += 1
                    turn %= 2
                    print_board(board)
                    draw_board(board)
                    pygame.display.update()
            # else:
            #     posx = event.pos[0]
            #     col = int(math.floor(posx/sqSize))

            #     if is_valid_loc(board, col):
            #         row = get_next_row(board, col)
            #         drop_piece(board, row, col, 2)

            #         if winning_move(board, 2, row, col):
            #             # draw_board(board)
            #             label = myfont.render("Player 2 wins!!", 1, yellow)
            #             screen.blit(label, (20, 10))
            #             game_over = True

        if turn == aiTurn and not game_over:

            col, minmax_score = minmax(
                board, 5, -math.inf, math.inf, True, -1, -1)
            print(minmax_score)
            if is_valid_loc(board, col):
                row = get_next_row(board, col)
                drop_piece(board, row, col, aiPiece)
                if winning_move(board, aiPiece, row, col):
                    # draw_board(board)
                    label = myfont.render("AI wins!!", 1, red)
                    screen.blit(label, (50, 10))
                    game_over = True

                turn += 1
                turn %= 2
                print_board(board)
                draw_board(board)
                pygame.display.update()

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
