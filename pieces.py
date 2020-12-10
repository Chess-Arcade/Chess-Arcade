import os
from copy import deepcopy
# from board import Board

# b_bishop = pygame.image.load(os.path.join('assets', 'black_bishop.png'))
# b_king = pygame.image.load(os.path.join('assets', 'black_king.png'))
# b_knight = pygame.image.load(os.path.join('assets', 'black_knight.png'))
# b_pawn = pygame.image.load(os.path.join('assets', 'black_pawn.png'))
# b_queen = pygame.image.load(os.path.join('assets', 'black_queen.png'))
# b_rook = pygame.image.load(os.path.join('assets', 'black_rook.png'))

# w_bishop = pygame.image.load(os.path.join('assets', 'white_bishop.png'))
# w_king = pygame.image.load(os.path.join('assets', 'white_king.png'))
# w_knight = pygame.image.load(os.path.join('assets', 'white_knight.png'))
# w_pawn = pygame.image.load(os.path.join('assets', 'white_pawn.png'))
# w_queen = pygame.image.load(os.path.join('assets', 'white_queen.png'))
# w_rook = pygame.image.load(os.path.join('assets', 'white_rook.png'))

class Piece:
    '''
    The piece base class applies to all the following chess piece classes. This class contains a reference to the piece's
    current row and column within the grid as integer indices from 0 to 7. The color property is a string of w or b which
    indicates the black or white orientation of the piece. The move_list is a list of the valid moves that a piece can 
    make from its current position on the board. It does not include the attack_list which are valid moves that indicate
    that the piece is capturing another piece. The valid moves are determined in the sub classes that follow. Finally, 
    there is a move_counter which tracks the state of the piece's activity to determine factors like castling and pawns
    being able to move twice on the first move.
    '''
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.move_list = []
        self.attack_list = []
        self.move_counter = 0
    
    def not_off_board(self, move):
        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
            return True

    def same_color_piece(self, move, board):
        row = move[0]
        column = move[1]
        # if row >= len(board.board):
        #     raise Exception('Row out of range')
        # if column >= len(board.board[row]):
        #     print(board.board[row])
        #     return f'Column:{column} out of range'

        if board.board[row][column]:
            if board.board[move[0]][move[1]].color == self.color:
                return True

    def validate_possibility(self, move, board):
        if self.not_off_board(move) and not self.same_color_piece(move, board):
            return True

    def test_if_your_king_is_in_check(self):
        '''
        Go through the whole board and find out if the attempted move results in the same color king being in check
        Returns a truthy if king is under attack
        '''
        # take out valid moves that end in king in check

        def psuedo_move(move):
            temp_board = deepcopy(board)
            temp_board.board[move[0]][move[1]] = temp_board.board[self.row][self.col]
            temp_board.board[self.row][self.row] = 0

            for i in range(8):
                for j in range(8):
                    if temp_board.board[i][j]:
                        if temp_board.board[i][j].color != self.color:
                            temp_board.board[i][j].valid_moves(temp_board)

            if self.color != temp_board.check_status():
                return True
            return False

        survivors = []

        for move in self.move_list:
            if psuedo_move(move):
                survivors.append(move) 
 
        self.move_list = survivors
        # return self.move_list
       
