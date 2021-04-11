import numpy as np
import pygame
import sys   # for what?
import math
import random
import time
import pandas as pd

blue = (117, 148, 124)                  # light wood colour
black = (0, 0, 0)                       # black colour
red = (255, 0, 0)                       # red colour
yellow = (255, 255, 0)                  # yellow colour

rowCount = 6                            # total number of rows
colCount = 7                            # total number of column

playerTurn = 0                          # player turn = 0
aiTurn = 1                              # ai turn = 1

empty = 0                               # empty cell, represented by 0 in matrix
playerPiece = 1                         # player Piece in a cell, represented by 1
aiPiece = 2                             # ai piece in a cell, represented by 2

windowLen = 4                           # winning condition


def create_board():                     # create matrix with zeros
    board = np.zeros((rowCount, colCount))
    # board = [[0, 0, 0, 1, 0, 0, 0],
    #          [0, 0, 2, 2, 0, 0, 0],
    #          [0, 0, 1, 2, 0, 0, 0],
    #          [0, 0, 1, 2, 0, 0, 0],
    #          [0, 1, 2, 1, 2, 0, 0],
    #          [0, 2, 1, 2, 1, 0, 0]]
    # board = [[0, 0, 0, 1, 0, 0, 0],
    #          [0, 0, 2, 2, 0, 0, 0],
    #          [0, 0, 1, 2, 1, 1, 0],
    #          [0, 0, 1, 2, 2, 2, 0],
    #          [0, 1, 2, 1, 2, 1, 1],
    #          [1, 2, 1, 1, 1, 2, 2]]
    board = np.flip(board, 0)
    return board


# drop piece on board and returns edited board
def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board


# checks if the location is valid or not
def is_valid_loc(board, col):
    return board[rowCount-1][col] == 0


# get next open row for given column
def get_next_row(board, col):
    for row in range(rowCount):
        if board[row][col] == 0:
            return row
    return -1


# to print board after flipping it
def print_board(board):
    print(np.flip(board, 0))


# check if last performed move was winning move or not
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


def evaluate_window(window, piece):                                 # to score the window
    score = 0
    opp_piece = playerPiece
    if piece == playerPiece:
        opp_piece = aiPiece
    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 15
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(empty) == 1:
        score -= 14
    return score


def score_pos(board, piece):                                        # scores the board
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
            score += evaluate_window(window, piece)
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
            score += evaluate_window(window, piece)
    for r in range(rowCount):
        for c in range(colCount):
            if (board[r][c] == empty and winning_move(board, piece, r, c) and r+1 < rowCount and board[r+1][c] == empty and winning_move(board, piece, r+1, c)):
                score += 100
                print(score)
    return score


def score_pos_mcts(board, piece):                                        # scores the board
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
            score += evaluate_window(window, piece)
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
            score += evaluate_window(window, piece)

    return score


# returns all possible columns to drop piece
def get_valid_locations(board):
    valid_loc = []
    for col in range(colCount):
        if is_valid_loc(board, col):
            valid_loc.append(col)
    return valid_loc


# checks if any more moves are possible or not
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

# returns best column after checking scores


