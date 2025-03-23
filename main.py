import pygame
from math import *
from random import *
import time
import os
from random import randint
import sys

os.system("cls")  # Clear console screen

# Initialize pygame
pygame.init()
drawing = False
score = 0
combo = 0

# Screen settings
overSize = 4  # Scaling factor for canvas relative to screen size
pygame.display.set_caption("Drawn To Justice")
screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize, SCREEN_HEIGHT/overSize
borderPatrol = ((10*SCREEN_HEIGHT)/100)  # Border padding
screenX, screenY = ((3*SCREEN_WIDTH)/overSize)-borderPatrol, ((3*SCREEN_HEIGHT)/overSize)-borderPatrol  # Canvas position


def load_random_image(folder_path):
    """
    Load a random image from the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing images
        
    Returns:
        Surface: Randomly selected image as pygame Surface, or None if failed
    """
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


# Load game images
logo = pygame.image.load("images/logo.png")
testimony = load_random_image("images/testimonials")  # Random testimony image
boss = load_random_image("images/boss")  # Random boss image
criminal = load_random_image("images/criminals")  # Random criminal image

# Load and scale background image
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and scale mugshot image
mugshot = pygame.image.load("images/mugshot.jpg")
mugshot = pygame.transform.scale(mugshot, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and scale table image
table = pygame.image.load("images/table.png")
table = pygame.transform.scale(table, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (20, 255, 20)

# Brush settings
brush_color = BLACK
brush_size = 5

# Define UI button rectangles for collision detection
Space = 20  # Spacing between buttons
button_color_black = pygame.Rect(screenX+Space, screenY+10, 100, 40)  # Black color button
button_color_white_outline = pygame.Rect(screenX+100+Space, screenY+10, 100, 40)  # White color button outline
button_color_white = pygame.Rect(screenX+100+Space+5, screenY+10+5, 90, 30)  # White color button inner part
button_size_up = pygame.Rect(screenX+200+Space, screenY+10, 100, 40)  # Increase brush size button
button_size_down = pygame.Rect(screenX+300+Space, screenY+10, 100, 40)  # Decrease brush size button
button_done = pygame.Rect(screenX+400+Space, screenY+350, 100, 40)  # Done/Continue button

# Set up font
font = pygame.font.SysFont(None, int(SCREEN_HEIGHT/20))


def drawBackground():
    """Draw the background image to the screen."""
    width, height = background.get_size()
    screen.blit(background, (0, 0))


def drawImage(image, positionX, positionY):
    """
    Draw an image at the specified position.
    
    Args:
        image (Surface): The pygame image to draw
        positionX (int): X-coordinate for image placement
        positionY (int): Y-coordinate for image placement
    """
    screen.blit(image, (positionX, positionY))


def drawButtons():
    """Draw all the drawing tool buttons (colors and brush sizes)."""
    pygame.draw.rect(screen, BLACK, button_color_black)
    pygame.draw.rect(screen, BLACK, button_color_white_outline)
    pygame.draw.rect(screen, WHITE, button_color_white)
    pygame.draw.rect(screen, BLACK, button_size_up)
    pygame.draw.rect(screen, BLACK, button_size_down)
    screen.blit(font.render("+", True, WHITE), (screenX+200+(Space*3), screenY+10))
    screen.blit(font.render("-", True, WHITE), (screenX+300+(Space*3), screenY+10))


def drawDone():
    """Draw the green 'Done' button."""
    pygame.draw.rect(screen, GREEN, button_done)
 

def doCriminal():
    """Draw the criminal image in the comparison screen."""
    screen.blit(criminal, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2.5))


# Game state variables
running = True  # Main game loop flag
menu = True  # Start menu state
drawing = True  # Drawing mode state
isCriminal = True  # Criminal comparison state
bossSpeech = True  # Boss feedback state
playAgain = True  # Play again prompt state
drawings = []  # List to store paths to saved drawings
x1, y1, z1 = 100, 100, 100  # RGB values for color cycling text
color = 0  # Color cycling animation parameter
clock = pygame.time.Clock()  # Game clock for frame rate control

class person:
    
    def __init__(self,mood,hair):
        self.mood = mood
        self.hair = hair
    def build(self,posX,posY):
        base = pygame.image.load("images/creation/basic guy.png")
        image = pygame.image.load(f"images/creation/face_{self.mood}.png")
        hair = pygame.image.load(f"images/creation/hair_{self.hair}.png")
        base = pygame.transform.scale(base, (SCREEN_WIDTH/3, SCREEN_HEIGHT))
        image = pygame.transform.scale(image, (SCREEN_WIDTH/3, SCREEN_HEIGHT))
        hair = pygame.transform.scale(hair, (SCREEN_WIDTH/3, SCREEN_HEIGHT))
        surface = pygame.Surface((SCREEN_WIDTH/3, SCREEN_HEIGHT))
        surface.fill((255,255,255))
        surface.blit(base, (0, 0))
        surface.blit(image, (0, 0))
        
        surface.blit(hair, (0, 0))
        screen.blit(surface, (posX, posY))
    def genid(self):
        id = {"face":self.mood,"hair":self.hair}
        


    
# Main game loop
while running:
    
    culprit = person(choice(["angry","happy"]), choice(["fluffy","spicky","pea"]))
    culprit1 = person(choice(["angry","happy"]), choice(["fluffy","spicky","pea"]))
    culprit2 = person(choice(["angry","happy"]), choice(["fluffy","spicky","pea"]))
    
    # Start menu loop
    while menu:
        color += 0.01  # Increment color animation parameter
        screen.fill((0, 0, 0))  # Clear screen
        
        # Create color-cycling "Press space to start" text
        menu_text = font.render("Press space to start", True, (x1, y1, z1))
        screen.blit(menu_text, (SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/2)+200))
        
        # Event handling
        for event in pygame.event.get():   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False  # Exit menu when space is pressed
                if event.key == pygame.K_p:
                    running = False
                    menu = False
                    pygame.quit()
                    sys.exit()  
            if event.type == pygame.QUIT:
                running = False
                menu = False
        
        # Calculate color-cycling RGB values with sine waves
        x1 = int((sin(color) * 127.5) + 127.5)         # Red (0–255)
        y1 = int((sin(color + 2) * 127.5) + 127.5)     # Green (0–255)
        z1 = int((sin(color + 4) * 127.5) + 127.5)     # Blue (0–255)
        
        # Display game logo
        screen.blit(logo, (SCREEN_WIDTH/4, SCREEN_HEIGHT/20))
        pygame.display.flip()  # Update display

    # Testimony scene animation - slide in from right
    testimonyPosX, testimonyPosY = SCREEN_WIDTH, 0
    for i in range(int(SCREEN_WIDTH*2/3/20)):
        testimonyPosX -=20  # Move testimony image left
        drawBackground()
        drawImage(testimony, testimonyPosX, testimonyPosY)
        drawImage(table, 0, SCREEN_HEIGHT/2)
        clock.tick(60)  # Limit to 60 FPS
        pygame.display.flip()

    # Display testimony text letter by letter
    
    text = "Hello this is a test"
    newtext = ""
    textX, textY = SCREEN_WIDTH/4, SCREEN_HEIGHT/3
    for i in text:
        newtext += i
        drawText = font.render(newtext, True, (255, 255, 255), (0, 0, 0))
        screen.blit(drawText, (textX, textY))
        time.sleep(randint(1, 10)/200)  # Random delay for typewriter effect
        pygame.display.flip()

    # Create canvas for drawing
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    # Draw initial canvas and UI
    screen.blit(canvas, (screenX, screenY))
    drawDone()
    drawButtons()
    pygame.display.flip()

    # Drawing interface loop
    while drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drawing = False  # Exit the drawing loop
                if event.key == pygame.K_p:
                    running = False
                    menu = False
                    pygame.quit()
                    sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Handle button clicks
                if button_done.collidepoint(x, y):
                    drawing = False
                elif button_color_black.collidepoint(x, y):
                    brush_color = BLACK
                    
                elif button_color_white.collidepoint(x, y):
                    brush_color = WHITE
                elif button_size_up.collidepoint(x, y):
                    brush_size = min(20, brush_size + 2)  # Increase brush size with upper limit
                elif button_size_down.collidepoint(x, y):
                    brush_size = max(2, brush_size - 2)  # Decrease brush size with lower limit
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                # Draw on canvas when mouse is moved with button pressed
                x, y = event.pos
                if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT:
                    pygame.draw.circle(canvas, brush_color, (x - screenX, y - screenY), brush_size)
        
        # Redraw the scene each frame
        drawBackground()
        drawImage(testimony, testimonyPosX, testimonyPosY)
        screen.blit(drawText, (textX, textY))
        drawImage(table, 0, SCREEN_HEIGHT/2)
        screen.blit(canvas, (screenX, screenY))
        drawDone()
        drawButtons()
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    # Save the drawing when exiting the drawing loop
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    latest_drawing = os.path.join("saved_drawings", f"drawing_{timestamp}.png")
    drawings.append(latest_drawing)
    
    # Create directory if it doesn't exist
    os.makedirs("saved_drawings", exist_ok=True)

    # Save the canvas as a PNG file
    pygame.image.save(canvas, latest_drawing)
    print(f"Drawing saved to {latest_drawing}")
    lastDrawing = pygame.image.load(latest_drawing)

    # Criminal comparison screen loop
    while isCriminal:
        screen.fill((0, 0, 0))
        screen.blit(mugshot, (0, 0))    
        culprit.build(0,0)
        culprit1.build(SCREEN_WIDTH/3, 0)
        culprit2.build(SCREEN_WIDTH/3*2, 0)
        

        
        screen.blit(lastDrawing, (screenX, screenY))
        drawDone()
        doCriminal()  # Show the criminal image for comparison
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isCriminal = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isCriminal = False  
                if event.key == pygame.K_p:
                    running = False
                    menu = False
                    pygame.quit()
                    sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_done.collidepoint(x, y):
                    isCriminal = False
        pygame.display.flip()

    # Update display
    pygame.display.flip()
    
    # Boss feedback scene animation - slide in from right
    bossPosX, bossPosY = SCREEN_WIDTH, 300
    for i in range(int(SCREEN_WIDTH*2/3/10)):
        bossPosX -= 10  # Move boss image left
        screen.fill((20, 20, 20))
        drawImage(boss, bossPosX, bossPosY)
        clock.tick(60)  # Limit to 60 FPS
        pygame.display.flip()

    # Display boss feedback text letter by letter
    text = "Nice Job "
    newtext = ""
    textX, textY = SCREEN_WIDTH/4, SCREEN_HEIGHT/3
    for i in text:
        newtext += i
        drawText = font.render(newtext, True, (255, 255, 255), (0, 0, 0))
        screen.blit(drawText, (textX, textY))
        time.sleep(randint(1, 10)/200)  # Random delay for typewriter effect
        pygame.display.flip()    

    # Draw done button for play again screen
    drawDone()
    pygame.display.flip()
    
    # Play again prompt loop
    while playAgain:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playAgain = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playAgain = False
                    running = False
                if event.key == pygame.K_p:
                    running = False
                    menu = False
                    pygame.quit()
                    sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_done.collidepoint(x, y):
                    playAgain = False

# Quit pygame when game is done
pygame.quit()