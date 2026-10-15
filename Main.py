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
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #check if the event is a quit event
            running = False

    draw_board(screen, board) #draw the chess board and pieces on the screen

    pygame.display.flip()

    clock.tick(60) #limit the frame rate to 60 frames per second

pygame.quit()
sys.exit()