class King(Piece):
    '''
    The king can move one space in any direction as long as there is no piece of the same color on that square, 
    that square is not off the board, and there is no piece that would put the king in check if the king were to 
    move to that square. If the king has not moved yet, and neither has the rook with which it wants to castle, 
    the king can step over two squares towards the rook and have the rook hop directly over the king to the adjacent
    square. Castling can only occur if there is no piece of the same color sitting on any of the tiles being traversed, 
    and so long as the king is not placed in check along its path.
    '''

    def valid_moves(self, board):
        position = [self.row, self.col]

        up = [position[0] - 1, position[1]]
        down = [position[0] + 1, position[1]]
        right = [position[0], position[1] + 1]
        left = [position[0], position[1] - 1]
        down_right = [position[0] + 1, position[1] + 1]
        up_right = [position[0] - 1, position[1] + 1]
        down_left = [position[0] + 1, position[1] - 1]
        up_left = [position[0] - 1, position[1] - 1]

        possible_moves = [up,down,left,right,down_left,down_right,up_left,up_right]
        # check if the king has not moved, check if the corresponding rook has not moved
        # check that the tiles the king is moving over are not cover
        # check if the tiles the king is moving over are not under attack

        if self.move_counter == 0:
        #black king castling
            if board.board[0][7]:
                if board.board[0][7].move_counter == 0:
                    if not board.board[0][5] and not board.board[0][6]:
                        castle_right = [position[0],position[1] + 2]
                        possible_moves.append(castle_right)

            if board.board[0][0]:
                if board.board[0][0].move_counter == 0:
                    if not board.board[0][1] and not board.board[0][2] and not board.board[0][3]:
                        castle_left = [position[0],position[1] - 2]
                        possible_moves += [castle_left]
            
        #white king
            if board.board[7][7]: 
                if board.board[7][7].move_counter == 0:
                    if not board.board[7][6] and not board.board[7][5]:
                        castle_right = [position[0],position[1] + 2]
                        possible_moves.append(castle_right)

            if board.board[7][0]:
                if board.board[7][0].move_counter == 0:
                    if not board.board[7][1] and not board.board[7][2] and not board.board[7][3]: 
                        castle_left = [position[0],position[1] - 2]
                        possible_moves.append(castle_left)
       
        print(possible_moves)
        for move in possible_moves:
            if self.not_off_board(move):
                if board.board[move[0]][move[1]] and not self.same_color_piece(move, board):
                    self.attack_list += [move]
                elif not self.same_color_piece(move, board):
                    self.move_list += [move]

        #TODO: kings cannot move into check    
        #TODO: Castling to the left and right if the king has not moved and the castling rook has not moved

class Queen(Piece):

    def valid_moves(self, board):
        current_position = [self.row, self.col]
        
        def left():
            position = [current_position[0], current_position[1] - 1]
            while self.not_off_board(position) and not self.same_color_piece(position, board):
                # if self.color != self.test_if_your_king_is_in_check(position, board):
                temp_position = position
                if board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                else:
                    self.move_list += [temp_position]
                position = [position[0], position[1] - 1]
            return

        def right():
            position = [current_position[0], current_position[1] + 1]
            while self.not_off_board(position) and not self.same_color_piece(position, board):
                temp_position = position
                if board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                else:
                    self.move_list += [temp_position]
                position = [position[0], position[1] + 1]
            return

        def up():
            position = [current_position[0] - 1, current_position[1]]
            while self.not_off_board(position) and not self.same_color_piece(position, board):
                temp_position = position
                if board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                else:
                    self.move_list += [temp_position]
                position = [position[0] - 1, position[1]]
            return

        def down():
            position = [current_position[0] + 1, current_position[1]]
            while self.not_off_board(position) and not self.same_color_piece(position, board):
                temp_position = position
                if board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                else:
                    self.move_list += [temp_position]
                position = [position[0] + 1, position[1]]
            return


        def diagonal_north_west():
            position = [current_position[0] - 1, current_position[1] - 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] - 1, position[1] - 1]
            return
        
        def diagonal_north_east():
            position = [current_position[0] - 1, current_position[1] + 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] - 1, position[1] + 1]
            return

        def diagonal_south_east():
            position = [current_position[0] + 1, current_position[1] + 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] + 1, position[1] + 1]
            return

        def diagonal_south_west():
            position = [current_position[0] + 1, current_position[1] - 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] + 1, position[1] - 1]
            return

        up()
        down()
        left()
        right()
        diagonal_north_west()
        diagonal_north_east()
        diagonal_south_west()
        diagonal_south_east()
    
class Knight(Piece):

    def valid_moves(self, board):

        position = [self.row, self.col]

        left_up = [position[0] - 2,position[1] - 1]
        left_down = [position[0] - 2,position[1] + 1]
        up_left = [position[0] - 1,position[1] - 2]
        down_left = [position[0] - 1,position[1] + 2]
        right_up = [position[0] + 2,position[1] - 1]
        right_down = [position[0] + 2,position[1] + 1]
        up_right = [position[0] + 1,position[1] - 2]
        down_right = [position[0] + 1,position[1] + 2]

        possible_moves = [left_up,left_down,up_left,down_left,right_up,right_down,up_right,down_right]
        
        for move in possible_moves:
            if self.not_off_board(move):
                if board.board[move[0]][move[1]] and  not self.same_color_piece(move, board):
                    self.attack_list += [move]
                elif not self.same_color_piece(move, board):
                    self.move_list += [move]

    #TODO: build the moves checking

