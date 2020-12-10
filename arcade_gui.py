import arcade
import ctypes
# from AppKit import NSScreen

###Constants###

# Screen title and size
if hasattr(ctypes, 'windll'):
	user32 = ctypes.windll.user32
	SCREEN_WIDTH = user32.GetSystemMetrics(0)
	SCREEN_HEIGHT = user32.GetSystemMetrics(1)
else:
	# SCREEN_WIDTH = NSScreen.mainScreen().frame().size.width
	# SCREEN_HEIGHT = NSScreen.mainScreen().frame().size.height
	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720

SCREEN_TITLE = "Chess"

#Square side
SQUARE_HEIGHT = SQUARE_WIDTH = int((SCREEN_HEIGHT*.9) / 8)

#Piece_Size
PIECE_HEIGHT = PIECE_WIDTH = int(SQUARE_HEIGHT*.6)

#Start pos
START_X = SCREEN_WIDTH*.1
START_Y = SCREEN_HEIGHT*.1

#Pieces
PIECE_COLORS = ['White', 'Black']
PIECES = ['Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']

class Piece(arcade.Sprite):
	""" piece sprite """

	def __init__(self, colour, piece, scale=1):
		""" Piece constructor """

		# Attributes for colour and piece
		self.colour = colour
		self.piece = piece
		self.move_list = []
		self.attack_list = []
		self.move_counter = 0

		#Image to use for the sprite
		self.image_file_name = f'assets/images/{self.colour}_{self.piece}.png'
		super().__init__(self.image_file_name, scale)

class King(Piece):
	'''
	The king can move one space in any direction as long as there is no piece of the same color on that square, 
	that square is not off the board, and there is no piece that would put the king in check if the king were to 
	move to that square. If the king has not moved yet, and neither has the rook with which it wants to castle, 
	the king can step over two squares towards the rook and have the rook hop directly over the king to the adjacent
	square. Castling can only occur if there is no piece of the same color sitting on any of the tiles being traversed, 
	and so long as the king is not placed in check along its path.
	'''

	def __init__(self, colour, scale=1):
		self.been_checked = False
		super().__init__(colour, 'King', scale)

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()
		position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list
		possible_moves = []
		king_positon = 7 if self.colour == 'White' else 0
		# check if the king has not moved, check if the corresponding rook has not moved
		# check that the tiles the king is moving over are not cover
		# check if the tiles the king is moving over are not under attack

		def move(y_inc, x_inc):
			if not 0 > position[1]+x_inc and not position[1]+x_inc > 7 and not 0 > position[0]+y_inc and not position[0]+y_inc > 7:
				possible_moves.append((position[0]+y_inc, position[1]+x_inc))

		move(1,0)
		move(1,1)
		move(1,-1)
		move(-1,0)
		move(-1,1)
		move(-1,-1)
		move(0,1)
		move(0,-1)

		if self.move_counter == 0:
			if board.tiles[king_positon][7]:
				if board.tiles[king_positon][7].move_counter == 0:
					if not board.tiles[king_positon][5] and not board.tiles[king_positon][6]:
						possible_moves.append((position[0],position[1] + 2))

			if board.tiles[king_positon][0]:
				if board.tiles[king_positon][0].move_counter == 0:
					if not board.tiles[king_positon][1] and not board.tiles[king_positon][2] and not board.tiles[king_positon][3]: 
						possible_moves.append((position[0],position[1] - 2))
	   
		for move in possible_moves:
			if board.tiles[move[0]][move[1]]:
				if board.tiles[move[0]][move[1]] in enemy_piece_list:
			  		self.attack_list.append((move[0],move[1]))
			else:
			  	self.move_list.append((move[0],move[1]))

		#TODO: kings cannot move into check	
		#TODO: Castling to the left and right if the king has not moved and the castling rook has not moved

