#to choose who starts the game
import random
import copy

# board is represented as 3*3 matrix
empty_board = [[" "," "," "],[" "," "," "],[" "," "," "]]
linesep = "-------------\n"

# prints the current state of the board
def print_board(board):
    board_str = linesep
    for i in range(len(board)):
        line = ""
        for j in board[i]:
            element = "| "+str(j)+" "
            line = line+element
        line = line+"|"
        board_str = board_str+line+"\n"+linesep
    print("\n"+board_str)

#puts a symbol in the coordinate specified as move
def play(symbol,board,move):
    while True:
        if (len(move) == 2 and move[0] in ["1","2","3"] and move[1] in
            ["1","2","3"]):
            if board[int(move[0])-1][int(move[1])-1]==" ":
                board[int(move[0])-1][int(move[1])-1] = symbol
                return
            else:
                print("There is already a symbol there!")
                move=str(input("\nGive me the coordinates of your move as\
                               rowcolum (es. 22)\n"))
        else:
            print("I did not understand what you mean\n")
            move=str(input("\nGive me the coordinates of your move as rowcolum\
                           (es. 22)\n"))

#returns the winning charachter, or draw
def eval_board(board):
    board_full = True
    for i in range(3):
        for j in range(3):
            if board[j][i]==" ":
                board_full = False
    #checks for rows and columns
    for i in range(3):
        if (board[i][0]!=" " and board[i][0]==board[i][1] and
            board[i][0]==board[i][2]):
            return board[i][0]
        elif (board[0][i]!=" " and board[0][i]==board[1][i] and
              board[0][i]==board[2][i]):
            return board[0][i]
    if (board[0][0]!=" " and board[0][0]==board[1][1] and
        board[0][0]==board[2][2]): #checks diagonals
            return board[0][0]
    elif (board[0][2]!=" " and board[0][2]==board[1][1] and
          board[0][2]==board[2][0]):
            return board[0][2]
    elif board_full:
        return "draw"
    else:
        return "incomplete"

# returns True if the game is finished, False if
def game_finished(board,virtual=False):
    global index
    if eval_board(board) == "incomplete":   #not
        return False
    elif eval_board(board) == "draw":
        if not virtual:
            print("Game finished, it is a draw\n")
            print("Let's play again!\n")
        return True
    elif eval_board(board) == "X":
        if not virtual:
            print("Game finished, X is the winner\n")
            print("Let's play again!\n")
        return True
    elif eval_board(board) == "O":
        if not virtual:
            print("Game finished, O is the winner\n")
            print("Let's play again!\n")
        return True
    else: print("error game_finished")

def eval_for_minmax(board):
    if eval_board(board) == "draw":
        return 0
    elif eval_board(board) == "X":
        if AI_symbol == "X":
            return 1
        elif AI_symbol == "O":
            return -1
        else: print("error2 eval for minamx")
    elif eval_board(board) == "O":
        if AI_symbol == "X":
            return -1
        elif AI_symbol == "O":
            return 1
        else: print("error3 eval for minamx")
    else: print("error eval for minmax")

def virtual_play(symbol,board,move):
    virtual_board = copy.deepcopy(board)
    play(symbol,virtual_board,move)
    return virtual_board

# returns a list with the possible moves for the player, given a board
def possible_moves(board):
    possible_moves = []
    for j in range(3):
        for i in range(3):
            if board[i][j]==" ":
                possible_moves.append(str(i+1)+str(j+1))
    return possible_moves

# not used, I choosed to use alphabeta
def minmax(board,AI_plays=False):
    if game_finished(board,True):
        return eval_for_minmax(board)
    elif not game_finished(board):
        if AI_plays:
            score = -2
            for move in possible_moves(board):
                score = max(score,minmax(virtual_play(AI_symbol,board,move)))
            return score
        elif not AI_plays:
            score = +2
            for move in possible_moves(board):
                score = min(score,minmax(virtual_play(player_symbol,board,move),
                                         True))
            return score
        else: print("error minmax")
    else: print("error2 minmax")

# faster version of minmax
def alphabeta(board,alpha,beta,AI_plays=False):
    if game_finished(board,True):
        return eval_for_minmax(board)
    elif not game_finished(board):
        if AI_plays:
            score = -2
            for move in possible_moves(board):
                score = max(score,alphabeta(virtual_play(AI_symbol,board,move),
                                            alpha,beta))
                alpha = max(alpha,score)
                if alpha >= beta:
                    break
            return score
        elif not AI_plays:
            score = +2
            for move in possible_moves(board):
                score = min(score,alphabeta(virtual_play(player_symbol,board,
                                                         move),alpha,beta,True))
                beta = min(beta,score)
                if alpha >= beta:
                    break
            return score
        else: print("error minmax")
    else: print("error2 minmax")

def computer_move(board):
    best_result = -2
    for move in possible_moves(board):
        board_after_move = virtual_play(AI_symbol,board,move)
        current_result = alphabeta(board_after_move,-2,2)
        if current_result>best_result:
            best_move = move
            best_result = current_result
    return best_move

def main_routine():
    global AI_symbol
    global player_symbol
    global empty_board
    print("\nThis is a Tic-Tac-Toe game! Let's play")
    while True:
        board = copy.deepcopy(empty_board)
        mode = input("How many players? (1/2)\n")
        print_board(board)
        if mode == "2":
            # 2 players
            turn_player_1 = True
            while True:
                if turn_player_1 and not game_finished(board):
                    print("\nIt is the turn of the player X")
                    my_move=str(input("\nGive me the coordinates of your move\
                                      as rowcolum (es. 22)\n"))
                    play("X",board,my_move)
                    print_board(board)
                elif not turn_player_1 and not game_finished(board):
                    print("\nIt is the turn of the player O")
                    my_move=str(input("\nGive me the coordinates of your move\
                                      as rowcolum (es. 22)\n"))
                    play("O",board,my_move)
                    print_board(board)
                else: break
                turn_player_1 = not turn_player_1
        elif mode == "1":
            # against AI
            while True:
                player_starts = input("Do you want to start? (Y/N)\n").upper()
                if player_starts == "Y":
                    player_symbol = "X"
                    AI_symbol = "O"
                    turn_player = 1
                    break
                elif player_starts == "N":
                    player_symbol = "O"
                    AI_symbol = "X"
                    turn_player = 0
                    break
                else: print("I did not understand your choice")
            while True:
                if turn_player and not game_finished(board):
                    print("It is your turn and you are",player_symbol,"\n")
                    my_move=str(input("\nGive me the coordinates of your move\
                                      as rowcolum (es. 22)\n"))
                    play(player_symbol,board,my_move)
                    print_board(board)
                elif not turn_player and not game_finished(board):
                    print("It is my turn!\n")
                    play(AI_symbol,board,computer_move(board))
                    print_board(board)
                else: break
                turn_player = not turn_player
        else: print("I did not understand your choice.\n")

main_routine()
