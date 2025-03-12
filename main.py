#pyGame drawing game
import pygame
import sys
import random
from pygame.locals import *

pygame.init()
white = (255, 255, 255)
#screen
running = True
screen = pygame.display.set_mode((500,500)) #, pygame.FULLSCREEN 
pygame.display.set_caption("Portrait robot")
def check_collision(rectangle):
    return pygame.Rect.collidepoint(rectangle, (MouseX, MouseY))
#game loop
while running:
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 20)
    MouseX,MouseY = pygame.mouse.get_pos()
    rectangle = pygame.Rect(MouseX-50,MouseY-50, 100, 100)

    text = font.render(f"{MouseX},{MouseY}",False, (255,255,255))
    screen.blit(text, (0, 0))
    pygame.draw.rect(screen, white, rectangle)
    if check_collision(rectangle):
        pygame.draw.rect(screen, (255, 0, 0), rectangle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  
            if check_collision(rectangle):
                if white != (255, 255, 255):
                    white = (255,255,255)
                else:
                    white = (0,0,0)
    

    pygame.display.flip()
    #PosX,PosY = pygame.mouse.get_pos()
    #screen.blit((PosX,PosY),(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        