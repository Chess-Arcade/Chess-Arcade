from board import Board 
from pieces import Pawn, Rook, King, Queen, Knight, Bishop

# KING Tests
def test_king_no_valid_start_moves():
    board = Board()
    board.reset_pieces()
    king = board.board[0][4]
    king.valid_moves(board)
    actual = king.move_list
    expected = []
    assert actual == expected

def test_king_valid_start_moves():
    board = Board()
    king = King(4,4,'w')
    king.valid_moves(board)
    actual = king.move_list
    expected = [[3, 4], [5, 4], [4, 3], [4, 5], [5, 3], [5, 5], [3, 3], [3, 5]]
    assert actual == expected

def test_black_king_castling():
    board = Board()
    king = King(0,4,'b')
    board.board[0][4] = king
    board.board[0][7] = Rook(0,7,'b')
    board.board[0][0] = Rook(0,0,'b')
    king.valid_moves(board)
    actual = king.move_list
    expected = [[1, 4], [0, 3], [0, 5], [1, 3], [1, 5], [0, 6], [0, 2]]
    assert actual == expected

def test_white_king_castling():
    board = Board()
    king = King(7,4,'b')
    board.board[7][4] = king
    board.board[7][7] = Rook(7,7,'w')
    board.board[7][0] = Rook(7,0,'w')
    king.valid_moves(board)
    actual = king.move_list
    expected = [[6, 4], [7, 3], [7, 5], [6, 3], [6, 5], [7, 6], [7, 2]]
    assert actual == expected

def test_black_king_cannot_castling():
    board = Board()
    king = King(0,4,'b')
    board.board[0][4] = king
    board.board[0][7] = Rook(0,7,'b')
    board.board[0][6] = Knight(0,5,'b')
    board.board[0][0] = Rook(0,0,'b')
    king.valid_moves(board)
    actual = king.move_list
    expected = [[1, 4], [0, 3], [0, 5], [1, 3], [1, 5], [0, 2]]
    assert actual == expected

def test_white_king_cannot_castling():
    board = Board()
    king = King(7,4,'w')
    board.board[7][4] = king
    board.board[7][7] = Rook(7,7,'w')
    board.board[7][6] = Knight(7,6,'w')
    board.board[7][3] = Bishop(7,3,'w')
    board.board[7][0] = Rook(7,0,'w')
    king.valid_moves(board)
    actual = king.move_list
    expected = [[6, 4], [7, 5], [6, 3], [6, 5]]
    assert actual == expected
    
# Pawn Tests:
def test_valid_white_center_pawn_moves():
    board = Board()
    board.reset_pieces()
    pawn = board.board[6][4]
    pawn.valid_moves(board)
    actual = pawn.move_list
    expected = [[5, 4], [4, 4]]
    assert actual == expected

def test_valid_black_center_pawn_moves():
    board = Board()
    board.reset_pieces()
    pawn = board.board[1][4]
    pawn.valid_moves(board)
    actual = pawn.move_list
    expected = [[2, 4], [3, 4]]
    assert actual == expected
    
def test_pawn_validate_attacking():
    board = Board()
    board.reset_pieces()
    board.board[2][3] = Pawn(2,3,'w')
    pawn = board.board[1][4]
    pawn.valid_moves(board)
    actual = pawn.attack_list
    expected =  [[2, 3]]               
    assert actual == expected

def test_pawn_no_valid_moves():
    board = Board()
    board.board[1][0] = Pawn(1,0, 'b')
    white_pawn = Pawn(2,0,'w')
    white_pawn.valid_moves(board)
    actual = white_pawn.move_list
    expected = []
    assert actual == expected


# Rook Tests:
def test_rook_no_valid_start_moves():
    board = Board()
    board.reset_pieces()
    rook = board.board[0][0]
    rook.valid_moves(board)
    actual = rook.move_list
    expected = []
    assert actual == expected

def test_rook_valid_moves():
    board = Board()
    rook= Rook(4,4,'w')
    rook.valid_moves(board)
    actual = rook.move_list
    expected = [[3, 4], [2, 4], [1, 4], [0, 4], [5, 4], [6, 4], [7, 4], [4, 3], [4, 2], [4, 1], [4, 0], [4, 5], [4, 6], [4, 7]]
    assert actual == expected

def test_rook_attack_list():
    board = Board()
    rook = Rook(4,4,'w')
    board.board[4][1] = Pawn(4,1,'b')
    board.board[4][2] = Pawn(4,2,'b')
    board.board[7][4] = Pawn(7,4,'b')
    board.board[0][4] = Pawn(0,4,'b')
    board.board[6][6] = Pawn(6,6,'b')
    rook.valid_moves(board)
    actual = rook.attack_list
    expected = [[0, 4], [7, 4], [4, 2]]
    assert actual == expected

# Knight Tests:
def test_knight_valid_moves():
    board = Board()
    knight = Knight(4,4,'w')
    knight.valid_moves(board)
    actual = knight.move_list
    expected = [[2, 3], [2, 5], [3, 2], [3, 6], [6, 3], [6, 5], [5, 2], [5, 6]]
    assert actual == expected

def test_knight_valid_start_moves():
    board = Board()
    board.reset_pieces()
    knight = Knight(7,3,'w')
    knight.valid_moves(board)
    actual = knight.move_list
    expected = [[5, 2], [5, 4]]

def test_knight_valid_attack():
    board = Board()
    knight = Knight(4,4,'w')
    board.board[6][5] = Pawn(6, 5,'b')
    board.board[6][3] = Pawn(6, 3,'b')
    board.board[5][6] = Pawn(5, 6,'b')
    knight.valid_moves(board)
    actual = knight.attack_list
    expected = [[6, 3], [6, 5], [5, 6]]
    assert actual == expected

# Bishop Tests:
def test_bishop_valid_moves():
    board = Board()
    bishop = Bishop(1,3,'b')
    bishop.valid_moves(board)
    actual = bishop.move_list
    expected = [[0, 2], [0, 4], [2, 4], [3, 5], [4, 6], [5, 7], [2, 2], [3, 1], [4, 0]]
    assert actual == expected

def test_bishop_valid_moves_two():
    board = Board()
    bishop = Bishop(4,4,'b')
    bishop.valid_moves(board)
    actual = bishop.move_list
    expected = [[3, 3], [2, 2],[1,1], [0, 0], [3, 5], [2, 6], [1, 7], [5, 5], [6, 6], [7, 7], [5, 3], [6, 2], [7, 1]]
    assert actual == expected

def test_bishop_attacking():
    board = Board()
    bishop = Bishop(4,3,'w')
    board.board[4][3] = bishop
    board.board[5][4] = Pawn(5,4,'b')
    bishop.valid_moves(board)
    actual = bishop.attack_list
    expected = [[5,4]]
    assert actual == expected

def test_bishop_no_moves_after_attacking():
    board = Board()
    bishop = Bishop(4,3,'w')
    board.board[4][3] = bishop
    board.board[5][4] = Pawn(5,4,'b')
    bishop.valid_moves(board)
    actual = bishop.move_list
    expected = [[3, 2], [2, 1], [1, 0], [3, 4], [2, 5], [1, 6], [0, 7], [5, 2], [6, 1], [7, 0]]
    assert actual == expected