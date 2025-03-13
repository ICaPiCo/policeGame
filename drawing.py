import pygame

# Initialize pygame
pygame.init()

# Screen settings
overSize = 4
pygame.display.set_caption("PortraitRobot")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize,SCREEN_HEIGHT/overSize

#IMAGES
image = pygame.image.load("napoleon.png")
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT))
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

def collision(a,b):
    return pygame.collidepoint(a,b)
def i():
    pass







def drawBackground():
    width,height=background.get_size()
    screen.blit(background,(0,0))


def drawImage(postionX,postionY):
    screen.blit(image,(postionX,postionY))

def drawForeground():
    width,height=background.get_size()
    screen.blit(background,(0,0))
    screen.blit(table,(0,(60*height/100)))

def drawButtons():
    pygame.draw.rect(screen, BLACK, button_color_black)
    pygame.draw.rect(screen, WHITE, button_color_white)
    pygame.draw.rect(screen, BLACK, button_size_up)
    pygame.draw.rect(screen, BLACK, button_size_down)
    screen.blit(font.render("+", True, WHITE), (670, 230))
    screen.blit(font.render("-", True, WHITE), (670, 290))

running = True
drawing = False

def drawOrder():
    mousePosX, mousePosY = pygame.mouse.get_pos()
    drawBackground()
    drawButtons()
    drawImage(mousePosX,mousePosY)
    drawForeground()

while running:

    drawOrder()

    borderPatrol = ((10*SCREEN_HEIGHT)/100)
    screenX, screenY = ((3*SCREEN_WIDTH)/overSize)-borderPatrol, ((3*SCREEN_HEIGHT)/overSize)-borderPatrol
    screen.blit(canvas, (screenX,screenY))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
    pygame.display.flip()

pygame.quit()

#S Stage: create interaction objects
#S Stage: create drawing complete
#S Stage: create story & progression - objects in background
#S Stage: create minigames
#S Stage: create looking around