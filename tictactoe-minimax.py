from os import system
from os import name as sys_name
from random import choice
from time import sleep
from math import inf

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
human = -1
comp = +1

board_copy = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

def clear_board():
    global board
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

def is_winner(board, player):
    win_state = [
        [board[0][0], board[0][1], board[0][2]],    # Primeira linha
        [board[1][0], board[1][1], board[1][2]],    # Segunda linha
        [board[2][0], board[2][1], board[2][2]],    # Terceira linha
        [board[0][0], board[1][0], board[2][0]],    # Primeira coluna
        [board[0][1], board[1][1], board[2][1]],    # Segunda coluna
        [board[0][2], board[1][2], board[2][2]],    # Terceira coluna
        [board[0][0], board[1][1], board[2][2]],    # Diagonal principal
        [board[0][2], board[1][1], board[2][0]]     # Diagonal secundária
    ]

    return True if [player, player, player] in win_state else False


def available_move(move):
    return True if board[move[0]][move[1]] == 0 else False


def set_move(move, choice):
    board[move[0]][move[1]] = choice


def human_move(h_choice, c_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over():
        return

    clear_screen()
    print(f'HUMAN TURN - {h_choice}', end='')
    print_board(h_choice, c_choice)
    move_set = {
        1 : [0, 0], 2 : [0, 1], 3 : [0, 2],
        4 : [1, 0], 5 : [1, 1], 6 : [1, 2],
        7 : [2, 0], 8 : [2, 1], 9 : [2, 2]}
    
    while True:
        try:
            move = int(input('Choose where to play (1 to 9): '))
            if 0 < move < 10:
                if available_move(move_set[move]):
                    h_move = move
                    break
                else:
                    print('Invalid choice!')
            else:
                print('Please choose from 1 to 9 only!')
        except (TypeError, ValueError):
            print('Invalid choice!')
        except KeyboardInterrupt:
            print('\n\nBye\n')
            exit()
    
    set_move(move_set[h_move], human)


def empty_cells(board):
    empty_cells = list()

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                empty_cells.append([x, y])
    
    return empty_cells


def evaluate(board):
    if is_winner(board, comp):
        score = +1
    elif is_winner(board, human):
        score = -1
    else:
        score = 0

    return score


def minimax(board, depth, player):
    if player == comp:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if depth == 0 or game_over():
        score = evaluate(board)
        return [-1, -1, score]

    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == comp:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def ai_move(h_choice, c_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over():
        return

    clear_screen()
    print(f'COMPUTER TURN - {c_choice}', end='')
    print_board(h_choice, c_choice)
    
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        move = [x, y]
    else:
        move = minimax(board, depth, comp)

    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = comp
        if is_winner(board, comp):
            move = [x, y]
        board[x][y] = 0

    set_move(move, comp)
    sleep(0.1)


def game_over():
    return is_winner(board, human) or is_winner(board, comp) or board_full()


def board_full():
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    
    return True


def print_board(h_choice, c_choice):
    symbols = {
        -1 : h_choice,
        +1 : c_choice,
        0 : ' '
    }
    line = '-------------'

    print(f'\n{line}')
    for row in board:
        for cell in row:
            print(f'| {symbols[cell]} ', end='')
        print(f'|\n{line}')


def clear_screen():
    if 'windows' in sys_name.lower():
        system('cls')
    else:
        system('clear')


def main():
    clear_screen()
    while True:
        try:
            first = input('Wanna play first? (s/n) ').strip().lower()
            if first == 's' or first == 'n':
                print()
                break
            else:
                print('Insert only \'s\' or \'n\'!')
        except KeyboardInterrupt:
            print('\n\nBye!\n')
            exit()

    clear_screen()
    while True:
        try:
            human_choice = input('Wanna play as \'X\' or \'O\'? ').strip().upper()
            if human_choice == 'X' or human_choice == 'O':
                print(f'Chosen: {human_choice}')
                input()
                break
            else:
                print('Insert only \'X\' or \'O\'!')
        except KeyboardInterrupt:
            print('\n\nBye!\n')
            exit()

    comp_choice = 'O' if human_choice == 'X' else 'X'
    clear_screen()
    while not game_over():
        if first == 'n':
            ai_move(human_choice, comp_choice)
            first = ''
        
        human_move(human_choice, comp_choice)
        ai_move(human_choice, comp_choice)

    
    clear_screen()
    print_board(human_choice, comp_choice)

    if is_winner(board, human):
        print('\nYOU WIN!\n')
    elif is_winner(board, comp):
        print('\nYOU LOSE!\n')
    else:
        print('\nIT\'S A DRAW!\n')

    input()


while True:
    main()

    clear_screen()
    while True:
        try:
            again = input('Wanna play again? (s/n) ').strip().lower()
            if again == 's':
                clear_board()
                main()
            elif again == 'n':
                print('\n\nBye!\n')
                exit()
            else:
                print('Invalid choice!')
        except KeyboardInterrupt:
            print('\n\nBye!\n')
            exit()