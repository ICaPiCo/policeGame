import pygame
from math import*
from random import*
import time
import os
from random import randint

os.system("cls")

# Initialize pygame
pygame.init()
drawing = False
score=0
combo=0


# Screen settings
overSize = 4
pygame.display.set_caption("Drawn To Justice")
screen = pygame.display.set_mode((1920,1200), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize,SCREEN_HEIGHT/overSize
borderPatrol = ((10*SCREEN_HEIGHT)/100)
screenX, screenY = ((3*SCREEN_WIDTH)/overSize)-borderPatrol, ((3*SCREEN_HEIGHT)/overSize)-borderPatrol

def load_random_image(folder_path):
    """Load a random image from the specified folder"""
    if not os.path.exists(folder_path):
        print(f"Error: The directory '{folder_path}' does not exist!")
        return None
        
    image_files = [f for f in os.listdir(folder_path)]
    
    if not image_files:
        print(f"Error: No image files found in '{folder_path}'!")
        return None
        
    random_image = choice(image_files)
    try:
        return pygame.image.load(os.path.join(folder_path, random_image))
    except pygame.error as e:
        print(f"Error loading image {random_image}: {e}")
        return None

#IMAGES
logo = pygame.image.load("images/logo.png")
testimony = load_random_image("images/testimonials")
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT))
table = pygame.image.load("images/table.png")
table = pygame.transform.scale(table, (SCREEN_WIDTH,SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Brush settings
brush_color = BLACK
brush_size = 5

# UI buttons make em collidepointable
button_color_black = pygame.Rect(650, 100, 100, 40)
button_color_white = pygame.Rect(650, 160, 100, 40)
button_size_up = pygame.Rect(650, 220, 100, 40)
button_size_down = pygame.Rect(650, 280, 100, 40)

# Font setup
font = pygame.font.SysFont(None, int(SCREEN_HEIGHT/20))

def drawBackground():
    width,heigth=background.get_size()
    screen.blit(background,(0,0))

def drawImage(image,postionX,postionY):
    screen.blit(image,(postionX,postionY))

def drawButtons():
    pygame.draw.rect(screen, BLACK, button_color_black)
    pygame.draw.rect(screen, WHITE, button_color_white)
    pygame.draw.rect(screen, BLACK, button_size_up)
    pygame.draw.rect(screen, BLACK, button_size_down)
    screen.blit(font.render("+", True, WHITE), (670, 230))
    screen.blit(font.render("-", True, WHITE), (670, 290))
 

running = True
menu = True
drawing = True
x1,y1,z1 = 100,100,100
color=0
clock = pygame.time.Clock()


while running:
    while menu:
        color+=0.01
        screen.fill((0, 0, 0))
        menu_text = font.render("Press space to start", True, (x1,y1,z1))
        screen.blit(menu_text, (SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/2)+200))
        for event in pygame.event.get():   
            if event.type == pygame.KEYDOWN:  # First check if it's a keyboard event
                if event.key == pygame.K_SPACE:
                    menu = False
            if event.type == pygame.QUIT:  # Good practice to add quit condition
                running = False
                menu = False
                
        x1 = int((sin(color) * 127.5) + 127.5)  # Red (0–255)
        y1 = int((sin(color + 2) * 127.5) + 127.5)  # Green (0–255)
        z1 = int((sin(color + 4) * 127.5) + 127.5)  # Blue (0–255)
        
        xtext = font.render(f"{x1} / {y1} / {z1}", True,(255,255,255))
        screen.blit(xtext, (10,100))
        screen.blit(logo, (SCREEN_WIDTH/4, SCREEN_HEIGHT/20))
        pygame.display.flip()

    testimonyPoxX,testimonyPoxY = SCREEN_WIDTH,0
    for i in range(int(SCREEN_WIDTH*2/3/5)):
        testimonyPoxX-=5
        drawBackground()
        drawImage(testimony, testimonyPoxX, testimonyPoxY)
        drawImage(table, 0, SCREEN_HEIGHT/2)
        clock.tick(60)
        pygame.display.flip()

    text = "Hello this is a test"
    newtext = ""
    x,y = SCREEN_WIDTH/4,SCREEN_HEIGHT/3
    for i in text:
        newtext += i
        drawText = font.render(newtext, True, (255,255,255), (0,0,0))
        screen.blit(drawText, (x,y))
        time.sleep(randint(1,10)/200)
        pygame.display.flip()

    # Create canvas once before entering the drawing loop
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    # Draw initial canvas and UI
    screen.blit(canvas, (screenX, screenY))
    drawButtons()
    pygame.display.flip()

    # Drawing loop
    while drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drawing = False  # Exit the drawing loop
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
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                x, y = event.pos
                if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                    pygame.draw.circle(canvas, brush_color, (x - screenX, y - screenY), brush_size)
        
        # Redraw the background, canvas, and buttons every frame
        drawBackground()
        drawImage(table, 0, SCREEN_HEIGHT/2)
        screen.blit(canvas, (screenX, screenY))
        drawButtons()
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    #while genration:
    #while selecting:
    #while bossSpeech:
    #while playAgain:

pygame.quit()