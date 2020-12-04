import os
from board import board

b_bishop = pygame.image.load(os.path.join('assets', 'black_bishop.png'))
b_king = pygame.image.load(os.path.join('assets', 'black_king.png'))
b_knight = pygame.image.load(os.path.join('assets', 'black_knight.png'))
b_pawn = pygame.image.load(os.path.join('assets', 'black_pawn.png'))
b_queen = pygame.image.load(os.path.join('assets', 'black_queen.png'))
b_rook = pygame.image.load(os.path.join('assets', 'black_rook.png'))

w_bishop = pygame.image.load(os.path.join('assets', 'white_bishop.png'))
w_king = pygame.image.load(os.path.join('assets', 'white_king.png'))
w_knight = pygame.image.load(os.path.join('assets', 'white_knight.png'))
w_pawn = pygame.image.load(os.path.join('assets', 'white_pawn.png'))
w_queen = pygame.image.load(os.path.join('assets', 'white_queen.png'))
w_rook = pygame.image.load(os.path.join('assets', 'white_rook.png'))

class Piece:

	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.move_list = []

class King(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking

class Queen(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking


class Knight(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking

class Bishop(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking

class Rook(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking

class Pawn(Piece):

	def valid_moves(self, board):

		#TODO: build the moves checking
