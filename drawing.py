import pygame
from math import*
from random import*
import time
import os
from random import randint
# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
global PosX, PosY, textI
PosX, PosY = 1000, 200

print(pygame.display.Info())


# Screen settings
overSize = 4
pygame.display.set_caption("PortraitRobot")
screen = pygame.display.set_mode((1920,1200), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize,SCREEN_HEIGHT/overSize

#IMAGES
napoleon = pygame.image.load("napoleon.png")
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH+200,SCREEN_HEIGHT+200))
table = pygame.image.load("table.png")
table = pygame.transform.scale(table, (SCREEN_WIDTH,SCREEN_HEIGHT))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Brush sett
brush_color = BLACK
brush_size = 5

# Create screen and canvas
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# UI buttons make em collidepointable
button_color_black = pygame.Rect(650, 100, 100, 40)
button_color_white = pygame.Rect(650, 160, 100, 40)
button_size_up = pygame.Rect(650, 220, 100, 40)
button_size_down = pygame.Rect(650, 280, 100, 40)

# Font setup
font = pygame.font.Font(None, 30)
frame= 0
global mousePosX,mousePosY,n
mousePosX,mousePosY = 0,0
n = 0
stored_x,stored_y = 200,200
trigger = False
trig_done = False
running = False
Menu = True
Yapping = False
Drawing = False
Generation = False
ScoreMenu = False
textI = 0
font = pygame.font.Font(None,37)
running = False
drawing = False
Menu = True 
x1,y1,z1 = 100,100,100
o=0

def create_text():
    info = {"nose":["green","red","blue"],"hair":["black","blond","brown"],"eyes":["blue","green","brown"],"skin":["white","black","brown"]}
    text = ""
    for i in info:
        text += f"{i}:{info[i][randint(0,2)]}\n"
        text +=" , "
    return text
def text_speech(posX, posY, text, speed, color, bgColor):
    global textI
    if 'textI' not in globals():
        textI = 0  
    if textI < len(text):
        if choice([1,0,0,0,0,0,0,0]):    
            newText = font.render(text[:textI+1], True, color, bgColor)
            screen.blit(newText, (posX, posY))
            textI += 1
        else: 
            newText = font.render(text[:textI], True, color, bgColor)
            screen.blit(newText, (posX, posY))
            textI += 1
    
    

def clicking_on(object):
    if pygame.mouse.get_pressed()[0]:
        if collision(object, pygame.mouse.get_pos()):
            return True
        else:
            return False

def drawBackground():
    width, height = background.get_size()
    mX, mY = pygame.mouse.get_pos()
    backX = 0-(((mX / SCREEN_WIDTH) - 0.5) * 0.1 *width)  #0.1 can change
    backY = 0-(((mY / SCREEN_HEIGHT) - 0.5) * 0.1 * height)
    screen.blit(background, (backX-100, backY))
    #text_back = font.render(f"BackPos: {backX:.2f}, {backY:.2f}", True, (255, 255, 255))
    #screen.blit(text_back, (10, 50))

def drawNapoleon(postionX,postionY):
    global PosX, PosY
    screen.blit(napoleon,(PosX+postionX,PosY+postionY))

def drawForeground():
    width,height=background.get_size()
    mX, mY = pygame.mouse.get_pos()
    #0.1 can change
    TableX = 0-(((mX / SCREEN_WIDTH) - 0.5) * 0.05 *width)  #0.05 can change
    TableY = 0-(((mY / SCREEN_HEIGHT) - 0.5) * 0.11 *height)  #0.1 can change
    table_text = font.render(f"TablePos: {TableX:.2f}, {TableY:.2f}", True, (255, 255, 255))
    
    screen.blit(table,(TableX,TableY+620))
    screen.blit(table_text, (10, 80))

def drawButtons():
    pygame.draw.rect(screen, BLACK, button_color_black)
    pygame.draw.rect(screen, WHITE, button_color_white)
    pygame.draw.rect(screen, BLACK, button_size_up)
    pygame.draw.rect(screen, BLACK, button_size_down)
    screen.blit(font.render("+", True, WHITE), (670, 230))
    screen.blit(font.render("-", True, WHITE), (670, 290))


def drawOrder():
    global mousePosX,mousePosY,n
    mousePosX, mousePosY = pygame.mouse.get_pos()
    text_mouse = font.render(f"Mouse position: {mousePosX,mousePosY}", True, (255, 255, 255))
    e,r = animateFrame()
    debug_text = font.render(f"Posish: {e:.2f}/{r:.2f}", True, (255, 255, 255))
    screen.blit(debug_text,(10,150))
    drawNapoleon(e,r)
    drawForeground()
    drawButtons()
    
    screen.blit(text_mouse, (10, 10))   

