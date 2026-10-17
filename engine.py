import chess
import json
from pathlib import Path

WEIGHTS_FILE = Path(__file__).parent / "weights.json"

PIECES_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

def load_weights():
    """Loads positional weights from a weight.json or create a new table of 0s."""
    if WEIGHTS_FILE.exists():
        with open(WEIGHTS_FILE, "r") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    else:
        weights = {piece_type: [0.0] * 64 for piece_type in range(1, 7)}
        save_weights(weights)
        return weights

def save_weights(weights):
    """Saves the learned positional weights to weights.json."""
    with open(WEIGHTS_FILE, "w") as f:
        json.dump(weights, f, indent=2)

POSITION_WEIGHTS = load_weights()

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
        base_value = PIECES_VALUES[piece.piece_type]
        piece_table = POSITION_WEIGHTS[piece.piece_type]
        if piece.color == chess.WHITE:
            bonus = piece_table[square]
            score += base_value + bonus
        else:
            mirrored_square = chess.square_mirror(square)
            bonus = piece_table[mirrored_square]
            score -= base_value + bonus

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

def get_best_move(board, depth):
    best_move = None
    
    # Check if the AI is currently playing as White or Black
    if board.turn == chess.WHITE:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            # After White moves, it is Black's turn (False)
            score = minimax(board, depth - 1, -float('inf'), float('inf'), False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            # After Black moves, it is White's turn (True)
            score = minimax(board, depth - 1, -float('inf'), float('inf'), True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
                
    return best_move