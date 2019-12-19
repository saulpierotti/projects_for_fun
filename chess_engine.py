# Purposes of the programme:
    # Takes a move in chees notation and outputs an appropriate and legal
    # countermove
    # Represents the current board status when asked
    # It is OO for didactic purposes

# General outline of the game representation:
    # The board is represented as a 8*8 matrix (list of lists) of game class
        # The first coordinate is the column, the second the row
    # An empty cell has value 0
    # A cell with a piece contains an object of the appropriate class

# Notes:
    # Maybe could add an option for specifying a particular pieces arrangement
    # Maybe could add an option for playing human-human, human-AI or AI-AI,
    # current only human-AI
    # perfect evaluate_board function
    # add special moves: pawn promotion, en passant
    # add algorithms: a/b
    # add possibility to give check!

letter_xy_table = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
xy_letter_table = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
#set a corrispondece x_value:row_name
W,B = "white","black"
out_of_range = "This value is out of the specified range"
#codifies an uniform way for representing an out of range value
p,r,c,b,q,k = "pawn","rook","knight","bishop","queen","king"
all_pieces = (p,r,c,b,q,k)
automated = False
#is true when an a function is called without user input, skips assertions
showing_possibles = False
#enter a variant path in show_board() if called by show_piece_possibles()
showing_moves = []
#initialises the variable for show_piece_possibles()


#chose a move between the possible ones, using the given algorithm
def AI(algorithm):
    global automated
    automated = True
#skip assertions
    print("I am thinking...")
#the comparison sense is inverted because the function is called after the move
#has been done
#sets the sense of the comparison accordinglu to the palyer who is playing,
#maximising or minimasing
    def compare(current_score,best_score):
        if current_game.who_plays() == W:
            if current_score < best_score: return True
            else: return False
        elif current_game.who_plays() == B:
            if current_score > best_score: return True
            else: return False
        else: raise AssertionError

#choose the best moove considering a depth of 1
    def greedy():
        i = 0
        best_score = 0
        for move in current_game.player_possibles():
#go through all the possible moves
            i += 1
            current_game.move_piece(move)
#perform the move on the board
            current_score = current_game.evaluate_board()
#evaluate the score after the move
            if compare(current_score,best_score) or i == 1:
#update the best score if needed, and in case save the current move as best
                best_move = move
                best_score = current_score
            current_game.undo_move()
#go to the state of the board previous to moving
            current_game.read(move[0]).update_position(move[0])
#moving the piece has update its internal position variable
#undoing the move I need to reset the position to the current one
#move[0] is the address of the piece after the undoing
        return (best_score,best_move)

#return the best move at a given depth+1(0 is considered)
#check the comments on greedy() for a general explanation of the common
#features
    def minmax(depth):
        i = 0
        best_score = 0
        if depth == 0:
#I am at the final iteration, do a greedy choice
            return greedy()
        elif depth > 0:
#I have to go deeper
#First part similar to greedy
            for move in current_game.player_possibles():
#iterate through all the moves
                i += 1
                current_game.move_piece(move)
#perform the move
                current_score = minmax(depth-1)[0]
#this is the iteration: set the score for this move to the score that comes
#from the greedy choice of the deepest iteretion
                if compare(current_score,best_score) or i == 1:
                    best_score = current_score
                    best_move = move
                current_game.undo_move()
                current_game.read(move[0]).update_position(move[0])
#same of greedy()
            return (best_score,best_move)

#AI can be called using one of the available algorithms
    if algorithm == "greedy":
        selected_move = greedy()
    elif algorithm == "minmax":
        selected_move = minmax(2)[1]
#depth is fixed to a value that takes a reasonable amount of time to run
    automated = False
    return selected_move


#convert xy coordinate to conventional notation
def xy_to_letter(coordinate_list):
    x,y = coordinate_list[0],coordinate_list[1]
    try:
        assert ((0<=x<=7) and (0<=y<=7))
        x_letter = xy_letter_table[x]
