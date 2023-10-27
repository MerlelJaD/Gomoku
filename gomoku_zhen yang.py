# -*- coding: utf-8 -*-
"""
A Python module for the Gomoku game.
TODO: Write a Python module to implement the famous Gomoku game.
It allows the game to be played either by two humans, 
a human against a computer, or by the computer against itself.
It also allows for a game to be loaded from a file and continued.

Full name: Zhen Yang
StudentId: 10636485
Email: zhen.yang@student.manchester.ac.uk
"""
from copy import deepcopy

def newGame(player1, player2):
    """
    Returns a game dictionary where player1 and player2 corresponding to 
    the player's names are set to the input parameters of the function, 
    and the variable who is set to the integer 1. In this dictionary all 
    the positions of the board are empty (set to the integer 0).
    """
    game = {
     'player1' : player1,
     'player2' : player2,
     'who' : 1,
     'board' : [ [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0], 
                 [0,0,0,0,0,0,0,0]]
    }
    
    return game

def printBoard(board):
    """
    Prints the 8-by-8 Gomoku board.
    Board positions which are not occupied by any player should be printed empty.
    Positions occupied by player 1 should be marked with an "X".
    Positions occupied by player 2 should be marked with an "O".
    """
    board2 = deepcopy(board)
    for i in range(8):  
        for j in range(8):
            if board2[i][j] == 0:
                board2[i][j] = " "
            if board2[i][j] == 1:
                board2[i][j] = "X"
            if board2[i][j] == 2:
                board2[i][j] = "O"

    for k in range(8):
        board2[k].insert(0,k+1)
        
    print(' |a|b|c|d|e|f|g|h|')
    print(" " + "+-" * 8 + "+")
    for row in board2:
        print('{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(*row))
    print(" " + "+-" * 8 + "+")
          
def posToIndex(s):
    """
    The function takes a string s as argument and returns a tuple (r,c) with r and c 
    corresponding to the indices of the associated board row and column position.
    If the provided string cannot be converted, the function raise a ValueError exception.
    """
    s=s.lower()
    s=",".join(s)
    s=s.split(",")
    while " " in s:
        s.remove(" ")
    if len(s) == 2:
        s=sorted(s)
        r=int(s[0])-1
        c=ord(s[1])-97
        if r in range(8) and c in range(8):
            return (r,c)
        else:
            raise ValueError
    else:
        raise ValueError
              
def indexToPos(t):
    """
    Returns a 2-character string corresponding to the board column/row using 
    a single letter from a,…,h and a single-digit integer from 1,…,8.
    """
    r=str(t[0]+1)
    c=chr(t[1]+97)
    t=c+r
    return t        

def loadGame(filename):
    """
    The function attempts to open the text file of the name filename and 
    returns its content in form of a game dictionary.
    The function raise a FileNotFoundError exception if the file cannot be loaded.
    If the file’s content is not of the correct format, raise a ValueError exception.
    """
    with open(filename, mode="rt", encoding="utf8") as f:
        lines = f.readlines()
        if lines[0].isspace() == True or lines[1].isspace() == True:
            raise ValueError
        if len(lines) != 11:
            raise ValueError
        for i in range(11):
            lines[i] = lines[i].strip('\n')
        if int(lines[2]) != 1 and int(lines[2]) != 2:
            raise ValueError
        for i in range(3,11):
            a = lines[i].split(",")
            if len(a)!=8:
                raise ValueError
            else:
                for j in range(8):
                    if int(a[j]) != 0 and int(a[j]) != 1 and int(a[j]) != 2:
                        raise ValueError
                    else:
                        a[j]=int(a[j])
                        lines[i]=a
                     
    game = {
     'player1' : lines[0],
     'player2' : lines[1],
     'who' : int(lines[2]),
     'board' : lines[3:11]
    }
    return game

def getValidMoves(board):
    """
    Returns a list of tuples of the form (r,c) with r and c corresponding to 
    the indices of the associated board row/column position.
    If no valid move is possible, the function returns an empty list.
    """
    A=[]
    for i in range(8):  
        for j in range(8):
            if  board[i][j] == 0:
                a = (i,j)
                A.append(a)

    return A

def makeMove(board,move,who):
    """
    Returns the updated board.
    """
    r = move[0]
    c = move[1]
    board[r][c] = who
    return board
    
def hasWon(board,who):
    """
    Returns True if the player with number who occupies five adjacent positions 
    which form a horizontal, vertical, or diagonal line. Returns False otherwise.
    """
    for i in range(8-4):
        for j in range(8):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] == who:
                return True
            
    for i in range(8):
        for j in range(8-4):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] == who:
                return True
            
    for i in range(8-4):
        for j in range(8-4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] == who:
                return True
            
    for i in range(8-4):
        for j in range(8-4):
            if board[i+4][j] == board[i+3][j+1] == board[i+2][j+2] == board[i+1][j+3] == board[i][j+4] == who:
                return True
    
    return False