class Queen(Piece):

	def __init__(self, colour, scale=1):
		super().__init__(colour, 'Queen', scale)

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()

		current_position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list

		def move(y_inc, x_inc):
			position = [current_position[0] + y_inc, current_position[1] + x_inc]
			for i in range(7):
				if 0 > position[1] or position[1] > 7 or 0 > position[0] or position[0] > 7:
					break
				if board.tiles[position[0]][position[1]]:
					if board.tiles[position[0]][position[1]] in enemy_piece_list:
						self.attack_list.append((position[0], position[1]))
					break
				else:
					self.move_list.append((position[0], position[1]))
				position[0] += y_inc
				position[1] += x_inc

		move(1,0)
		move(-1,0)
		move(0,1)
		move(0,-1)
		move(1,1)
		move(-1,1)
		move(1,-1)
		move(-1,-1)

class Knight(Piece):

	def __init__(self, colour, scale=1):
		super().__init__(colour, 'Knight', scale)

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()

		position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list
		possible_moves = []
		
		def move(y_inc, x_inc):
			if not 0 > position[1]+x_inc and not position[1]+x_inc > 7 and not 0 > position[0]+y_inc and not position[0]+y_inc > 7:
				possible_moves.append((position[0]+y_inc, position[1]+x_inc))

		move(2,-1)
		move(2,1)
		move(1,2)
		move(1,-2)
		move(-1,2)
		move(-1,-2)
		move(-2,1)
		move(-2,-1)

		for move in possible_moves:
			if board.tiles[move[0]][move[1]]:
				if board.tiles[move[0]][move[1]] in enemy_piece_list:
					self.attack_list.append(move)
			else:
				self.move_list.append(move)

	#TODO: build the moves checking

class Bishop(Piece):

	def __init__(self, colour, scale=1):
		super().__init__(colour, 'Bishop', scale)

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()

		current_position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list

		def move(y_inc, x_inc):
			position = [current_position[0] + y_inc, current_position[1] + x_inc]
			for i in range(7):
				if 0 > position[1] or position[1] > 7 or 0 > position[0] or position[0] > 7:
					break
				if board.tiles[position[0]][position[1]]:
					if board.tiles[position[0]][position[1]] in enemy_piece_list:
						self.attack_list.append((position[0], position[1]))
					break
				else:
					self.move_list.append((position[0], position[1]))
				position[0] += y_inc
				position[1] += x_inc

		move(-1,-1)
		move(-1,1)
		move(1,-1)
		move(1,1)

class Rook(Piece):

	def __init__(self, colour, scale=1):
		super().__init__(colour, 'Rook', scale)

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()

		current_position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list

		def move(y_inc, x_inc):
			position = [current_position[0] + y_inc, current_position[1] + x_inc]
		   
			for i in range (7):
				if 0 > position[1] or position[1] > 7 or 0 > position[0] or position[0] > 7:
					break
				if board.tiles[position[0]][position[1]]:
					if board.tiles[position[0]][position[1]] in enemy_piece_list:
						self.attack_list.append((position[0], position[1]))
					break
				else:
			   		self.move_list.append((position[0], position[1]))
				position[0] += y_inc
				position[1] += x_inc

		move(1,0)
		move(-1,0)
		move(0,1)
		move(0,-1)
	#TODO: build the moves checking

class Pawn(Piece):

	def __init__(self, colour, scale=1):
		super().__init__(colour, 'Pawn', scale)

	def promote(self, board):
		current_position = board.get_tile_for_piece(self)
		new_queen = Queen(self.colour, .9*(SCREEN_WIDTH/2480))
		piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list
		piece_list.remove(self)
		piece_list.append(new_queen)
		board.tiles[current_position[0], current_position[1]] = new_queen

	def valid_moves(self, board):

		self.move_list.clear()
		self.attack_list.clear()

		current_position = board.get_tile_for_piece(self)
		enemy_piece_list = board.black_piece_list if self.colour == 'White' else board.white_piece_list
		direction = -1 if self.colour == 'White' else 1

		if not board.tiles[current_position[0]+direction][current_position[1]]:
			self.move_list.append((current_position[0]+direction, current_position[1]))
			if not self.move_counter and not board.tiles[current_position[0]+2*direction][current_position[1]]:
				self.move_list.append((current_position[0]+2*direction, current_position[1]))

		if current_position[1] != 0:
			if board.tiles[current_position[0]+direction][current_position[1]-1] in enemy_piece_list:
				self.attack_list.append((current_position[0]+direction, current_position[1]-1))

		if current_position[1] != 7:
			if board.tiles[current_position[0]+direction][current_position[1]+1] in enemy_piece_list:
				self.attack_list.append((current_position[0]+direction, current_position[1]+1))
	#TODO: add ability to promote to queen if it reaches end of board




