#add 1 because cells go from 1-8, not 0-7
        letteral_coordinate = str(x_letter)+str(y+1)
        return letteral_coordinate
    except: return out_of_range


#extract x from conventional notation
def letter_to_x(letter_coordinate):
    x_letteral = letter_coordinate[0]
    x_value_string = letter_xy_table[x_letteral]
    x = int(x_value_string)
    assert (0<=x<=7)
    return x


#extract y from conventional notation
def letter_to_y(letter_coordinate):
    y_string = letter_coordinate[1]
    y = int(y_string)-1
    assert (0<=y<=7)
    return y


#combines the to previos functions and return a list
def letter_to_xy(letter_coordinate):
    x = letter_to_x(letter_coordinate)
    y = letter_to_y(letter_coordinate)
    return [x,y]

#returns the opposite color of the one given
def opposite_color(color):
    assert color in (W,B)
    if color == W: return B
    elif color == B: return W


#set the global variable current game to point to the game in play
def set_current_game(game):
    global current_game
    current_game = game

#create a list with all valid square names in it
#needed to check if an user input is a valid move
def list_all_squares():
    global all_squares
    all_squares = []
    for y in range(0,8):
        for x in range(0,8):
            square = xy_to_letter([x,y])
            if square != out_of_range:
                all_squares.append(square)

list_all_squares()


#the complicated game class, which builts the checkboard
class game:
    def __init__(self):
#create an 8*8 empty list of lists
        self.board = []
        for y in range (0,8):
            self.row = []
            for x in range (0,8):
                self.row.append([])
            self.board.append(self.row)
#create a counter variable with value 0
        self.counter = 0
#at creation, the board is assumed to be the current game
        set_current_game(self)

#add pieces in specified positions and gives them properties
    def add_piece(self,piece_name,color,coordinate_list):
        x,y = coordinate_list[0],coordinate_list[1]
        if automated == False:
            assert piece_name in (p,r,c,b,q,k)
            assert color in (W,B)
            assert 0<=x,y<=7
#assert input validity if the human is playing
        if piece_name == p: self.board[x][y].append(pawn())
        elif piece_name == r: self.board[x][y].append(rook())
        elif piece_name == c: self.board[x][y].append(knight())
        elif piece_name == b: self.board[x][y].append(bishop())
        elif piece_name == q: self.board[x][y].append(queen())
        elif piece_name == k: self.board[x][y].append(king())
#add the right object depending on input
        self.read(coordinate_list).update_position(coordinate_list)
        self.read(coordinate_list).give_color(color)
        if automated == False:
#board is represemted as a list of rows. Rows are a list of squares. Squares
#are a list of what was in them in each round. The actual element in a square
#is square[-1]
#when human performs a move, I need to add an element to each square in order
#to preserve an equal lenght for all of them
#this is skipped when building the board, because the function does it
            for my_x in range(0,8):
                for my_y in range(0,8):
                    if len(self.board[x][y])>len(self.board[my_x][my_y]):
#for each square, if it is shorter than the one where I added the piece, add an
#element to it
                        if self.board[my_x][my_y] == []:
                            self.board[my_x][my_y].append(0)
                        else:
                            self.board[my_x][my_y].append(self.board
                                                          ([my_x][my_y][-1]))
                            print("hey")


#place all pieces in the starting position on the board, creating piece objects
    def initialise(self):
        global automated
        automated = True
#avoid checking for unbalanced adding in add_piece
        self.__init__()
#put the board in a virgin state
        self.add_piece(r,W,[0,0])
        self.add_piece(c,W,[1,0])
        self.add_piece(b,W,[2,0])
        self.add_piece(q,W,[3,0])
        self.add_piece(k,W,[4,0])
        self.add_piece(b,W,[5,0])
        self.add_piece(c,W,[6,0])
        self.add_piece(r,W,[7,0])
        for x in range(0,8):
            self.add_piece(p,W,[x,1])
        self.add_piece(r,B,[0,7])
        self.add_piece(c,B,[1,7])
        self.add_piece(b,B,[2,7])
        self.add_piece(q,B,[3,7])
        self.add_piece(k,B,[4,7])
        self.add_piece(b,B,[5,7])
        self.add_piece(c,B,[6,7])
        self.add_piece(r,B,[7,7])
        for x in range(0,8):
            self.add_piece(p,B,[x,6])
        for y in range(2,6):
            for x in range(0,8):
                self.board[x][y].append(0)
        automated = False

