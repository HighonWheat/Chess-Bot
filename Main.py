import pygame
import sys
from Board import draw_board, load_images
import chess
board = chess.Board()

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess AI")
load_images()

clock = pygame.time.Clock()

running = True
selected_square = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #check if the event is a quit event
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // 100
            row = y // 100
            rank = 7 - row
            square = chess.square(col, rank)
            piece = board.piece_at(square)

            if selected_square is None:
                # Click 1: Only select if there is a piece of the current turn's color
                if piece is not None and piece.color == board.turn:
                    selected_square = square
            else:
                # Click 2: Attempt the move
                move = chess.Move(selected_square, square)

                # What if it's a pawn promotion? (Rank 0 for black, Rank 7 for white)
                # python-chess expects promotion=chess.QUEEN for pawn moves reaching the end
                if chess.Move(selected_square, square, promotion=chess.QUEEN) in board.legal_moves:
                    move = chess.Move(selected_square, square, promotion=chess.QUEEN)

                if move in board.legal_moves:
                    board.push(move)
                    selected_square = None
                elif piece is not None and piece.color == board.turn:
                    # Player changed their mind and clicked another of their own pieces!
                    selected_square = square
                else:
                    # Clicked an invalid destination or empty space
                    selected_square = None

    draw_board(screen, board) #draw the chess board and pieces on the screen

    pygame.display.flip()

    clock.tick(60) #limit the frame rate to 60 frames per second




pygame.quit()
sys.exit()