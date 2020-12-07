import os
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

	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.move_list = []

class King(Piece):

	
    def valid_moves(self, board):
        position = [self.row, self.col]

        def off_board(move):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                self.move_list += [move]
            return

        def same_color_piece(move):
            if board.board[move[0]][move[1]].color == self.color:
                self.move_list.pop()
            return

        up = [position[0] - 1, position[1]]
        down = [position[0] + 1, position[1]]
        right = [position[0], position[1] + 1]
        left = [position[0], position[1] - 1]
        down_right = [position[0] + 1, position[1] + 1]
        up_right = [position[0] - 1, position[1] + 1]
        down_left = [position[0] + 1, position[1] - 1]
        up_left = [position[0] - 1, position[1] - 1]
        
        possible_moves = [up,down,left,right,down_left,down_right,up_left,up_right]

        for move in possible_moves:
            off_board(move)
            same_color_piece(move)

        #TODO: kings cannot move into check
        #TODO: Castling to the left and right if the king has not moved and the castling rook has not moved

class Queen(Piece):

    def valid_moves(self, board):
        current_position = [self.row, self.col]

        def off_board(move):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                self.move_list += [move]
            return

        def same_color_piece(move):
            if board.board[move[0]][move[1]].color == self.color:
                self.move_list.pop()
            return
        
        up = current_position[0] 
        
    #TODO: build the moves checking


class Knight(Piece):

    def valid_moves(self, board):
        def off_board(move):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                self.move_list += [move]
            return

        def same_color_piece(move):
            if board.board[move[0]][move[1]].color == self.color:
                self.move_list.pop()
            return
    #TODO: build the moves checking

class Bishop(Piece):

    def valid_moves(self, board):
        current_position = [self.row, self.col]

        def not_off_board(row, col):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                return True

        def same_color_piece(move):
            if board.board[move[0]][move[1]]:
                if board.board[move[0]][move[1]].color == self.color:
                    return True

        def diagonal_north_west():
            position = [current_position[0] - 1, current_position[1] - 1]
            while not_off_board(position) and not same_color_piece(position):
                temp_position = position
                self.move_list += [temp_position]
                position = [position[0] -1, position[1] - 1]
            return
        
        def diagonal_north_east():
            position = [current_position[0] - 1, current_position[1] + 1]
            while not_off_board(position) and not same_color_piece(position):
                temp_position = position
                self.move_list += [temp_position]
                position = [position[0] - 1, position[1] + 1]
            return

        def diagonal_south_east():
            position = [current_position[0] + 1, current_position[1] + 1]
            while not_off_board(position) and not same_color_piece(position):
                temp_position = position
                self.move_list += [temp_position]
                position = [position[0] + 1, position[1] + 1]
            return

        def diagonal_south_west():
            position = [current_position[0] + 1, current_position[1] - 1]
            while not_off_board(position) and not same_color_piece(position):
                temp_position = position
                self.move_list += [temp_position]
                position = [position[0] + 1, position[1] - 1]
            return
        
        diagonal_north_west()
        diagonal_north_east()
        diagonal_south_east()
        diagonal_south_west()

class Rook(Piece):

    def valid_moves(self, board):
        current_position = [self.row,self.col]
        def not_off_board(move):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                return True

        def same_color_piece(move):
            if board.board[move[0]][move[1]]:
                if board.board[move[0]][move[1]].color == self.color:
                    return True

        def left():
            position = [current_position[0] - 1, current_position[1]]
            while not_off_board(position) and not same_color_piece(position):
                self.move_list += [position]
                position[0] += -1
            return
        def right():
            position = [current_position[0] + 1, current_position[1]]
            while not_off_board(position) and not same_color_piece(position):
                self.move_list += [position]
                position[0] += 1
            return
        def up():
            position = [current_position[0], current_position[1] + 1]
            while not_off_board(position) and not same_color_piece(position):
                self.move_list += [position]
                position[1] += 1
            return
        def down():
            position = [current_position[0], current_position[1] - 1]
            while not_off_board(position) and not same_color_piece(position):
                self.move_list += [position]
                position[1] += -1
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
    def valid_moves(self, board):
        def not_off_board(move):
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                return True

        def same_color_piece(move):
            if board.board[move[0]][move[1]]:
                if board.board[move[0]][move[1]].color == self.color:
                    return True

        def validate_possibility(move):
            if not_off_board(move) and not same_color_piece(move):
                self.move_list += [move]

        current_position = [self.row, self.col]
        move_counter = 0
        if self.color == 'w':
            if not move_counter:
                forward_two = [current_position[0] - 2, current_position[1]]
                validate_possibility(forward_two)
            forward = [current_position[0] - 1, current_position[1]]
            validate_possibility(forward)
            if board.board[current_position[0] - 1][current_position[1] - 1]:
                if board.board[current_position[0] - 1][current_position[1] - 1].color == 'b':
                    attack_left = [current_position[0] - 1, current_position[1] - 1]
                    validate_possibility(attack_left)
            if board.board[current_position[0] - 1][current_position[1] + 1]:
                if board.board[current_position[0] - 1][current_position[1] + 1].color == 'b':
                    attack_right = [current_position[0] - 1, current_position[1] + 1]
                    validate_possibility(attack_right)

        elif self.color == 'b':
            if not move_counter:
                forward_two = [current_position[0] + 2, current_position[1]]
                validate_possibility(forward_two)
            forward = [current_position[0] + 1, current_position[1]]
            validate_possibility(forward)
            if board.board[current_position[0] + 1][current_position[1] - 1]:
                if board.board[current_position[0] + 1][current_position[1] - 1].color == 'w':
                    attack_left = [current_position[0] + 1, current_position[1] - 1]
                    validate_possibility(attack_left)
            if board.board[current_position[0] + 1][current_position[1] + 1]:
                if board.board[current_position[0] + 1][current_position[1] + 1].color == 'w':
                    attack_right = [current_position[0] + 1, current_position[1] + 1]
                    validate_possibility(attack_right)
        
        return 
    #TODO: build the moves checking
    #TODO: fix up same color piece check, it seems to always pop out all the solutions