# give a score to the current status of the board
    def evaluate_board(self):
        board_value = 0
        for y in range(0,8):
            for x in range(0,8):
                square_content = self.read([x,y])
                if square_content == 0: pass
                else:
                    if square_content.piece_color == W:
                        board_value += square_content.piece_value
                    if square_content.piece_color == B:
                        board_value -= square_content.piece_value
#0 is equally good for balck and white, <0 is good for black, >0 is good for
#white
        return board_value

#take a position, read its content, move the piece on the board to the
#specified position and update the piece internal memory
    def move_piece(self,list_of_positions):
        rook_castled_moving_positions = ()
#reset a variable called when castling
        starting_position,arriving_position = list_of_positions[0],list_of_positions[1]
#it is called with the format [[x,y][x,y]]
        starting_x,starting_y = starting_position[0],starting_position[1]
        arriving_x,arriving_y = arriving_position[0],arriving_position[1]
        my_piece = self.read(starting_position)
        my_color = my_piece.piece_color
        piece_type = my_piece.name
        if automated == False:
#refresh the available moves
            my_piece.update_piece_possibles()
            assert arriving_position in my_piece.possibles
# assert move validity if the human is playing
        if piece_type == k:
            if (abs(starting_x - arriving_x) == 2):
#this means that I am castling, the king is moved normally but here I have to
#move the rook
                if (starting_x - arriving_x == 2):
                    rook_starting_x = 0
                    rook_arriving_x = 3
                elif (starting_x - arriving_x == -2):
                    rook_starting_x = 7
                    rook_arriving_x = 5
                rook_starting_position = [rook_starting_x,starting_y]
                rook_arriving_position = [rook_arriving_x,starting_y]
                my_rook = self.read(rook_starting_position)
                self.board[rook_starting_x][starting_y].append(0)
                self.board[rook_arriving_x][starting_y].append(my_rook)
                rook_castled_moving_positions = (rook_starting_position,
                                                 rook_arriving_position)
        self.board[arriving_x][arriving_y].append(my_piece)
        self.board[starting_x][starting_y].append(0)
#this removes the piece from the starting position and puts it in the new
#position
        for y in range(0,8):
            for x in range(0,8):
                position = [x,y]
                if (position != starting_position and
                    position != arriving_position and
                    not (position in rook_castled_moving_positions)):
                    self.board[x][y].append(self.board[x][y][-1])
#all square lists must have the same lenght, this adds an element to non-moved
#squares
        self.counter += 1
# increment counter variable by 1
        self.read(arriving_position).update_position(arriving_position)
#update the internal position variable for the piece

#eliminate the last element on the list for each square
    def undo_move(self):
        for y in range(0,8):
            for x in range(0,8):
                self.board[x][y].pop()
        self.counter -= 1
#by default pop() eliminates the last element

#return the content of a cell
    def read(self,coordinate_list):
        try:
            x,y = coordinate_list[0],coordinate_list[1]
            assert(x>=0 and y>=0)
#otherways it calls non-existent squares from the end of the list
            square_content = self.board[x][y][-1]
            return square_content
        except:
            return out_of_range
#this is useful for handling exceptions

