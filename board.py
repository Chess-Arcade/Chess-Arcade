from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class Board:

    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)]
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

    def check_units_moves(self, piece):
        pass
        #TODO: call the piece method to update move_list, then check the list and highlight open tiles blue and tiles that can be attacked on red

    def check_units_attackers(self, piece):
        pass
        #TODO: build checks for units that can currently attack the selected piece and highlight the tile orange

    def check_checked_status(self, color):
        pass
        #TODO: build something to check for a check position

    def move(self, piece):
        pass
        #TODO: build something to register user input movements and update the board