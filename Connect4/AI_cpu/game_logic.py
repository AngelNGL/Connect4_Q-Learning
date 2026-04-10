from copy import deepcopy

ROWS = 6
COLS = 7
EMPTY = 0
CPU_PIECE = 1
PLAYER_PIECE = 2


def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def copy_board(board):
    return deepcopy(board)

def print_board(board):
    print()
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print("0 1 2 3 4 5 6")

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == EMPTY

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def get_next_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None

def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    if row is None:
        return False
    board[row][col] = piece
    return True

def check_winner(board, piece):
    for row in range(ROWS):
        for col in range(COLS-3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    for row in range(ROWS-3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    for row in range(ROWS-3):
        for col in range(COLS-3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS-3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    return len(get_valid_moves(board)) == 0 and not check_winner(board, CPU_PIECE) and not check_winner(board, PLAYER_PIECE)

def convert_board(board):
    return "\n".join("".join(str(cell) for cell in row) for row in board)

def opponent_of(piece):
    return CPU_PIECE if piece == PLAYER_PIECE else PLAYER_PIECE

def get_winning_moves(board, piece):
    winning_moves = []
    for col in get_valid_moves(board):
        temp_board = copy_board(board)
        drop_piece(temp_board, col, piece)
        if check_winner(temp_board, piece):
            winning_moves.append(col)
    return winning_moves