#human-readable representation of the checkboard
    def show_board(self):
        global automated
        if self.board[0][0] == []:
            print("The board is empty")
            return
        automated = True
        print("  ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        if self.who_plays() == W:
            reverse = False
        elif self.who_plays() == B:
            reverse = True
#reverse the board if black is playing
        if reverse:
            y_range = range(0,8)
            x_range = range(7,-1,-1)
        elif not reverse:
            y_range = range(7,-1,-1)
            x_range = range(0,8)
        for y in y_range:
#the 3rd argument is the incremnent of the range, which has to go backwards in
#order to put white at the bottom
            print(str(y+1),end="")
            for x in x_range:
                if showing_possibles == False:
#default value
                    print(" │ ",end="")
#| symbol preceding the element, without \n (end="")
                    if self.read([x,y]) == 0: print(" ",end="")
                    elif self.read([x,y]).piece_color == W:
                        print(self.read([x,y]).symbol[0],end="")
                    elif self.read([x,y]).piece_color == B:
                        print(self.read([x,y]).symbol[1],end="")
#the first character of the .symbol string is for white, the second for black
                elif showing_possibles == True:
#True only if the function is called by piece.show_piece_possibles()
                    if [x,y] in showing_moves:
#if the current position is among the ones in which the current piece can move
                        if self.read([x,y]) == 0:
#if the square is empty the formatting is the same as always because we will
#add just an x
                            print(" │ ",end="")
                        else:
                            print(" │",end="")
#if the square is already occupied i want to print a space less, because i will
#print both an x an the occupying piece
                            if self.read([x,y]).piece_color == W:
                                print(self.read([x,y]).symbol[0],end="")
                            elif self.read([x,y]).piece_color == B:
                                print(self.read([x,y]).symbol[1],end="")
#the usual if cycle for printing the right color
                        print("x",end="")
#print x in the treathened squares
                    else:
#if current square is not treathened by current piece, do the usual cycle
                        print(" │ ",end="")
                        if self.read([x,y]) == 0: print(" ",end="")
                        elif self.read([x,y]).piece_color == W:
                            print(self.read([x,y]).symbol[0],end="")
                        elif self.read([x,y]).piece_color == B:
                            print(self.read([x,y]).symbol[1],end="")
#leave a blank space for empty cells, which raise an error
            print(" │ ")
#print the row number at the end of the row itself, and prints a different row
#for the last iteration
            if reverse:
                if y<7: print("  ├───┼───┼───┼───┼───┼───┼───┼───┤")
                elif y==7: print("  └───┴───┴───┴───┴───┴───┴───┴───┘")
            elif not reverse:
                if y>0: print("  ├───┼───┼───┼───┼───┼───┼───┼───┤")
                elif y==0: print("  └───┴───┴───┴───┴───┴───┴───┴───┘")
#add a delimiting line after each row
        if reverse:
            print ("    H   G   F   E   D   C   B   A")
        elif not reverse:
            print ("    A   B   C   D   E   F   G   H")
#a representation of the columns, written under them
        automated = False

#return white or balck depending on who must move
    def who_plays(self):
        if self.counter % 2 == 0:
#% is the remainder operator
            return W
        elif self.counter % 2 == 1:
            return B

#return all the legal moves for a given player
    def player_possibles(self):
        player_possibles = []
        player_color = self.who_plays()
        movable_pieces = []
        for y in range(0,8):
            for x in range(0,8):
                current_square = self.read([x,y])
                if current_square != 0:
                    if current_square.piece_color == player_color:
#a move is legal only from a square where I have a piece
                        current_square.update_piece_possibles()
                        for destination in current_square.possibles:
                            move =  [[x,y],destination]
                            player_possibles.append(move)
#create a list of moves
#a move is itself a list [starting_position,arriving_position]
#a position is a list [x,y]
        return player_possibles

#each kind of piece has its class
#this class is common to all pieces and sets shared properties
class piece:
    def give_color(self,color):
        self.piece_color = color
        if self.piece_color == W:
#the direction variables is used for keeping track of the forward
#direction, mainly for pawns
            self.direction = 1
        elif self.piece_color == B:
            self.direction = -1
        else:
            raise AssertionError("The color variable at square " +
                                 self.position  + " has an unexpected value: "
                                 + self.piece_color)

#stores the position in [x,y] format
    def update_position(self,coordinate_list):
        self.position = coordinate_list
        self.x,self.y = coordinate_list[0],coordinate_list[1]
        self.square = current_game.board[self.x][self.y]

#human readable form of the previous function
    def read_position_letteral(self):
        letter_coordinate = xy_to_letter(self.position)
        return letter_coordinate

#prints a chessboard with x on the possible moves for the piece from the
#current position
    def show_piece_possibles(self):
        global showing_possibles
        global showing_moves
#these globals are used by the game.show_board() function
        showing_possibles = True
        self.update_piece_possibles()
        showing_moves = self.possibles
        current_game.show_board()
        showing_possibles = False
        showing_moves = []

#return True if the piece has never moved
    def did_not_move(self):
        return all(content == self.square[-1] for content in self.square)

#this class comprehends pieces capable of moving for a variable amount of
#squares in a given direction
class long_range_piece(piece):
#horizontal sliding
    def h_slide(self,directional_length):
        final_x = self.x + directional_length
        final_y = self.y
        return  [final_x,final_y]

#vertical sliding
    def v_slide(self,directional_length):
        final_x = self.x
        final_y = self.y + directional_length
        return  [final_x,final_y]

#left-down/right-up sliding
    def ru_slide(self,directional_length):
        final_x = self.x + directional_length
        final_y = self.y + directional_length
        return  [final_x,final_y]

#right-down/left-up sliding
    def lu_slide(self,directional_length):
        final_x = self.x - directional_length
        final_y = self.y + directional_length
        return  [final_x,final_y]

#take a list of moves and calculate the ending positions accordingly
    def update_piece_possibles(self):
        self.possibles = []
        for move in self.all_moves:
#loop trough all the moves
            for direction in [1,-1]:
#calculate both in the fw and rv directions
                for length in range(1,8):
#8 is the maximum range possible in the board
#the innermost loop is length, beacause I want to stop calculating the given
#direction after an unsuccesfull trial
                    directional_length = length*direction
                    my_move = move(directional_length)
                    new_square_content = current_game.read(my_move)
                    if new_square_content == out_of_range: break
                    elif new_square_content == 0:
#avoid adding to the list squares not existing or not empty
                        self.possibles.append(my_move)
                    elif (new_square_content.piece_color ==
                    opposite_color(self.piece_color)):
                        self.possibles.append(my_move)
                        break
#even if there is a piece i can move and eat it if it's not mine, but then I
#have to break because i can eat only the first one that I encounter
                    else: break
#the first positions calculated are the nearest ones, breaking the loop avoids
#wasting time in calculating impossible positions

class pawn(piece):
# create human readable name variable for the current piece
    def __init__(self):
        self.name = p
        self.symbol = "♙♟"
        self.all_moves = (self.move_u1,self.move_ur,
                          self.move_ul)
        self.piece_value = 1

#list of all allowed moves
#simple advancement by 1
    def move_u1(self):
        final_x = self.x
        final_y = self.y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        if new_square_content == 0:
            self.move_is_allowed = True
#can move in this direction only if there is an empty square
        else: self.move_is_allowed = False
        return my_move

#eat right
    def move_ur(self):
        final_x = self.x + 1*self.direction
        final_y = self.y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        if new_square_content in (0,out_of_range):
            self.move_is_allowed = False
        elif (new_square_content.piece_color ==
        opposite_color(self.piece_color)):
#can move in this direction only if there is an opponent
            self.move_is_allowed = True
        else: self.move_is_allowed = False
        return my_move

#eat left
    def move_ul(self):
        final_x = self.x - 1*self.direction
        final_y = self.y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        if new_square_content in (0,out_of_range):
            self.move_is_allowed = False
        elif (new_square_content.piece_color ==
        opposite_color(self.piece_color)):
#can move in this direction only if there is an opponent
            self.move_is_allowed = True
        else: self.move_is_allowed = False
        return my_move

#special moves
#advancement by 2 at the beginning
   # def move_u2(self):
   #     final_x = self.x + 2*self.direction
   #     final_y = self.y
   #     return xy_to_letter(final_x,final_y)

# return a list of possible ending positions using the coded moves
    def update_piece_possibles(self):
        self.possibles = []
        for move in self.all_moves:
            my_move = move()
            new_square_content = current_game.read(my_move)
            if self.move_is_allowed:
#the conditions for each move are coded in the moves themselves, because of
#their complexity
                self.possibles.append(my_move)
            else: pass


class rook(long_range_piece):
    def __init__(self):
        self.name = r
        self.symbol = "♖♜"
        self.all_moves = (self.h_slide,self.v_slide)
#rook moves straight
        self.piece_value = 5


class knight(piece):
    def __init__(self):
        self.name = c
        self.symbol = "♘♞"
        self.piece_value = 3

    def update_piece_possibles(self):
        self.possibles = []
        self.all_moves = ()
        for a in (1,-1):
            for b in (2,-2):
                increment = (a,b)
                for i in (0,1):
                    x_increment,y_increment = increment[i],increment[1-i]
#possible increments of both x and y are 2 and 1, in both directions
#if x is 1 y is 3, and vice-versa
                    final_x = self.x + x_increment
                    final_y = self.y + y_increment
                    my_move = [final_x,final_y]
                    new_square_content = current_game.read(my_move)
                    if new_square_content == out_of_range: pass
                    elif (new_square_content == 0 or
                    (new_square_content.piece_color ==
                    opposite_color(self.piece_color))):
#avoid adding to the list squares not existing or not empty
                         self.possibles.append(my_move)
#even if there is a piece i can move and eat it if it's not mine
                    else: pass


class bishop(long_range_piece):
    def __init__(self):
        self.name = b
        self.symbol = "♗♝"
        self.all_moves = (self.ru_slide,self.lu_slide)
#bishop moves diagonally
        self.piece_value = 3

class queen(long_range_piece):
    def __init__(self):
        self.name = q
        self.symbol = "♕♛"
        self.all_moves = (self.h_slide,self.v_slide,self.ru_slide,
                          self.lu_slide)
#queen moves in all directions
        self.piece_value = 8

class king(piece):
    def __init__(self):
        self.name = k
        self.symbol = "♔♚"
        self.piece_possibles = []
        self.all_moves = (self.move_d,self.move_l,self.move_r,self.move_u,
                          self.move_dl,self.move_dr,self.move_ul,self.move_ur)
        self.castle_moves = (self.king_castle,self.queen_castle)
        self.piece_value = 1000

#list of all allowed moves (up,down,left,right and the 4 diagonals)
    def move_u(self):
        final_x = self.x
        final_y = self.y + 1
        return  [final_x,final_y]

    def move_d(self):
        final_x = self.x
        final_y = self.y - 1
        return  [final_x,final_y]

    def move_l(self):
        final_x = self.x - 1
        final_y = self.y
        return  [final_x,final_y]

    def move_r(self):
        final_x = self.x + 1
        final_y = self.y
        return  [final_x,final_y]

    def move_ul(self):
        final_x = self.x - 1
        final_y = self.y + 1
        return  [final_x,final_y]

    def move_ur(self):
        final_x = self.x + 1
        final_y = self.y + 1
        return  [final_x,final_y]

    def move_dl(self):
        final_x = self.x - 1
        final_y = self.y - 1
        return  [final_x,final_y]

    def move_dr(self):
        final_x = self.x + 1
        final_y = self.y - 1
        return  [final_x,final_y]

    def king_castle(self):
        final_x = self.x + 2
        final_y = self.y
        return  [final_x,final_y]

    def queen_castle(self):
        final_x = self.x - 2
        final_y = self.y
        return  [final_x,final_y]

# return a list of possible ending positions using the coded moves
    def update_piece_possibles(self):
        self.possibles = []
        for move in self.all_moves:
            my_move = move()
            new_square_content = current_game.read(my_move)
            if new_square_content == out_of_range: pass
            elif (new_square_content == 0 or
            (new_square_content.piece_color ==
            opposite_color(self.piece_color))):
#avoid adding to the list squares not existing or not empty
                self.possibles.append(my_move)
#even if there is a piece i can move and eat it if it's not mine
        king_allows_castle = ((self.x  == 4) and
                              ((self.y == 0 and self.piece_color == W) or
                               (self.y == 7 and self.piece_color == B)) and
                              self.did_not_move())
#check if can castle, and in case add the move to piece possibles
        for move in self.castle_moves:
            if move == self.king_castle:
                rook_x = 7
            elif move == self.queen_castle:
                rook_x = 0
            my_rook = current_game.read([rook_x,self.y])
            rook_allows_castle = ((my_rook != 0) and (my_rook.name == r) and my_rook.did_not_move())
            there_is_room = (((rook_x == 0) and
                              all((current_game.read([current_x,self.y]) == 0)
                                  for current_x in range(self.x-1,rook_x,-1)))
                             or ((rook_x == 7) and
                                 all((current_game.read([current_x,self.y]) == 0)
                                     for current_x in range(self.x+1,rook_x,+1))))
#to be implemented
            not_in_check = True
            self.castle_is_allowed = (king_allows_castle and rook_allows_castle and
                                 there_is_room and not_in_check)
            if self.castle_is_allowed:
                my_move = move()
                self.possibles.append(my_move)

# Print splash screen
# Main loop:
    # Ask for user input
    # Process the input and do one of the following:
        # Select AI alogrithm
            # Algorithm selection loop
        # Start a new game:
            # Control loop
        # List saved games and allows user to resume one:
            # Control loop
        # Quit
        # Print an error and restarts the main loop

# Control loop:
    # Has AI algorithm been selected?
        # YES:
            # Continue the control loop
        # NO:
            # Print an error
            # Enter algorithm selection loop
    # Ask for user input
    # Process the input and do one of the following:
        # Print current checkboard status
        # Operate a move on the board:
            # Game loop
        # Return to main loop
        # Print an error and restart the control loop

# Algorithm selection loop:
    # Ask for user input
    # Process the input and do one of the following:
        # Select the choosen algorthm
        # Print an error and restart the algorthm selection loop
        # Return to main menu

# Game loop:
    # Check if the game has ended:
        # Print result
        # return to control loop
    # Check who can move and enter the appropriate loop
        # User move loop
       # AI move loop

# User moves loop:
    # Ask the user to insert a move or quit to control loop
    # Input is converted in the internal representation
    # Assert move validity
    # Operate the move on the board
    # Return to game loop

#this calls the main game loop
def play():
    game()
#create a game object
    current_game.initialise()
#put pieces on the board
    while True:
#an infinite loop which cycles through the 2 players
        current_game.show_board()
        current_game.move_piece(AI("minmax"))
        current_game.show_board()
        while True:
#stay here until I do not get a valid move as input
            my_input = input("Which square do you want to select?")
            try:
                assert my_input in all_squares
                starting_position = letter_to_xy(my_input)
                user_selected_square = current_game.read(starting_position)
                user_selected_square.update_piece_possibles()
                assert user_selected_square != 0
                assert user_selected_square.piece_color == current_game.who_plays()
                assert user_selected_square.possibles != []
                break
            except AssertionError: print(my_input+" is not a valide square")
        user_selected_square.show_piece_possibles()
        while True:
#same as above, but for the destination
            my_input = input("Where do you want to move this piece?")
            try:
                assert my_input in all_squares
                arriving_position = letter_to_xy(my_input)
                arriving_position_content = current_game.read(arriving_position)
                assert arriving_position in user_selected_square.possibles
                break
            except AssertionError: print(my_input+" is not a valide square")
        current_game.move_piece([starting_position,arriving_position])
#move the piece as the human said and restart the loop, the AI plays

play()
##current_game.add_piece(k,B,letter_to_xy("E8"))
##current_game.show_board()
##current_game.read(letter_to_xy("E8")).castle()
##current_game.move_piece([letter_to_xy("E8"),letter_to_xy("E7")])
##current_game.show_board()
##current_game.read(letter_to_xy("E7")).castle()
##current_game.move_piece([letter_to_xy("E7"),letter_to_xy("E8")])
##current_game.show_board()
##current_game.read(letter_to_xy("E8")).castle()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
