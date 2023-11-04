from copy import deepcopy
import random
import time

stats = {'wins' : 0, 'losses' : 0, 'lastwin' : ''}
badaimoves = []
goodaimoves = []

def print_rules():
    print("Welcome to Hexapawn!")
    print("You move as with pawns in chess!")
    print("You win by eliminating all the enemy's pieces, preventing the enemy from making a legitimate move or")
    print("bringing a pawn to the enemy's front line.")
    print("The computer will continue to become better as you play, until")
    print("eventually it will be unbeatable")
    for i in range(3):  print('==============================================')    

def print_board(board):
    print()
    for i in range(1, 4):
        print(str(i) + '  |  ' + board[i - 1][0]  + '  |  ' + board[i - 1][1]  + '  |  ' + board[i - 1][2] + "\n")
    print('      a      b      c \n')

def pawn_exists(pawn, board):
    for i in range(3):
        for j in range(3):
            if pawn == board[i][j]:
                return True
    return False

def pawn_location(pawn, board):
    for i in range(3):
        for j in range(3):
            if pawn == board[i][j]:
                return (i, j)

def check_player_win(board):
    if (board[0][0][0] == 'p' or board[0][1][0] == 'p' or board[0][2][0] == 'p'):
        return True
    if not pawn_exists('c1', board) and not pawn_exists('c2', board) and not pawn_exists('c3', board):
        return True
    if len(computer_valid_moves(board)) == 0:
        return True
    return False

def check_computer_win(board):
    if (board[2][0][0] == 'c' or board[2][1][0] == 'c' or board[2][2][0] == 'c'):
        return True
    player_pawn_exists = False
    for i in range(3):
        for j in range(3):
            if board[i][j][0] == 'p':
                player_pawn_exists = True
    if not player_pawn_exists:
        return True
    if len(pawns_valid_moves('p1', board)) == 0 and len(pawns_valid_moves('p2', board)) == 0 and len(pawns_valid_moves('p3', board)) == 0:
        return True
    return False

def convert_square_to_index(square):
    i = None
    j = None
    if square[0] == 'a': j = 0
    elif square[0] == 'b': j = 1
    else: j = 2

    if square[1] == '1': i = 0
    elif square[1] == '2': i = 1
    else: i = 2

    return (i, j)


def convert_index_to_square(index):
    i, j = index
    square = ''
    if j == 0: square = square + 'a'
    elif j == 1: square = square + 'b'
    else: square = square + 'c'
    if i == 2: square = square + '3'
    elif i == 1: square = square + '2'
    else: square = square + '1'

    return square

def pawns_valid_moves(pawn, board):
    moves = []
    if not pawn_exists(pawn, board): return moves
    for i in range(3):
        for j in range(3): 
            if board[i][j] == pawn:
                if i > 0 and board[i - 1][j] == '  ':
                    moves.append(board[i][j] + convert_index_to_square((i - 1, j)))
                if i > 0 and j > 0 and (board[i - 1][j - 1][0] == 'c'):
                    moves.append(board[i][j] + convert_index_to_square((i - 1, j - 1)))
                if i > 0 and j < 2 and (board[i - 1][j + 1][0] == 'c'):
                    moves.append(board[i][j] + convert_index_to_square((i - 1, j + 1)))
    
    return moves

def computer_valid_moves(board):
    moves = []
    for i in range(3):
        for j in range(3): 
            if board[i][j][0] == 'c':
                if i < 2 and board[i + 1][j] == '  ':
                    move = board[i][j] + convert_index_to_square((i + 1, j))
                    if (board, move) not in badaimoves: moves.append(move)
                if i < 2 and j > 0 and (board[i + 1][j - 1][0] == 'p'):
                    move = board[i][j] + convert_index_to_square((i + 1, j - 1))
                    if (board, move) not in badaimoves: moves.append(move)
                if i < 2 and j < 2 and (board[i + 1][j + 1][0] == 'p'):
                    move = board[i][j] + convert_index_to_square((i + 1, j + 1))
                    if (board, move) not in badaimoves: moves.append(move)
    
    return moves

def player_turn(board):
    print("Your Move! \n")
    pawn = None
    pawnloc = tuple()
    while True:
        pawn = input("Which pawn would you like to move?")
        if pawn != 'p1' and pawn != 'p2' and pawn != 'p3': 
            print("That is not a valid pawn, try again!")
            continue
        valid = False
        for i in range(3):
            for j in range(3):
                if pawn == board[i][j]:
                    valid = True
                    pawnloc = (i, j)
        if not valid:
            print("That is not a valid pawn, try again!")
            continue
        if len(pawns_valid_moves(pawn, board)) == 0:
            print("That is pawn has no valid moves, try again!")
            continue
        break
    square = None
    while True:
        square = input("Which square would you like to move to? If you would like to select a different pawn, type 'NONE'")
        if square == 'NONE':
            player_turn(board)
            return None
        move = pawn + square
        if move not in pawns_valid_moves(pawn, board):
            print("That is not a valid move, try again!")
            continue
        break
    index = convert_square_to_index(square)
    i, j = index
    board[i][j] = pawn
    i, j = pawnloc
    board[i][j] = '  '

def computer_turn(board):
    print("Computers Turn! \n")
    time.sleep(1)
    moves = computer_valid_moves(board)
    pawn = None
    square = None
    goodmove = False
    for move in moves:
        if move in goodaimoves:
            pawn = move[0] + move[1]
            square = move[2] + move[3]
    if not goodmove:
        x = random.randint(0, len(moves) - 1)
        pawn = moves[x][0] + moves[x][1]
        square = moves[x][2] + moves[x][3]
    i, j = pawn_location(pawn, board)
    board[i][j] = '  '
    i, j = convert_square_to_index(square)
    board[i][j] = pawn
    return pawn + square

def print_stats():
    print("Wins : " + str(stats['wins']))
    print("Losses : " + str(stats['losses']))
    print("Last Win : " + str(stats['lastwin']) + '\n')

def reset_game(board):
    time.sleep(2)
    print('==============================================')
    print('==============================================')
    print("New Game!")
    game()

def game():
    board = [['c1', 'c2', 'c3'], ['  ', '  ', '  '], ['p1', 'p2', 'p3']]
    print_board(board)
    lastcomputermove = None
    while True:
        player_turn(board)
        print_board(board)
        if check_player_win(board):
            stats['wins'] = stats['wins'] + 1
            stats['lastwin'] = 'Player'
            print("You Won! \n")
            badaimoves.append(lastcomputermove)
            print_stats()
            reset_game(board)
            continue
        print('==============================================')
        print('==============================================')
        lastcomputermove = (deepcopy(board), computer_turn(board))
        print(lastcomputermove)
        print_board(board)
        if check_computer_win(board):
            stats['losses'] = stats['losses'] + 1
            stats['lastwin'] = 'Computer'
            print("The Computer Won! \n")
            goodaimoves.append(lastcomputermove)
            print_stats()
            reset_game(board)
        print('==============================================')
        print('==============================================')

print_rules()
game()

