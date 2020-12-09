import arcade
import ctypes

###Constants###

# Screen title and size
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)
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

#Piece offset in tile
PIECE_OFFSET_X = PIECE_OFFSET_Y = round(SQUARE_HEIGHT*.1)

class Piece(arcade.Sprite):
	""" piece sprite """

	def __init__(self, colour, piece, scale=.7):
		""" Piece constructor """

		# Attributes for colour and piece
		self.colour = colour
		self.piece = piece

		#Image to use for the sprite
		self.image_file_name = f'assets/images/{self.colour}_{self.piece}.png'
		super().__init__(self.image_file_name, scale)

class MyGame(arcade.Window):
	"""main application class."""

	def __init__(self):

		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

		#Sprite list with all the pieces
		self.white_piece_list = None
		self.black_piece_list = None

		arcade.set_background_color(arcade.color.ARSENIC)

		# Piece being dragged
		self.held_piece = None
		self.held_piece_origin = None

		# Board Tiles
		self.tile_list = None

		#matrix
		self.tiles = None

		self.turn = 'W'

	def setup(self):
		""" Set up game here, call this to restart """

		# Sprite List for tiles
		self.tile_list: arcade.SpriteList = arcade.SpriteList()

		# tiles content list
		self.tiles = []

		# Place tile sprites
		for row in range(8):
			self.tiles.append([])
			for column in range(8):
				if (column+row)%2==0:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, arcade.csscolor.WHITE)
				else:
					tile = arcade.SpriteSolidColor(SQUARE_HEIGHT, SQUARE_WIDTH, arcade.csscolor.BLACK)
				tile.position = START_X+(SQUARE_WIDTH*column), START_Y+(SQUARE_HEIGHT*row)
				self.tile_list.append(tile)
				self.tiles[row].append(None)

		# Set piece lists
		self.white_piece_list = arcade.SpriteList()
		self.black_piece_list = arcade.SpriteList()

		# Create Pieces
		for cind, colour in enumerate(PIECE_COLORS):
			for pind, piece_type in enumerate(PIECES):
				piece = Piece(colour, piece_type)
				if colour == 'Black':
					if piece_type == 'Pawn':
						piece.position = START_X+(SQUARE_WIDTH*pind)+PIECE_OFFSET_X, START_Y+(SQUARE_HEIGHT*6)+PIECE_OFFSET_Y
						self.tiles[1][pind] = piece
					else:
						piece.position = START_X+(SQUARE_WIDTH*(pind-8))+PIECE_OFFSET_X, START_Y+(SQUARE_HEIGHT*7)+PIECE_OFFSET_Y
						self.tiles[0][pind-8] = piece
					self.black_piece_list.append(piece)
				else:
					if piece_type == 'Pawn':
						piece.position = START_X+(SQUARE_WIDTH*pind)+PIECE_OFFSET_X, START_Y+SQUARE_HEIGHT+PIECE_OFFSET_Y
						self.tiles[6][pind] = piece
					else:
						piece.position = START_X+(SQUARE_WIDTH*(pind-8))+PIECE_OFFSET_X, START_Y+PIECE_OFFSET_Y
						self.tiles[7][pind-8] = piece
					self.white_piece_list.append(piece)

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

	def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
		""" Called when the user moves mouse """

		# if holding an item move with mouse
		if self.held_piece:
			self.held_piece.center_x += dx
			self.held_piece.center_y += dy

	def on_mouse_release(self, x:float, y: float, button: int, modifiers: int):
		""" Called when the user presses a mouse button """

		enemy_colour = 'B' if self.turn == 'W' else 'W'
		enemy_pieces = self.black_piece_list if self.turn == 'W' else self.white_piece_list

		# Check if a piece was held
		if not self.held_piece:
			return

		# Find the closest tile in case of overlap
		tile, distance = arcade.get_closest_sprite(self.held_piece, self.tile_list)
		# create reset variable with default True
		reset_position = True

		if arcade.check_for_collision(self.held_piece, tile):

			tile_index = self.tile_list.index(tile)
			tile_index_y = 7-int(tile_index//8)
			tile_index_x = tile_index%8
			new_tile = self.tiles[tile_index_y][tile_index_x]

			if self.get_tile_for_piece(self.held_piece) == (tile_index_y, tile_index_x):
				#TODO: build highlighting
				pass

			elif new_tile in enemy_pieces:
				print('enemy spotted')
				if enemy_colour == 'W':
					new_tile.position = START_X+SQUARE_WIDTH*9, \
										START_Y+PIECE_OFFSET_Y
				else:
					new_tile.position = START_X+SQUARE_WIDTH*9, \
										START_Y+SQUARE_HEIGHT*7+PIECE_OFFSET_Y
				self.tiles[tile_index_y][tile_index_x] = self.held_piece
				self.held_piece.position = tile.center_x+PIECE_OFFSET_X, \
											tile.center_y+PIECE_OFFSET_Y
				self.turn = 'W' if self.turn == 'B' else 'B'
				reset_position = False

			elif new_tile is None:
				self.tiles[tile_index_y][tile_index_x] = self.held_piece
				self.held_piece.position = tile.center_x+PIECE_OFFSET_X, \
											tile.center_y+PIECE_OFFSET_Y
				self.turn = 'W' if self.turn == 'B' else 'B'
				reset_position = False

		if reset_position:
			self.held_piece.position = self.held_piece_origin

		self.held_piece = None


	def on_key_press(self, symbol: int, modifiers: int):
		""" User presses key """
		if symbol == arcade.key.R:
			# Restart
			self.setup()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()