class MyGame(arcade.Window):
	"""main application class."""

	def __init__(self):

		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

		#Sprite list with all the pieces
		self.white_piece_list = None
		self.black_piece_list = None

		#grave counts
		self.black_pieces_captured = None
		self.white_pieces_captured = None


		arcade.set_background_color(arcade.color.ARSENIC)

		# Piece being dragged
		self.held_piece = None
		self.held_piece_origin = None

		# Board Tiles
		self.tile_list = None

		#matrix
		self.tiles = None

		#move sequence
		self.move_sequence = None

		self.turn = 'W'

	def end_turn(self):
		for piece in self.white_piece_list:
			for row in self.tiles:
				if piece in row:
					piece.valid_moves(self)
		for piece in self.black_piece_list:
			for row in self.tiles:
				if piece in row:
					piece.valid_moves(self)
		self.redraw_tiles()

	def redraw_tiles(self):
		
		self.tile_list: arcade.SpriteList = arcade.SpriteList()

		for row in range(8):
			for column in range(8):
				if (column+row)%2 == 0:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (85,85,85))
				else:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (245,245,245))
				tile.position = START_X+(SQUARE_WIDTH*column), START_Y+(SQUARE_HEIGHT*row)
				self.tile_list.append(tile)

	def undo_move(self):

		if len(self.move_sequence):
			for i in range(len(self.move_sequence[-1])):
				if i % 4 == 0:
					if i == 0:
						self.move_sequence[-1][i].move_counter -= 1
					print(self.move_sequence[-1][i].move_counter)
					self.move_sequence[-1][i].position = self.move_sequence[-1][i+1]
					self.tiles[self.move_sequence[-1][i+2][0]][self.move_sequence[-1][i+2][1]] = self.move_sequence[-1][i]
					if self.move_sequence[-1][i+3]:
						self.tiles[self.move_sequence[-1][i+3][0]][self.move_sequence[-1][i+3][1]] = None
			self.turn = 'W' if self.turn == 'B' else 'B'
			self.move_sequence.pop(-1)
			self.end_turn()

	def setup(self):
		""" Set up game here, call this to restart """

		# Sprite List for tiles
		self.tile_list: arcade.SpriteList = arcade.SpriteList()

		# tiles content list
		self.tiles = []

		self.move_sequence = []

		# Place tile sprites
		for row in range(8):
			self.tiles.append([])
			for column in range(8):
				if (column+row)%2==0:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (85,85,85))
				else:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (245,245,245))
				tile.position = START_X+(SQUARE_WIDTH*column), START_Y+(SQUARE_HEIGHT*row)
				self.tile_list.append(tile)
				self.tiles[row].append(None)
		# 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13 -> 14 -> 15 -> 16
		# 0.0 -> 0.1 -> 0.2 -> 0.3 -> 0.4 -> 0.5 -> 0.6 -> 0.7 -> 1.0 -> 1.1 -> 1.2 -> 1.3 -> 1.4 -> 1.5 -> 1.6 -> 1.7 -> 2.0

		# Set piece lists
		self.white_piece_list = arcade.SpriteList()
		self.black_piece_list = arcade.SpriteList()

		# Set captured counters
		self.white_pieces_captured = 0
		self.black_pieces_captured = 0

		#Set whites turn
		self.turn = 'W'

		# Create Pieces
		for cind, colour in enumerate(PIECE_COLORS):
			for pind, piece_type in enumerate(PIECES):
				if piece_type == 'Knight': 
					piece = Knight(colour, .7*(SCREEN_WIDTH/2480))
				elif piece_type == 'Rook':
					piece = Rook(colour, .75*(SCREEN_WIDTH/2480))
				else:
					piece = eval(piece_type)(colour, .9*(SCREEN_WIDTH/2480))
				if colour == 'Black':
					if piece_type == 'Pawn':
						piece.position = START_X+(SQUARE_WIDTH*pind), START_Y+(SQUARE_HEIGHT*6)
						self.tiles[1][pind] = piece
					else:
						piece.position = START_X+(SQUARE_WIDTH*(pind-8)), START_Y+(SQUARE_HEIGHT*7)
						self.tiles[0][pind-8] = piece
					self.black_piece_list.append(piece)
				else:
					if piece_type == 'Pawn':
						piece.position = START_X+(SQUARE_WIDTH*pind), START_Y+SQUARE_HEIGHT
						self.tiles[6][pind] = piece
					else:
						piece.position = START_X+(SQUARE_WIDTH*(pind-8)), START_Y
						self.tiles[7][pind-8] = piece
					self.white_piece_list.append(piece)
		self.end_turn()

	def get_tile_for_piece(self, piece):
		""" what tile is this piece on? """
		for y_index, row in enumerate(self.tiles):
			for x_index, column in enumerate(row):
				if piece == column:
					return (y_index, x_index)

	def on_draw(self):
		""" Render the screen. """

		#clear screen
		arcade.start_render()

		#draw the board
		self.tile_list.draw()

		#draw the pieces
		self.black_piece_list.draw()
		self.white_piece_list.draw()

	def on_mouse_press(self, x, y, button, key_modifiers):
		""" called when the user presser a mouse button """

		# get piece clicked on, only allow own units
		if self.turn == 'W':
			piece = arcade.get_sprites_at_point((x,y), self.white_piece_list)
		else:
			piece = arcade.get_sprites_at_point((x,y), self.black_piece_list)

		#check that a sprite was clicked
		if len(piece) > 0:

			# get the tile clicked
			current_tile_coord = self.get_tile_for_piece(piece[0])

			# check that the piece existed as tile content
			if current_tile_coord:
				# adjust held piece information
				self.held_piece = piece[0]
				# save origin for returning piece
				self.held_piece_origin = piece[0].position

				acceptable_moves = self.held_piece.move_list
				acceptable_attacks = self.held_piece.attack_list

				#do highlighting
				for movement in acceptable_moves:
					sprite_index = (7-movement[0])*8+movement[1]
					# highlight_tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (200,200,0))
					# highlight_tile.position = self.tile_list[sprite_index].position
					# self.tile_list.pop(sprite_index)
					# self.tile_list.insert(sprite_index, highlight_tile)
					if (movement[0]+movement[1])%2==0:
						self.tile_list[sprite_index].color = (0,145,145)
					else:
						self.tile_list[sprite_index].color = (0,255,255)
				for movement in acceptable_attacks:
					sprite_index = (7-movement[0])*8+movement[1]
					# highlight_tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, (200,0,0))
					# highlight_tile.position = self.tile_list[sprite_index].position
					# self.tile_list.pop(sprite_index)
					# self.tile_list.insert(sprite_index, highlight_tile)
					if (movement[0]+movement[1])%2==0:
						self.tile_list[sprite_index].color = (145,0,0)
					else:
						self.tile_list[sprite_index].color = (255,0,0)

	def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
		""" Called when the user moves mouse """

		# if holding an item move with mouse
		if self.held_piece:

			#movement tracking
			self.held_piece.center_x += dx
			self.held_piece.center_y += dy

	def on_mouse_release(self, x:float, y: float, button: int, modifiers: int):
		""" Called when the user presses a mouse button """

		enemy_colour = 'B' if self.turn == 'W' else 'W'
		enemy_pieces = self.black_piece_list if self.turn == 'W' else self.white_piece_list

		# Check if a piece was held
		if not self.held_piece:
			return

		acceptable_moves = self.held_piece.move_list
		acceptable_attacks = self.held_piece.attack_list
		# Find the closest tile in case of overlap
		tile, distance = arcade.get_closest_sprite(self.held_piece, self.tile_list)
		# create reset variable with default True
		reset_position = True

		if arcade.check_for_collision(self.held_piece, tile):

			tile_index = self.tile_list.index(tile)
			tile_index_y = 7-int(tile_index//8)
			tile_index_x = tile_index%8
			new_tile = self.tiles[tile_index_y][tile_index_x]
			old_tile = self.get_tile_for_piece(self.held_piece)

			if old_tile == (tile_index_y, tile_index_x):
				#TODO: build highlighting
				pass

			elif (tile_index_y, tile_index_x) not in acceptable_moves and (tile_index_y, tile_index_x) not in acceptable_attacks:
				pass

			elif new_tile in enemy_pieces:
				self.move_sequence.append((self.held_piece, self.held_piece_origin, old_tile, (tile_index_y, tile_index_x), new_tile, new_tile.position, (tile_index_y, tile_index_x), None))
				if enemy_colour == 'W':
					if self.white_pieces_captured < 8:
						new_tile.position = START_X+SQUARE_WIDTH*8, \
											START_Y+(SQUARE_HEIGHT*self.white_pieces_captured)
					else:
						new_tile.position = START_X+SQUARE_WIDTH*9, \
											START_Y+(SQUARE_HEIGHT*(self.white_pieces_captured-8))
					self.white_pieces_captured += 1
				else:
					if self.black_pieces_captured < 8:
						new_tile.position = START_X+SQUARE_WIDTH*10, \
											START_Y+(SQUARE_HEIGHT*self.black_pieces_captured)
					else:
						new_tile.position = START_X+SQUARE_WIDTH*11, \
											START_Y+(SQUARE_HEIGHT*(self.black_pieces_captured-8))
					self.black_pieces_captured += 1
				self.held_piece.position = tile.center_x, \
											tile.center_y
				self.tiles[tile_index_y][tile_index_x] = self.held_piece
				self.held_piece.move_counter += 1
				self.turn = 'W' if self.turn == 'B' else 'B'
				self.tiles[old_tile[0]][old_tile[1]] = None
				reset_position = False

			elif self.held_piece.piece == 'King' and (abs(old_tile[1]-tile_index_x)) > 1:
				self.tiles[tile_index_y][tile_index_x] = self.held_piece
				self.held_piece.position = tile.center_x, \
											tile.center_y
				if tile_index_x > old_tile[1]:
					castled_rook = self.tiles[tile_index_y][tile_index_x+1]
					old_pos = castled_rook.position
					rook_old_shift = 1
					rook_new_shift = -1
					self.tiles[tile_index_y][tile_index_x-1] = castled_rook
					castled_rook.position = tile.center_x-SQUARE_WIDTH, \
											tile.center_y
				else:
					castled_rook = self.tiles[tile_index_y][tile_index_x-2]
					old_pos = castled_rook.position
					rook_old_shift = -2
					rook_new_shift = 1
					self.tiles[tile_index_y][tile_index_x+1] = castled_rook
					castled_rook.position = tile.center_x+SQUARE_WIDTH, \
											tile.center_y
				self.move_sequence.append((self.held_piece, self.held_piece_origin, old_tile, (tile_index_y, tile_index_x), castled_rook, old_pos, (tile_index_y, tile_index_x+rook_old_shift), (tile_index_y, tile_index_x+rook_new_shift)))
				self.held_piece.move_counter += 1
				self.turn = 'W' if self.turn == 'B' else 'B'
				self.tiles[old_tile[0]][old_tile[1]] = None
				reset_position = False

			elif new_tile is None:
				self.tiles[tile_index_y][tile_index_x] = self.held_piece
				self.held_piece.position = tile.center_x, \
											tile.center_y
				self.move_sequence.append((self.held_piece, self.held_piece_origin, old_tile, (tile_index_y, tile_index_x)))
				self.turn = 'W' if self.turn == 'B' else 'B'
				self.tiles[old_tile[0]][old_tile[1]] = None
				self.held_piece.move_counter += 1
				reset_position = False

		if reset_position:
			self.held_piece.position = self.held_piece_origin

		self.held_piece = None
		self.end_turn()


	def on_key_press(self, symbol: int, modifiers: int):
		""" User presses key """
		if symbol == arcade.key.R:
			# Restart
			self.setup()

		if symbol == arcade.key.Z:
			#undo
			self.undo_move()

def main():
	""" Main method """
	window = MyGame()
	window.setup()
	arcade.run()

if __name__ == "__main__":
	main()