import pygame
from math import*
from random import*
import time
import os
from random import randint

os.system("cls")

pygame.init()
drawing = False
score=0
combo=0
penning = False

pen = 1
font = pygame.font.Font(None, 36)
# Screen settings
overSize = 4
pygame.display.set_caption("Drawn To Justice")
screen = pygame.display.set_mode((1920,1200), pygame.FULLSCREEN)
COLOR = (255, 255, 255)
trail = []
previous_pos = pygame.mouse.get_pos()
saved_surface = screen.copy()
class Drawn:
    def __init__(self,name,PosX,PosY,color,layer,size,shape):
        self.PosX = PosX
        self.PosY = PosY
        self.layer = layer
        self.color = color
        self.size = size
        self.shape = shape
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.PosX, self.PosY),self.size)
    def move(self, x, y):
        self.PosX += x
        self.PosY += y
class Thing(Drawn):
    '''this is the same as the other one but a subclass'''
    def __init__(self, name, PosX, PosY, color, layer, size, shape):
        super().__init__(name, PosX, PosY, color, layer, size, shape) # super uselfull
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.PosX, self.PosY), self.size)
'''
while True:

    ball = Drawn("ball", 100, 100, (255, 255, 255), 1, 10, "circle") 
    ball.draw()
    rect  = Drawn("rect", 200, 200, (255, 255, 255), 1, 10, "rect")
    rect.draw() #hmm not sure how to do this 
    pygame.display.flip() 
'''
last_thickness = 3

while True:
    current_pos = pygame.mouse.get_pos()
    deltaX, deltaY = pygame.mouse.get_rel()
    distance = sqrt(deltaX**2 + deltaY**2)
    thickness = max(3, distance * 0.29)  
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                drawing = True 
            elif event.key == pygame.K_e:
                if COLOR == (255,255,255) :
                    COLOR = (0, 0, 0)
                else:
                    COLOR = (255, 255, 255)
            elif event.key == pygame.K_r:
                screen.fill((0,0,0))
        elif event.type == pygame.KEYUP:
            if event.key ==  pygame.K_SPACE:
                drawing = False
                last_thickness = 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                drawing = False  
        elif event.type == pygame.WINDOWMINIMIZED:  # Save the screen before minimizing 
            saved_surface = screen.copy()
        elif event.type == pygame.WINDOWFOCUSGAINED:  # Restore the screen when refocused
            screen.blit(saved_surface, (0, 0))
            pygame.display.update()
    if drawing:
        if distance > 0.1:
            r,t = current_pos
            pygame.draw.line(screen, COLOR, previous_pos, current_pos, int(last_thickness))  
            previous_pos = current_pos  
            last_thickness = last_thickness * 0.75 + thickness * 0.25
    else:
        
        previous_pos = pygame.mouse.get_pos() 
    text_surface = pygame.Surface((500, 100)) 
    text_surface.fill((0, 0, 0))
    thick_text = font.render(f"Thickness: {int(thickness)}",True,(255,255,255))
    text_surface.blit(thick_text, (10, 10))   
    screen.blit(text_surface, (0, 0))
    pygame.display.update()
    pygame.display.update(100,100,1300,800) 
   
   
   