def pick_best_move_mcts(board, piece):
    valid_loc = get_valid_locations(board)
    best_score = -math.inf
    best_col = random.choice(valid_loc)
    for col in valid_loc:
        row = get_next_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_pos_mcts(board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


# minmax function to predict the future and choose move accordingly
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
                return (None, 10000000000+depth)
            elif winning_move(board, playerPiece, r, c):
                # print("danger!!!!!!!!")
                return (None, -10000000000-depth)
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


def winning_move_whole_board(board, piece):
    # Check horizontal locations for win
    for c in range(colCount-3):
        for r in range(rowCount):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(colCount):
        for r in range(rowCount-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(colCount-3):
        for r in range(rowCount-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(colCount-3):
        for r in range(3, rowCount):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False


board = create_board()                          # init. of game and game variable
game_over = False
turn = 1
# turn = random.randint(playerTurn, aiTurn)
print_board(board)

pygame.init()

sqSize = 100

width = colCount * sqSize
height = (rowCount+1) * sqSize

size = (width, height)

radius = int(sqSize/2 - 10)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


class MCTS():
    # init_time = time.time()
    def __init__(self, board, player, tree, prev_board, root):

        self.state = board
        self.prev_state = prev_board
    #   self.config = config
        self.player = player
        self.final_action = None
        self.time_limit = 10
        self.root_node = root
        self.tunable_constant = 10

        if tree != None:
            self.tree = tree
        else:
            self.tree = {self.root_node: {'state': self.state, 'player': 1,
                                          'child': [], 'parent': None, 'total_node_visits': 0,
                                          'total_node_wins': 0}}
        # self.total_parent_node_visits = 0

    def get_action(self):
        for c in range(colCount):
            for r in range(rowCount):
                if self.prev_state[r][c] == 0:
                    if self.state[r][c] != 0:
                        return c
                    break

    def get_ucb(self, node_no):
        # if not self.total_parent_node_visits:
        #     return math.inf
        # else:
        value_estimate = self.tree[node_no]['total_node_wins'] / \
            (self.tree[node_no]['total_node_visits'] + .000001)
        exploration = math.sqrt(2*math.log(self.tree[self.tree[node_no]['parent']]['total_node_visits']) /
                                (self.tree[node_no]['total_node_visits'] + .000001))
        ucb_score = value_estimate + self.tunable_constant * exploration
        # print(ucb_score)
        return ucb_score

    def selection(self):
        '''
        Aim - To select the leaf node with the maximum UCB
        '''
        is_terminal_state = False
        leaf_node_id = self.root_node
        while not is_terminal_state:
            node_id = leaf_node_id
            if node_id == (0, 3, 3, 3, 3, 3, 3):
                print("got child id")
                print(len(self.tree[node_id]['child']))
                number_of_child = len(self.tree[node_id]['child'])
            else:
                number_of_child = len(self.tree[node_id]['child'])
            if not number_of_child:
                leaf_node_id = node_id
                is_terminal_state = True
            else:
                max_ucb_score = -math.inf
                best_action = leaf_node_id
                for i in range(number_of_child):
                    action = self.tree[node_id]['child'][i]
                    child_id = leaf_node_id + (action,)
                    current_ucb = self.get_ucb(child_id)
                    if current_ucb > max_ucb_score:
                        max_ucb_score = current_ucb
                        best_action = action

                leaf_node_id = leaf_node_id + (best_action,)
                # print("leaf in selection", leaf_node_id)
        return leaf_node_id

    def expansion(self, leaf_node_id):
        '''
        Aim - Add new nodes to the current leaf node by taking a random action
              and then take a random or follow any policy to take opponent's action.
        '''
        current_state = self.tree[leaf_node_id]['state']
        player_mark = self.tree[leaf_node_id]['player']
        self.actions_available = get_valid_locations(current_state)
        # if player_mark == 1:
        #     player_mark = 2
        # else:
        #     player_mark = 1
        done = winning_move_whole_board(current_state, player_mark)
        # if (leaf_node_id == (0, 4, 4)):
        #     print(done)
        # child_node_id = leaf_node_id
        is_availaible = False
        # print("axt ", self.actions_available)
        if len(self.actions_available) and not done:
            childs = []
            if player_mark == 1:
                player_mark = 2
            else:
                player_mark = 1
            for action in self.actions_available:
                child_id = leaf_node_id + (action,)
                childs.append(action)
                roww = get_next_row(current_state, action)
                new_board = current_state.copy()
                drop_piece(new_board, roww, action, player_mark)
            #   new_board = put_new_piece(
            #       current_state, action, player_mark, self.config)
                # print("leaf in expan ", leaf_node_id)

                self.tree[child_id] = {'state': new_board, 'player': player_mark,
                                       'child': [], 'parent': leaf_node_id,
                                       'total_node_visits': 0, 'total_node_wins': 0}
                if child_id == (0, 3, 3, 3, 3, 3, 3, 3):
                    print("got child id")
                    print(self.tree[child_id]['child'])
                # if check_result(new_board, player_mark, self.config):
                if winning_move_whole_board(new_board, player_mark):
                    best_action = action
                    is_availaible = True

            self.tree[leaf_node_id]['child'] = childs

            if is_availaible:
                child_node_id = best_action
            # elif 3 in childs:
            #     child_node_id = 3
            else:
                child_node_id = random.choice(childs)
            return leaf_node_id + (child_node_id,)
        return leaf_node_id

    def simulation(self, child_node_id):
        '''
        Aim - Reach the final state of the game
        '''
        # self.total_parent_node_visits += 1
        state = self.tree[child_node_id]['state']
        previous_player = self.tree[child_node_id]['player']

    #   is_terminal = check_result(state, previous_player, self.config)
        is_terminal = winning_move_whole_board(state, previous_player)
        # if (child_node_id == (0, 4, 4)):
        #     print(is_terminal)
        # print("/n"))
        winning_player = previous_player
        count = 0
        flag = 0

        # if is_terminal:
        #     print(state)
        #     flag = 1
        nstate = state.copy()
        # print(nstate)
        while not is_terminal:
            self.actions_available = get_valid_locations(nstate)
            if not len(self.actions_available) or count == 30:
                winning_player = None
                is_terminal = True
            else:
                count += 1
                if previous_player == 1:
                    current_player = 2
                else:
                    current_player = 1

                col = random.choice(self.actions_available)
                # col = pick_best_move_mcts(nstate, current_player)
                roww = get_next_row(nstate, col)
                drop_piece(nstate, roww, col, current_player)
                result = winning_move(nstate, current_player, roww, col)
                if result:  # A player won the game
                    is_terminal = True
                    winning_player = current_player
                    break
                previous_player = current_player
        # if (flag == 1):
        #     print(nstate)
        return winning_player, 51 - count

    def backpropagation(self, child_node_id, winner, value):
        '''
        Aim - Update the traversed nodes
        '''
        player = self.player
        # print(self.tree[(0,)]['player'])
        # player = self.tree[child_node_id]['player']
        # print("node ", child_node_id[1])
        if winner == None:
            reward = 0
        elif (winner == player):
            reward = 1
        else:
            reward = 1

        # if (winner == player):
        node = child_node_id
        self.tree[node]['total_node_visits'] += 1
        if (self.tree[node]['player'] == winner):
            self.tree[node]['total_node_wins'] += value
            # if (node == (0, 4, 4)):
            #     print(self.tree[node]['total_node_wins'])
            #     print("/n")
        while(self.tree[node]['parent'] != None):
            # if (node == (0, 4, 4)):
            #     print(self.tree[node]['total_node_wins'])
            #     print("/n")
            node = self.tree[node]['parent']
            self.tree[node]['total_node_visits'] += 1
            if (self.tree[node]['player'] == winner):
                self.tree[node]['total_node_wins'] += value
        # else:
        #     node = child_node_id
        #     self.tree[node]['total_node_visits'] += 1
        #     # self.tree[node]['total_node_wins'] += 1
        #     while(self.tree[node]['parent'] != None):
        #         node = self.tree[node]['parent']
        #         self.tree[node]['total_node_visits'] += 1
        #         # self.tree[node]['total_node_wins'] += 1

    def start_the_game(self):
        '''
        Aim - Complete MCTS iteration with all the process running for some fixed time
        '''
        self.initial_time = time.time()
        is_expanded = True
        if (self.state[1] == np.array([0, 0, 0, 0, 0, 0, 0])).all():
            count = 0
            for c in range(colCount):
                if self.state[0][c] != 0:
                    count += 1
            if count <= 1:
                is_expanded = False
        last_action = None
        if is_expanded:
            last_action = self.get_action()
            self.root_node = self.root_node + (last_action,)
        flag = 0
        count = 0
        while (time.time() - self.initial_time < self.time_limit and count < 30000):
            count += 1
            if (flag == 0 and time.time() - self.initial_time > 20):
                flag = 1
                # self.tunable_constant = 15
                current_state_node_id = self.root_node
                action_candidates = self.tree[current_state_node_id]['child']
                total_visits = -math.inf
                for action in action_candidates:
                    action = current_state_node_id + (action,)
                    visit = self.tree[action]['total_node_visits']
                    print("value ", visit)
                    print(
                        "value ", self.tree[action]['total_node_wins']/(self.tree[action]['total_node_visits']+1))

                print("\n")

            elif (flag == 1 and time.time() - self.initial_time > 26):
                flag = 2
                # self.tunable_constant = 10
                current_state_node_id = self.root_node
                action_candidates = self.tree[current_state_node_id]['child']
                total_visits = -math.inf
                for action in action_candidates:
                    action = current_state_node_id + (action,)
                    visit = self.tree[action]['total_node_visits']
                    print("value ", visit)
                    print(
                        "value ", self.tree[action]['total_node_wins']/(self.tree[action]['total_node_visits']+1))
                print("\n")

            node_id = self.selection()
            node_id = self.expansion(node_id)
            # if not is_expanded:
            #     node_id = self.expansion(node_id)
            #     is_expanded = True
            winner, value = self.simulation(node_id)
            # print(winner)
            self.backpropagation(node_id, winner, value)
        current_state_node_id = self.root_node
        action_candidates = self.tree[current_state_node_id]['child']
        # print(action_candidates)
        total_visits = -math.inf
        for action in action_candidates:
            action = current_state_node_id + (action,)
            visit = self.tree[action]['total_node_visits']
            print("visits ", visit)
            print("value ", self.tree[action]['total_node_wins'] /
                  (self.tree[action]['total_node_visits']+1))
            # print("visits ", self.tree[action]['total_node_visits'])
            if visit > total_visits:
                total_visits = visit
                best_action = action
        Gtree = self.tree
        print(best_action, self.root_node)
        return best_action, self.tree

#   my_agent = MCTS(obs, config)

#   return my_agent.start_the_game()[1]


def play_game():
    global Gtree
    Gtree = None

    board = create_board()                          # init. of game and game variable

    game_over = False
    # turn = 1
    turn = random.randint(playerTurn, aiTurn)
    init_turn = turn
    result = None
    print_board(board)

    pygame.init()

    sqSize = 100

    width = colCount * sqSize
    height = (rowCount+1) * sqSize

    size = (width, height)

    radius = int(sqSize/2 - 10)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)
    tree = None
    prevBoard = None
    root = (0,)
    col = 0
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, black, (0, 0, width, sqSize))
                posx = event.pos[0]
                if turn == playerTurn:
                    pygame.draw.circle(
                        screen, red, (posx, int(sqSize/2)), radius)
                    pygame.display.update()
                # else:
                #     pygame.draw.circle(
                #         screen, yellow, (posx, int(sqSize/2)), radius)
            # pygame.display.update()

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
                            label = myfont.render("You win!!", 1, red)
                            screen.blit(label, (20, 10))
                            game_over = True

                        turn += 1
                        turn %= 2
                        print_board(board)
                        draw_board(board)
                        pygame.display.update()

            if turn == aiTurn and not game_over:
                label = myfont.render("MCTS Turn", 1, yellow)
                screen.blit(label, (20, 10))
                pygame.display.update()
                # posx = event.pos[0]
                # col = int(math.floor(posx/sqSize))
                root, tree = (
                    MCTS(board, aiPiece, tree, prevBoard, root).start_the_game())
                # col = arr[0]
                col = root[-1]
                # tree = arr[1]
                # prevBoard = arr[2]
                # root = arr[3]
                if is_valid_loc(board, (col)):
                    row = get_next_row(board, col)
                    drop_piece(board, row, col, aiPiece)
                    prevBoard = board.copy()
                    pygame.init()
                    screen = pygame.display.set_mode(size)
                    if winning_move(board, aiPiece, row, col):
                        # draw_board(board)
                        label = myfont.render("MCTS wins!!", 1, yellow)
                        screen.blit(label, (20, 10))
                        game_over = True
                        result = "MCTS"

                    turn += 1
                    turn %= 2
                    print_board(board)
                    draw_board(board)
                    pygame.display.update()

            if (get_valid_locations(board) == 0):
                game_over = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                pygame.event.pump()
                if event.type == pygame.MOUSEMOTION:
                    pass
                    # pygame.draw.rect(screen, black, (0, 0, width, sqSize))
                    # posx = event.pos[0]
                    # if turn == playerTurn:
                    #     pygame.draw.circle(screen, red, (posx, int(sqSize/2)), radius)
                    # else:
                    #     pygame.draw.circle(
                    #         screen, yellow, (posx, int(sqSize/2)), radius)
                pygame.display.update()
                # time.sleep(3)

            if (get_valid_locations(board) == 0):
                game_over = True

            if game_over:
                if (result == None):
                    result = "Draw"
                pygame.time.wait(5000)
    return


play_game()
# data = []
# rows = []
# t = 10
# count = 0
# while(t > 0):
#     t -= 1
#     count += 1
#     rows = play_game()
#     rows.insert(0, count)
#     data.append(rows)
# print(data)
# df = pd.DataFrame(data)

# with open('game_data.csv', 'a') as f:
#     df.to_csv(f, header=False)
