import chess
import chess.pgn
import random
from pathlib import Path
from engine import get_best_move, evaluate_board
from engine import load_weights, save_weights

def train_from_pgn(pgn_path, max_games=500, learning_rate=0.05):
    """Reads games from a .pgn database and updates weights.json."""
    weights = load_weights()
    
    with open(pgn_path, "r", encoding="utf-8", errors="ignore") as pgn_file:
        for game_count in range(1, max_games + 1):
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # Reached end of PGN file!

            # 1. Check who won the game
            result = game.headers.get("Result", "*")
            if result == "1-0":
                outcome = 1.0   # White won
            elif result == "0-1":
                outcome = -1.0  # Black won
            else:
                continue  # Skip draws or unfinished games so the AI learns decisive play

            # 2. Replay the game move-by-move
            board = game.board()
            for move in game.mainline_moves():
                piece = board.piece_at(move.from_square)
                
                if piece is not None:
                    target_sq = move.to_square
                    
                    if piece.color == chess.WHITE:
                        weights[piece.piece_type][target_sq] += learning_rate * outcome
                    else:

                        mirrored_sq = chess.square_mirror(target_sq)
                        weights[piece.piece_type][mirrored_sq] -= learning_rate * outcome

                board.push(move)

            if game_count % 50 == 0:
                print(f"Processed {game_count} games...")

    # Clamp weights between -50 and +50 so no single square becomes worth more than a Pawn (100)!
    for pt in weights:
        weights[pt] = [round(max(-50.0, min(50.0, w)), 2) for w in weights[pt]]

    save_weights(weights)
    print("Training from PGN database complete! weights.json updated.")

if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"
    for pgn_name in ("Carlsen.pgn", "Nakamura.pgn"):
        train_from_pgn(data_dir / pgn_name, max_games=500, learning_rate=0.05)


def train_self_play(num_games=20, depth=2, learning_rate=0.05):
    """Have the AI play against itself and update weights.json."""
    weights = load_weights()

    for game_num in range(1, num_games + 1):
        board = chess.Board()
        history = []

        # --- WHILE LOOP: Plays 1 full game ---
        while not board.is_game_over() and len(history) < 100:
            if random.random() < 0.15:
                move = random.choice(list(board.legal_moves))
            else:
                move = get_best_move(board, depth=depth)

            # Lined up outside the if/else, inside the while loop:
            piece = board.piece_at(move.from_square)
            if piece is not None:
                history.append((piece.piece_type, piece.color, move.to_square))

            board.push(move)

        # --- OUTSIDE WHILE LOOP (Lined up with 'while'): Game just ended! ---
        final_score = evaluate_board(board)
        if final_score > 150:
            outcome = 1.0
        elif final_score < -150:
            outcome = -1.0
        else:
            outcome = 0.0

        if outcome != 0.0:
            for piece_type, color, square in history:
                if color == chess.WHITE:
                    weights[piece_type][square] += learning_rate * outcome
                else:
                    mirrored_square = chess.square_mirror(square)
                    weights[piece_type][mirrored_square] -= learning_rate * outcome

        print(f"Self-Play Game {game_num}/{num_games} finished | Moves: {len(history)} | Outcome: {outcome}")

    # --- OUTSIDE FOR LOOP (Lined up with 'for game_num'): All 20 games finished! ---
    for pt in weights:
        weights[pt] = [round(max(-50.0, min(50.0, w)), 2) for w in weights[pt]]

    save_weights(weights)
    print("Self-play training complete! weights.json updated.")

            


    

        