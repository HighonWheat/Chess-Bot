import pygame
from pathlib import Path

square_size = 100

color_light = (240, 217, 181)
color_dark = (181, 136, 99)
PIECES = {}


def load_images():
    assets_dir = Path(__file__).parent / "assets"
    pieces = ["P", "R", "N", "B", "Q", "K"]

    for color in ("w", "b"):
        for piece in pieces:
            image_path = assets_dir / f"{color}{piece}.webp"
            image = pygame.image.load(str(image_path)).convert_alpha()
            PIECES[f"{color}{piece}"] = pygame.transform.smoothscale(
                image, (square_size, square_size)
            )


def draw_board(screen, board, selected_square=None):
    for row in range(8):
        for col in range(8):
            color = color_light if (row + col) % 2 == 0 else color_dark
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    col * square_size,
                    row * square_size,
                    square_size,
                    square_size,
                ),
            )

    for square, piece in board.piece_map().items():
        col = square % 8
        row = 7 - square // 8
        piece_color = "w" if piece.color else "b"
        image = PIECES[f"{piece_color}{piece.symbol().upper()}"]
        screen.blit(image, (col * square_size, row * square_size))

    if selected_square is not None:
        move_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        for move in board.legal_moves:
            if move.from_square == selected_square:
                dest_col = move.to_square % 8
                dest_row = 7 - move.to_square // 8
                center = (
                    dest_col * square_size + square_size // 2,
                    dest_row * square_size + square_size // 2,
                )
                pygame.draw.circle(move_overlay, (40, 40, 40, 128), center, 12)
        screen.blit(move_overlay, (0, 0))
