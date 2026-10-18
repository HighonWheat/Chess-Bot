import chess
import chess.pgn
from pathlib import Path
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

        