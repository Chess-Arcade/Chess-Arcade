from board import Board 
from pieces import Pawn, Rook, King, Queen, Knight, Bishop

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

def test_valid_white_center_pawn_moves():
    board = Board()
    board.reset_pieces()
    pawn = board.board[6][4]
    pawn.valid_moves(board)
    actual = pawn.move_list
    expected = [[4, 4], [5, 4]]
    assert actual == expected

def test_valid_black_center_pawn_moves():
    board = Board()
    board.reset_pieces()
    pawn = board.board[1][4]
    pawn.valid_moves(board)
    actual = pawn.move_list
    expected = [[3, 4], [2, 4]]
    assert actual == expected
    
def test_pawn_validate_attacking():
    board = Board()
    board.reset_pieces()
    board.board[2][3] = Pawn(2,3,'w')
    pawn = board.board[1][4]
    pawn.valid_moves(board)
    actual = pawn.move_list
    expected = [[3, 4], [2, 4], [2,3]]
    assert actual == expected

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
    expected = [[3, 4], [2, 4], [1, 4], [0, 4], [5, 4], [4, 3], [4, 2], [4, 1], [4, 0], [4, 5], [4, 6], [4, 7]]
    assert actual == expected

def test_knight_valid_moves():
    board = Board()
    knight = Knight(4,4,'w')
    knight.valid_moves(board)
    actual = knight.move_list
    expected = [[2, 3], [2, 5], [3, 2], [3, 6], [5, 2], [5, 6]]
    assert actual == expected

def test_knight_valid_start_moves():
    board = Board()
    knight = Knight(7,3,'w')
    knight.valid_moves(board)
    actual = knight.move_list
    expected = [[5, 2], [5, 4]]
    assert actual == expected