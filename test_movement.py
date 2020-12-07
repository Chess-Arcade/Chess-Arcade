from pieces import King
from board import Board 
from pieces import Pawn, Rook

def test_king_no_valid_start_moves():
    board = Board()
    board.reset_pieces()
    king = board.board[0][4]
    king.valid_moves(board)
    actual = king.move_list
    expected = []
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
    board.board[4][4] = rook
    rook.valid_moves(board)
    actual = rook.move_list
    expected = []
    assert actual == expected
