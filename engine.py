import chess

PIECES_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

def evaluate_board(board):
    """
    Evaluate the board position and return a score.
    Positive score favors white, negative score favors black.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return  -99999
        else:
            return 99999   # White wins
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Draw
    score = 0


    #  Loop through all pieces on the board using board.piece_map()
    for square, piece in board.piece_map().items():
        value = PIECES_VALUES[piece.piece_type]
        if piece.color == chess.WHITE:
            score += value
        else:
            score -= value
    return score
