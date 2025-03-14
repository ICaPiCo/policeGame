import pygame
from math import*
from random import*
import time
import os

# Initialize pygame
pygame.init()

global PosX, PosY
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
global mousePosX,mousePosY
mousePosX,mousePosY = 0,0
stored_x,stored_y = 200,200
trigger = False
trig_done = False
running = False
Menu = True
Yapping = False
Drawing = False
Generation = False
ScoreMenu = False

def text_speech(posX,posY,text,speed,color,bgColor):
    textList=list(text)
    for i in range(len(textList)):
        randomTime=(uniform(speed-0.1,speed+0.1))/60
        time.sleep(randomTime)
        newText = font.render(text[:i+1], True, color, bgColor)
        screen.blit(newText, (posX, posY))
        pygame.display.update()


def clicking_on(object):
    if pygame.mouse.get_pressed()[0]:
        if collision(object, pygame.mouse.get_pos()):
            return True
        else:
            return False

def drawBackground():
    width, height = background.get_size()
    mX, mY = pygame.mouse.get_pos()
    backX = 0#-(((mX / SCREEN_WIDTH) - 0.5) * 0.1 *width)  #0.1 can change
    backY = 0#-(((mY / SCREEN_HEIGHT) - 0.5) * 0.1 * height)
    screen.blit(background, (backX-100, backY))
    text_back = font.render(f"BackPos: {backX:.2f}, {backY:.2f}", True, (255, 255, 255))
    screen.blit(text_back, (10, 50))

def drawNapoleon(postionX,postionY):
    global PosX, PosY
    screen.blit(napoleon,(PosX+postionX,PosY+postionY))

def drawForeground():
    width,height=background.get_size()
    mX, mY = pygame.mouse.get_pos()
    #0.1 can change
    TableX = 0#-(((mX / SCREEN_WIDTH) - 0.5) * 0.05 *width)  #0.05 can change
    TableY = 0#-(((mY / SCREEN_HEIGHT) - 0.5) * 0.11 *height)  #0.1 can change
    table_text = font.render(f"TablePos: {TableX:.2f}, {TableY:.2f}", True, (255, 255, 255))
    
    screen.blit(table,(TableX,TableY+570))
    screen.blit(table_text, (10, 80))

def drawButtons():
    pygame.draw.rect(screen, BLACK, button_color_black)
    pygame.draw.rect(screen, WHITE, button_color_white)
    pygame.draw.rect(screen, BLACK, button_size_up)
    pygame.draw.rect(screen, BLACK, button_size_down)
    screen.blit(font.render("+", True, WHITE), (670, 230))
    screen.blit(font.render("-", True, WHITE), (670, 290))


def drawOrder():
    global mousePosX,mousePosY
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
    global frame,mousePosX,mousePosY,trigger,trig_done
    width, height = background.get_size()
    nap_rect = napoleon.get_rect(topleft=((frame-1)*-10,sin(frame-1)*10))
    if frame<60:# and #not nap_rect.collidepoint(mousePosX,mousePosY):
        frame+=1
    else:
        trigger = True
    if trigger == True and not trig_done:  
        text_speech(0,0,"Hello world",1,(255,255,255),(0,0,0))
        trig_done = True
    frameX = -10*frame-(mousePosX/SCREEN_WIDTH)*0.08
    frameY = (sin(frame)*10)-(mousePosY/SCREEN_HEIGHT)*0.10
    
    return frameX, frameY
    
  
    
'''
def animation(image,startX,startY,SpeedX,SpeedY,endX,endY):
    image_rect = image.get_rect(topleft=(PosX, PosY))
    currentPosX, currentPosY = image_rect.centerx, image_rect.centery
    while currentPosX < endX and currentPosY < endY:
        if currentPosX < endX:
            currentPosX += SpeedX
        if currentPosY < endY:
            currentPosY += SpeedY

        drawBackground()
        drawImage(currentPosX, currentPosY)
        drawForeground()
        drawButtons()
'''
#animation(image, -500, 200, 20, 20, SCREEN_WIDTH/2, 200)

def drawMenu():
    screen.fill((0, 0, 0))

font = pygame.font.Font(None,37)
running = False
drawing = False
Menu = True 
x1,y1,z1 = 100,100,100
o=0

def buttonCliqued():
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

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

#MAIN Loop for menu / game
while running or Menu:

    #SECOND Loop for running
    while running:

    #main stuff going on here
        drawBackground()
        drawOrder()
        canvasStuff()
        wantToQuit()
        buttonCliqued()
        pygame.display.flip()

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
                    Menu = False if Menu else True
                    running = True
        
        x1 = int((sin(o) + 1) * 100)  # Red
        y1 = int((sin(o + -cos(0)) + 1) * 80)  # Green (offset by -cos)
        z1 = int((sin(o + cos(0)) + 1) * 125)  # Blue (offset by cos)
        
        xtext = font.render(f"{x1} / {y1} / {z1}", True,(255,255,255))
        screen.blit(xtext, (10,100))
        pygame.display.flip()
    
    while Yapping:
        pass
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
