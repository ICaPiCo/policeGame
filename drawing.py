import pygame
from math import*
# Initialize pygame
pygame.init()

global PosX, PosY
PosX, PosY = -700, 200

# Screen settings
overSize = 4
pygame.display.set_caption("PortraitRobot")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize,SCREEN_HEIGHT/overSize

#IMAGES
image = pygame.image.load("napoleon.png")
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH+200,SCREEN_HEIGHT+200))
table = pygame.image.load("table.png")
table = pygame.transform.scale(table, (SCREEN_WIDTH,SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Brush settings
brush_color = BLACK
brush_size = 5

# Create screen and canvas
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# UI buttons
button_color_black = pygame.Rect(650, 100, 100, 40)
button_color_white = pygame.Rect(650, 160, 100, 40)
button_size_up = pygame.Rect(650, 220, 100, 40)
button_size_down = pygame.Rect(650, 280, 100, 40)

# Font setup
font = pygame.font.Font(None, 30)
Menu = False 



def clicking_on(object):
    if pygame.mouse.get_pressed()[0]:
        if collision(object, pygame.mouse.get_pos()):
            return True
        else:
            return False





def drawBackground():
    width, height = background.get_size()
    mX, mY = pygame.mouse.get_pos()
    backX = -(((mX / SCREEN_WIDTH) - 0.5) * 0.1 *width)  #0.1 can change
    backY = -(((mY / SCREEN_HEIGHT) - 0.5) * 0.1 * height)
    screen.blit(background, (backX-100, backY))
    text_back = font.render(f"BackPos: {backX:.2f}, {backY:.2f}", True, (255, 255, 255))
    screen.blit(text_back, (10, 50))


def drawImage(postionX,postionY):
    screen.blit(image,(postionX,postionY))

def drawForeground():
    width,height=background.get_size()
    mX, mY = pygame.mouse.get_pos()
    #0.1 can change
    TableX = -(((mX / SCREEN_WIDTH) - 0.5) * 0.05 *width)  #0.05 can change
    TableY = -(((mY / SCREEN_HEIGHT) - 0.5) * 0.11 *height)  #0.1 can change
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
    mousePosX, mousePosY = pygame.mouse.get_pos()
    text_mouse = font.render(f"Mouse position: {mousePosX,mousePosY}", True, (255, 255, 255))
    drawForeground()
    drawButtons()
    drawImage(mousePosX,mousePosY)
    

    screen.blit(text_mouse, (10, 10))   

font = pygame.font.Font(None,37)
running = True
drawing = False


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
        


#animation(image, -500, 200, 20, 20, SCREEN_WIDTH/2, 200)
x1,y1,z1 = 100,100,100
o=0
def drawMenu():
    screen.fill((0, 0, 0))
    
    drawForeground()
    
while running or Menu:
    while running:

    #main stuff going on here
        screen.fill((0,0,0))
        drawBackground()
        drawOrder()
        animation(image, -500, 200, 20, 20, SCREEN_WIDTH/2, 200)
        borderPatrol = ((10*SCREEN_HEIGHT)/100)
        screenX, screenY = ((3*SCREEN_WIDTH)/overSize)-borderPatrol, ((3*SCREEN_HEIGHT)/overSize)-borderPatrol
        screen.blit(canvas, (screenX,screenY))
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
    #the following is Ioanis' draw code
    #maybe we can use the clicking function here but flemme
            elif event.type == pygame.MOUSEBUTTONDOWN:
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

        pygame.display.flip()

    while Menu:
        o+=0.1
        drawMenu()
        font = pygame.font.Font(None,37)
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
                    Menu = False
                    running = True
                    continue
        
        x1 = int((sin(o) + 1) * 100)  # Red
        y1 = int((sin(o + 2) + 1) * 80)  # Green (offset by 2)
        z1 = int((sin(o + 4) + 1) * 125)  # Blue (offset by 4)
        xtext = font.render(f"{x1} / {y1} / {z1}", True,(255,255,255))
        screen.blit(xtext, (10,100))
        pygame.display.flip()

pygame.quit()



#S Stage: create interaction objects
#S Stage: create drawing complete
#S Stage: create story & progression - objects in background
#S Stage: create minigames
#S Stage: create looking around (parralax) -...
# Features: parralax, image generation?, drawing engine, interactivity


