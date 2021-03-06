from pieces import Rook, Knight, Bishop, Queen, King, Pawn
from copy import deepcopy

class Board:
    '''
    The board class keeps track of all the pieces in on the 8 by 8 chess board grid. It keeps track of whose turn it is
    '''
    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)]
        self.player_turn = 'w'
        self.white_king_location = 0
        self.black_king_location = 0
        # self.reset_pieces()

    def reset_pieces(self):

        self.board[0][0] = Rook(0, 0, 'b')
        self.board[0][1] = Knight(0, 1, 'b')
        self.board[0][2] = Bishop(0, 2, 'b')
        self.board[0][3] = Queen(0, 3, 'b')
        self.board[0][4] = King(0, 4, 'b')
        self.board[0][5] = Bishop(0, 5, 'b')
        self.board[0][6] = Knight(0, 6, 'b')
        self.board[0][7] = Rook(0, 7, 'b')

        self.board[1][0] = Pawn(1, 0, 'b')
        self.board[1][1] = Pawn(1, 1, 'b')
        self.board[1][2] = Pawn(1, 2, 'b')
        self.board[1][3] = Pawn(1, 3, 'b')
        self.board[1][4] = Pawn(1, 4, 'b')
        self.board[1][5] = Pawn(1, 5, 'b')
        self.board[1][6] = Pawn(1, 6, 'b')
        self.board[1][7] = Pawn(1, 7, 'b')

        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][3] = Queen(7, 3, 'w')
        self.board[7][4] = King(7, 4, 'w')
        self.board[7][5] = Bishop(7, 5, 'w')
        self.board[7][6] = Knight(7, 6, 'w')
        self.board[7][7] = Rook(7, 7, 'w')

        self.board[6][0] = Pawn(6, 0, 'w')
        self.board[6][1] = Pawn(6, 1, 'w')
        self.board[6][2] = Pawn(6, 2, 'w')
        self.board[6][3] = Pawn(6, 3, 'w')
        self.board[6][4] = Pawn(6, 4, 'w')
        self.board[6][5] = Pawn(6, 5, 'w')
        self.board[6][6] = Pawn(6, 6, 'w')
        self.board[6][7] = Pawn(6, 7, 'w')
    
    def empty_board(self, x, y):
        if self.board[x][y] == '0':
            return True
        else:
            return False

    def display_board(self):
        pass
        #TODO: render information with arcade

    def remove_piece(self, piece):
        pass
        #TODO: call the piece method to update move_list, then check the list and highlight open tiles blue and tiles that can be attacked on red

    def checkmate_status(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                current_piece = self.board[i][j]

                if current_piece:
                    if self.player_turn == current_piece.color:
                        # if current_piece.move_list:
                        current_piece.test_if_your_king_is_in_check(self)
                        if current_piece.move_list:
                            print('checkmate false due to move list')
                            return False

                        # if current_piece.attack_list:
                        current_piece.test_if_your_king_is_in_check(self)
                        if current_piece.attack_list:
                            print('checkmate false due to attack list')
                            return False

        return True
               
            

        # make temp list of all moves
        # run each move through a temporary board
        # check status of that temporary board
        # if any status comes back false, then checkmate_status comes back false

        #TODO: build checks for units that can currently attack the selected piece and highlight the tile orange

    def check_status(self):

        temp_black_attack_list = []
        temp_white_attack_list = []

        try:
            for i in range(0,8):
                for j in range(0,8):
                    if self.board[i][j]:
                        if isinstance(self.board[i][j], King) and self.board[i][j].color == 'w':
                            print('white king location', self.white_king_location)
                            self.white_king_location = [i,j]
                        elif isinstance(self.board[i][j], King) and self.board[i][j].color == 'b':
                            self.black_king_location = [i,j]
                        elif self.board[i][j].color == "b":
                            temp_black_attack_list += self.board[i][j].attack_list 
                        elif self.board[i][j].color == "w":
                            temp_white_attack_list += self.board[i][j].attack_list 
            
            for attacks in temp_black_attack_list:
                if attacks == self.white_king_location:
                    return 'w'
            for attacks in temp_white_attack_list:
                if attacks == self.black_king_location:
                    return 'b'
            
        except:
            return False
        return False

    def move(self, start_position, end_position):

        '''
        To move a piece, we first make sure that the piece color matches the players turn color (white should move white
        pieces). If there is a piece on the selected end position, then we validate moves from the attack list and replace 
        the end position piece with the moving piece if it is a valid move. If there is not a piece on the end position, we 
        simply copy that piece onto the end position and remove it from the start position. After every move, we must change 
        the current players turn to reflect the actual current colors turn.
        '''

        start = self.board[start_position[0]][start_position[1]]
        end = self.board[end_position[0]][end_position[1]]

        if not start:
            print('Please choose a piece on the board')
            return   

        if not start.color == self.player_turn:
            print('Other player\'s turn')   
            return

        if start.color == self.player_turn: # does the turn match the piece color
            if not end: # does the end position contain a unit 
               
                for move in start.move_list: # go through the valid moves
                    
                    if move == end_position: # if a valid move matches the end position, then do the move
                        start.row = end_position[0]
                        start.col = end_position[1]

                        self.board[end_position[0]][end_position[1]] =  start
                        self.board[start_position[0]][start_position[1]] = 0

                        self.board[end_position[0]][end_position[1]].move_counter += 1
                        self.board[end_position[0]][end_position[1]].move_list = []
                        self.board[end_position[0]][end_position[1]].valid_moves(self)
                        if self.player_turn == 'w':
                            self.player_turn = 'b'
                        elif self.player_turn == 'b':
                            self.player_turn = 'w'

            elif end: # if the end position is not empty (i.e. there is an opponent on that square)
                
                for attack in start.attack_list: # check the valid attacks
                    
                    if attack == end_position: # if the end position is a valid attack, move the piece and remove the opponent's piece
                        self.board[end_position[0]][end_position[1]] = 0
                        start.row = end_position[0] # updated the current row for the piece
                        start.col = end_position[1] # update the current column for the piece
                        self.board[end_position[0]][end_position[1]] =  start # append the board at the end position with the piece
                        self.board[start_position[0]][start_position[1]] = 0 # clear the startin square
                        self.board[end_position[0]][end_position[1]].move_list = [] # clear the previous move lists
                        self.board[end_position[0]][end_position[1]].move_counter += 1 # increment the counter
                        self.board[end_position[0]][end_position[1]].valid_moves(self) # update the valid moves
                        if self.player_turn == 'w':
                            self.player_turn = 'b'
                        elif self.player_turn == 'b':
                            self.player_turn = 'w'
            else: 
                print('Invalid move, try another move')
            # no matter what happens, if a move is completed change the player turn

        #TODO: validate for checking and not moving into check
        #TODO: update move_counter or remove move_counter
        #TODO: update move_list with the moves from the new position