class Bishop(Piece):

    def valid_moves(self, board):
        current_position = [self.row, self.col]

        def diagonal_north_west():
            position = [current_position[0] - 1, current_position[1] - 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] - 1, position[1] - 1]
            return
        
        def diagonal_north_east():
            position = [current_position[0] - 1, current_position[1] + 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] - 1, position[1] + 1]
            return

        def diagonal_south_east():
            position = [current_position[0] + 1, current_position[1] + 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] + 1, position[1] + 1]
            return

        def diagonal_south_west():
            position = [current_position[0] + 1, current_position[1] - 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    temp_position = position
                    self.attack_list += [temp_position]
                    break
                self.move_list+= [position]
                position = [position[0] + 1, position[1] - 1]
            return
    
        diagonal_north_west()
        diagonal_north_east()
        diagonal_south_east()
        diagonal_south_west()

class Rook(Piece):

    def valid_moves(self, board):

        current_position = [self.row,self.col]

        def left():
            position = [current_position[0], current_position[1] - 1]
           
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                    break
                # temp_position = position
                self.move_list += [position]
                position = [position[0], position[1] - 1]
            return

        def right():
            position = [current_position[0], current_position[1] + 1]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                    break
                # temp_position = position
                self.move_list += [position]
                position = [position[0], position[1] + 1]
            return

        def up():
            position = [current_position[0] - 1, current_position[1]]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                    break
                # temp_position = position
                self.move_list += [position]
                position = [position[0] - 1, position[1]]
            return

        def down():
            position = [current_position[0] + 1, current_position[1]]
            while self.not_off_board(position):
                if self.same_color_piece(position, board):
                    break
                elif board.board[position[0]][position[1]]:
                    self.attack_list += [position]
                    break
                # temp_position = position
                self.move_list += [position]
                position = [position[0] + 1, position[1]]
            return

        up()
        down()
        left()
        right()

    #TODO: build the moves checking

# Pawn class includes a move counter to track the first move when moving forward by 2 steps is a valid move
    # Also keep track of when pawn gets to 5 moves and is on the last row, or has moved 6 times in total to promote the pawn
# Other than these exceptions, pawns can always move one step forward if there are no pieces in front of them
# Pawns can attack to the left or attack to the right if there are opposing pieces on those tiles
# Pawns direction of movement depends on the pawn's color (black moves down the board, white moves up the board)
class Pawn(Piece):

    def promote(self):
        current_position = [self.row, self.col]
        color = self.color
        self = Queen(current_position[0],current_position[1], color)
   
    def valid_moves(self, board):

        current_position = [self.row, self.col]

        if self.color == 'w':

            forward = [current_position[0] - 1, current_position[1]]
            if not board.board[forward[0]][forward[1]]:
                if self.validate_possibility(forward, board):
                    self.move_list += [forward]

                forward_two = [current_position[0] - 2, current_position[1]]
                if not self.move_counter and not board.board[forward_two[0]][forward_two[1]]:
                    if self.validate_possibility(forward_two, board):
                        self.move_list += [forward_two]

            attack_left = [current_position[0] - 1, current_position[1] - 1]
            if board.board[attack_left[0]][attack_left[1]]:
                if board.board[attack_left[0]][attack_left[1]].color == 'b':
                    if self.validate_possibility(attack_left, board):
                        self.attack_list += [attack_left]

            attack_right = [current_position[0] - 1, current_position[1] + 1]
            if board.board[attack_right[0]][attack_right[1]]:
                if board.board[attack_right[0]][attack_right[1]].color == 'b':
                    if self.validate_possibility(attack_right, board):
                        self.attack_list += [attack_right]

        elif self.color == 'b':

            forward = [current_position[0] + 1, current_position[1]]
            if not board.board[forward[0]][forward[1]]:
                if self.validate_possibility(forward, board):
                    self.move_list += [forward]
                forward_two = [current_position[0] + 2, current_position[1]]
                if not self.move_counter and not board.board[forward_two[0]][forward_two[1]]:
                    if self.validate_possibility(forward_two, board):
                        self.move_list += [forward_two]

            attack_left = [current_position[0] + 1, current_position[1] - 1]
            if board.board[attack_left[0]][attack_left[1]]:
                if board.board[attack_left[0]][attack_left[1]].color == 'w':
                    if self.validate_possibility(attack_left, board):
                        self.attack_list += [attack_left]

            attack_right = [current_position[0] + 1, current_position[1] + 1]
            if board.board[attack_right[0]][attack_right[1]]:
                if board.board[attack_right[0]][attack_right[1]].color == 'w':
                    if self.validate_possibility(attack_right, board):
                        self.attack_list += [attack_right]

        return 
    #TODO: add ability to promote to queen if it reaches end of board