def animateFrame():
    global frame,mousePosX,mousePosY,trigger,trig_done,n,textI,created_text
    width, height = background.get_size()
    nap_rect = napoleon.get_rect(topleft=((frame-1)*-10,sin(frame-1)*10))
    if frame<60:# and #not nap_rect.collidepoint(mousePosX,mousePosY):
        frame+=1 
    else:
        trigger = True
   
    if frame >= 60:
        pass 
        
    if trigger == True:
        text_speech(300, 300, created_text, 1, (0, 0, 0), (255, 255, 255))
        
    frameX = -10*frame  
    frameY = sin(frame)*10
    frameX -= (mousePosX/SCREEN_WIDTH)*0.08*width
    frameY -= (mousePosY/SCREEN_HEIGHT)*0.10*height
    
    return frameX, frameY
  

def drawMenu():
    screen.fill((0, 0, 0))


'''
def buttonCliqued(brush_color, brush_size, drawing):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_color_black.collidepoint(x, y):
                brush_color = BLACK
            elif button_color_white.collidepoint(x, y):
                brush_color = WHITE
            elif button_size_up.collidepoint(x, y):
                brush_size = min(20, brush_size + 2)
            elif button_size_down.collidepoint(x, y):
                brush_size = max(2, brush_size - 2)
            elif screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos
                if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                    pygame.draw.circle(canvas, brush_color, (x - screenX, y - screenY), brush_size)

 '''   

def wantToQuit():
    global Menu,running,drawing
    #Get key presses here: feel free to add
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()   
                sys.exit()
                
            elif event.key == pygame.K_SPACE:
                Menu = False if Menu else True
                running = False

def canvasStuff():
    borderPatrol = ((10*SCREEN_HEIGHT)/100)
    screenX, screenY = ((3*SCREEN_WIDTH)/overSize)-borderPatrol, ((3*SCREEN_HEIGHT)/overSize)-borderPatrol
    screen.blit(canvas, (screenX,screenY))

#How to loop it?

#MAIN Loop for menu / game
while running or Menu:

    #SECOND Loop for running
    while running:

    #main stuff going on here
        drawBackground()
        drawOrder()
        canvasStuff()
        wantToQuit()
        #buttonCliqued(brush_color, brush_size, drawing)
        pygame.display.flip()#
        clock.tick(30)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_color_black.collidepoint(x, y):
                    brush_color = BLACK
                elif button_color_white.collidepoint(x, y):
                    brush_color = WHITE
                elif button_size_up.collidepoint(x, y):
                    brush_size = min(20, brush_size + 2)
                elif button_size_down.collidepoint(x, y):
                    brush_size = max(2, brush_size - 2)
                elif screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                elif event.type == pygame.MOUSEMOTION and drawing:
                    x, y = event.pos
                    if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                        pygame.draw.circle(canvas, brush_color, (x - screenX, y - screenY), brush_size)

    while Menu:
        o+=0.01
        
        drawMenu()
        font = pygame.font.Font(None,50)
        menu_text = font.render("Press space to start", True, (x1,y1,z1))
        screen.blit(menu_text, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2))
        #if menu_rect.collidepoint(pygame.mouse.get_pos()):
        #   x1, y1, z1 = 255, 255, 255
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()   
                    sys.exit()
                    
                elif event.key == pygame.K_SPACE:
                    frame = 0
                    Menu = False if Menu else True
                    running = True
                    trigger = False
                    textI = 0
                    global created_text 
                    created_text = create_text()
        x1 = int((sin(o) + 1) * 100)  # Red
        y1 = int((sin(o + -cos(0)) + 1) * 80)  # Green (offset by -cos)
        z1 = int((sin(o + cos(0)) + 1) * 125)  # Blue (offset by cos)
        
        xtext = font.render(f"{x1} / {y1} / {z1}", True,(255,255,255))
        screen.blit(xtext, (10,100))
        pygame.display.flip()
    while Yapping:
        
        pass
        #talking - we want to be able to look around while talking? - what is it really for?
        #insetr description
    while Drawing:
        pass
    while Generation:
        pass 
    while ScoreMenu:
        pass
pygame.quit()



#S Stage: create interaction objects
#S Stage: create drawing complete
#S Stage: create story & progression - objects in background
#S Stage: create minigames
#S Stage: create looking around (parralax) -...
# Features: parralax, image generation?, drawing engine, interactivity