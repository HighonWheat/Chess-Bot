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

def minimax(board, depth, alpha, beta, maximizing_player):
    """
        Recursively searches the game tree to find the best score.
        - depth: how many half-moves (plies) left to search
        - alpha: best score White is guaranteed so far
        - beta: best score Black is guaranteed so far
        - maximizing_player: True if it's White's turn, False if Black's
        """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False) # Recursively call minimax for the next player
            board.pop()

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break  # Beta cut-off
        return max_eval

    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True) # Recursively call minimax for the next player
            board.pop()

            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)

            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval