#!/usr/bin/python3

from IPython.display import clear_output
import random, os

def explain():
    """
    Print intro
    Show the rows and index positions
    """

    print("Hi! Welcome to tic-tac-toe!")
    print("You will be asked in which row, and on which position to enter your mark")
    print("Once you get three in a row, you win!")
    print("It looks like this:")

    row_positions = ['1', '2', '3']

    print("\n"*2)

    for i in range(1, 4):
        print(f" {row_positions[0]} | {row_positions[1]} | {row_positions[2]}       <<<<<<---- Row {i}")
        if i != 3:
            print("-" * 11)

    print("\n"*2)


def playernames():
    """
    Get the names of the players
    """    
    player_1 = ''
    while player_1 == '':
        player_1 = input("What is the name of player 1? ")
    
    player_2 = ''
    while player_2 == '':
        player_2 = input("What is the name of player 2? ")

    return player_1, player_2

def whostarts():
    turn = random.randint(1, 2)
    return turn

def gamestate(row_1, row_2, row_3):
    """
    Visualize the gamestate while playing the game
    """

    print("\n" * 2)
    print(f" {row_1[0]} | {row_1[1]} | {row_1[2]} ")
    print("-" * 11)
    print(f" {row_2[0]} | {row_2[1]} | {row_2[2]} ")
    print("-" * 11)
    print(f" {row_3[0]} | { row_3[1]} | {row_3[2]} ")
    print("\n" * 2)


def select_row_position(row):
    """
    Get user input for a row or position choice
    Use boolean switch to display correct text
    return in which row/position to place a character
    """

    allowed = ['1', '2', '3']

    choice = 'wrong'

    if row == True:
        word = ('In', 'row')
    else:
        word = ('On', 'position')

    while choice not in allowed:
        choice = input(f"{word[0]} which {word[1]} do you want to enter your mark? ")

        if not choice.isdigit():
            print("Digits only please!")
        if not choice in allowed:
            print("Not in range!")

    if row:
        return int(choice)
    else:
        return int(choice) - 1

def win(row_1, row_2, row_3):
    """
    Check whether there is a 'three in a row' occurence and if so, return the corresponding character
    """    
    win_chars = ['x', 'o']

    # Horizontal rows
    if row_1[0] == row_1[1] == row_1[2] and row_1[0] in win_chars:
        return row_1[0]
    elif row_2[0] == row_2[1] == row_2[2] and row_2[0] in win_chars:
        return row_2[0]
    elif row_3[0] == row_3[1] == row_3[2] and row_3[0] in win_chars:
        return row_3[0]
    
    # Vertical rows
    elif row_1[0] == row_2[0] == row_3[0] and row_1[0] in win_chars:
        return row_1[0]
    elif row_1[1] == row_2[1] == row_3[1] and row_1[1] in win_chars:
        return row_1[1]
    elif row_1[2] == row_2[2] == row_3[2] and row_1[2] in win_chars:
        return row_1[2]
    
    # Diagonal rows
    elif row_1[0] == row_2[1] == row_3[2] and row_1[0] in win_chars:
        return row_1[0]
    elif row_1[2] == row_2[1] == row_3[0] and row_1[2] in win_chars:
        return row_1[2]

    else:
        return None

def legal_choice(rowc, posc, rows):
    """
    Check whether the chosen position is still free, return False otherwise
    """
    if rows[rowc -1][posc] == ' ':
        return True
    else:
        return False

def tie(rows):
    """
    Check whether there is a free space left on the board, return False otherwise
    """
    for row in rows:
        for i in row:
            if i == ' ':
                return False

    return True

def Play():
    """
    Play the game
    While the win function does not return a character, keep asking for row/position choice and increment the turn count
    Clear the screen after input has been given
    When a player wins, clear screen and show winner
    """
    explain()
    
    names = playernames()
    player_1 = names[0]
    player_2 = names[1]

    p1_mark = 'x'
    p2_mark = 'o'

    print(f"Player {player_1} has mark '{p1_mark}'")
    print(f"Player {player_2} has mark '{p2_mark}'")

    row_1 = [' ', ' ', ' ']
    row_2 = [' ', ' ', ' ']
    row_3 = [' ', ' ', ' ']

    turn = whostarts()

    while win(row_1, row_2, row_3) == None:
        os.system('clear')
        
        if turn % 2 != 0:
            print(f"\nIt's {player_1}'s turn!")
        else:
            print(f"\nIt's {player_2}'s turn!")

        gamestate(row_1, row_2, row_3)

        legal = 'no'
        while legal == 'no':
            row_choice = select_row_position(True)
            position_choice = select_row_position(False)

            if legal_choice(row_choice, position_choice, [row_1, row_2, row_3]) == True:
                legal = 'yes'
            else:
                print(f"This spot is already taken. Please choose a free place!")

        if turn % 2 != 0:
            mark = p1_mark
        else:
            mark = p2_mark

        if row_choice == 1:
            row_1[position_choice] = mark
        elif row_choice == 2:
            row_2[position_choice] = mark
        elif row_choice == 3:
            row_3[position_choice] = mark

        turn += 1

        if tie([row_1, row_2, row_3]) == True:
            break

    os.system('clear')

    if win(row_1, row_2, row_3) == p1_mark:
        print(f"Player {player_1} won!!")
    elif win(row_1, row_2, row_3) == p2_mark:
        print(f"Player {player_2} won!!")
    else:
        print(f"It's a tie :(")
    gamestate(row_1, row_2, row_3)


    again = input("Do you want to play again? (Yes/other) ")
    if again.lower() == 'yes' or again.lower() == 'y':
        os.system('clear')
        Play()

Play()