def suggestMove1(board, who):
    """
    Returns a tuple (r,c) with r and c corresponding to the indices of 
    the associated board row/column position onto which player number 
    who should place their "piece".
    """
    n = getValidMoves(board)
    board2=deepcopy(board)
    for i in n:
        makeMove(board2, i, who)
        if hasWon(board2, who) == True:
            return i
        else:
            board2=deepcopy(board)
    if who == 1:
        other = 2
    else:
         other = 1
    for j in n:
        makeMove(board2, j, other)
        if hasWon(board2, other) == True:
            return j
        else:
            board2=deepcopy(board)
            
    return n[0]

# ------------------- Main function --------------------
def play():
    """
    The driver function of the game and does the following things:
    1: Prints a welcome message.
    2: Ask for the names of player 1 and player 2.
    3: If one of the players’ names (or both) is the letter 'C', 
    the corresponding user is played automatically by the computer.
    4: Creates a new game dictionary.
    5: If the active player is human, the program asks which move they want to make.
    6: If the active player’s name is 'C', the program will make a move automatically.
    7: If one player has won, the game prints this information and then ends.
    8: If there is no valid move left, the game prints that there was a draw and ends.
    9: Otherwise, the active player switches and the program continues with Step 5.
    10: When the name of player 1 is entered as the letter 'L', the program will 
    skip asking for the name of player 2, ask instead for a filename and 
    attempt to load the game dictionary from that file.
    """
    print("*" * 55)
    print("***" + " " * 8 + "WELCOME TO STEFAN'S GOMOKU!" + " " * 8 + "***")
    print("*" * 55, "\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    player1 = input('Enter the name of player 1:')
    while len(player1) == 0 or player1.isspace() == True:
        player1 = input('Enter the name of player 1:')
    player1 = player1.capitalize()
        
    if player1 == "L":
        filename = input('Enter the filename:')
        if len(filename) == 0:
            filename = 'game.txt'
        game = loadGame(filename) 
    else:
        player2 = input('Enter the name of player 2:')
        while len(player2) == 0 or player2.isspace() == True:
            player2 = input('Enter the name of player 2:')
        player2 = player2.capitalize()
        game = newGame(player1, player2)
    
    player_1 = game['player1']
    player_2 = game['player2']
    board = game['board']
    who = game['who']
    while True:
        printBoard(board)
        if who == 1:
            player = player_1
        else:
            player = player_2
        print('Player ' + player + "'s turn")
        
        if player == 'C':
            move = suggestMove1(board, who) 
        else:
            while True:
                s = input('Which move do you want to make:')
                try:
                    move = posToIndex(s)
                    if move in getValidMoves(board):
                        break
                    if move not in getValidMoves(board):
                        print('Warning: This is not a valid move!')
                except ValueError:
                    print('Warning: This is not a valid move!')
            
        makeMove(board, move , who)
        
        A = getValidMoves(board)
        length_A = len(A)
        if length_A == 0:
            printBoard(board)
            print('There was a draw!')
            break
        
        if hasWon(board, who) == True:
            printBoard(board)
            print('Player ' + player + ' won!')
            break
        
        if who == 1:
            who = 2
        else:
            who = 1
            
if __name__ == '__main__' or __name__ == 'builtins':
 play()


