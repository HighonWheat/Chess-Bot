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


def draw_board(screen, board):
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
        color = "w" if piece.color else "b"
        image = PIECES[f"{color}{piece.symbol().upper()}"]
        screen.blit(image, (col * square_size, row * square_size))
