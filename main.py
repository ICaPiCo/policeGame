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
screenX, screenY = (((3*SCREEN_WIDTH)/overSize)-90)-borderPatrol, (((3*SCREEN_HEIGHT)/overSize)-130)-borderPatrol  # Canvas position


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
background = pygame.image.load("images/background.png")
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
def dict_to_text(dictionary):
    """Convert a dictionary to a formatted text string."""
    text = ""
    for key, value in dictionary.items():
        text += f"{key}: {value}\n"
    return text.strip()
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
    alle = []
    def __init__(self,mood,hair,name):
        self.mood = mood
        self.hair = hair
        self.name = name
        person.alle.append(self)
    def build(self,posX,posY,difficulty):
        base = pygame.image.load("images/creation/basic guy.png")
        image = pygame.image.load(f"images/creation/face_{self.mood}.png")
        hair = pygame.image.load(f"images/creation/hair_{self.hair}.png")
        if difficulty>4:
            difficulty = 4
        base = pygame.transform.scale(base, (SCREEN_WIDTH/difficulty-1,3* SCREEN_HEIGHT/6))
        image = pygame.transform.scale(image, (SCREEN_WIDTH/difficulty-1,3* SCREEN_HEIGHT/6))
        hair = pygame.transform.scale(hair, (SCREEN_WIDTH/difficulty-1, 3*SCREEN_HEIGHT/6))
        surface = pygame.Surface((SCREEN_WIDTH/3, SCREEN_HEIGHT))
        surface.fill((255,255,255))
        surface.blit(mugshot,(0,0))
        surface.blit(base, (0, 0))
        surface.blit(image, (0, 0))
        surface.blit(hair, (0, 0))
        if self == culprit:
            ct = font.render("Culprit",True,(128,0,128))
            surface.blit(ct, (200, 400))
        elif self == culprit1:
            ct = font.render("Culprit 1", True, (128, 0, 128))
            surface.blit(ct, (200, 400))
        self.posX = posX
        self.posY = posY
        screen.blit(surface, (posX, posY))
    def genid(self):
        id = {"face":self.mood,"hair":self.hair}
        return id
    def calculate_similarity(self,id2):
        id1 = self.genid()  
        id2 = id2.genid()
        matches = sum(1 for thing in id1 if id1[thing] == id2[thing])  # Count matching keys
        return (matches / 2) * 100 
    def genText(self,id):
        text = f"Face: {id['face']}, Hair: {id['hair']}"
        return text
    def clickGlow(self,difficulty):
        global selected_culprit
        if difficulty>4:
            difficulty = 4
        chr_rect = pygame.Rect(self.posX, self.posY, SCREEN_WIDTH/difficulty, 3*SCREEN_HEIGHT/6)
        mouse_pos = pygame.mouse.get_pos()
        if chr_rect.collidepoint(mouse_pos) and not button_done.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), chr_rect, 5)
            if  pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, (255, 255, 0), chr_rect, 5)
                selected_culprit = self
                return selected_culprit
                
mood_options = ["angry", "happy","dumb","sunglasses"]
hair_options = ["fluffy", "spicky", "pea","judge"]
difficulty = 3
# Main game loop
while running:
    
    person.alle = []
    selected_culprit = None
    culprit = person(choice(mood_options), choice(hair_options),"badguy")
    culprit_id  = culprit.genid()
    mood_weights = [difficulty if mood == culprit_id["face"] else 1 for mood in mood_options]
    hair_weights = [difficulty if hair == culprit_id["hair"] else 1 for hair in hair_options]
    mood_weights1 = [difficulty-1 if mood == culprit_id["face"] else 1 for mood in mood_options]
    hair_weights2 = [difficulty-1 if hair == culprit_id["hair"] else 1 for hair in hair_options]
    #print(f"culprit: {culprit_id}")
    culprits = []
    
    culprit1 = person(choices(mood_options,(mood_weights))[0], choices(hair_options,hair_weights)[0],"littlebad")
    culprit2 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"notsobad")
    culprit3 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"VERYBADCHOICE")
    culprit4 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"VERYVERYBADCHOICE")
    culprit5 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"Culprit5")
    culprit6 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"Culprit6")
    culprit7 = person(choices(mood_options,(mood_weights1))[0],  choices(hair_options,(hair_weights2))[0],"Culprit7")
    available = [culprit,culprit1,culprit2,culprit3,culprit4,culprit5,culprit6,culprit7]
    for i in range(difficulty):
        if i<len(available):
            culprits.append(available[i])
        else:
            break
    
    #a = culprit1.genid()
    #b = culprit2.genid()
    shuffle(culprits)
    #print(f"Are culprit2 and 3 similar?: {a},{b}<=>{culprit_id}")
    #print(f"{culprit1.calculate_similarity(culprit)}, {culprit2.calculate_similarity(culprit)}")
    # Start menu loop
    
    while menu:
        color += 0.01  # Increment color animation parameter
        screen.fill((0, 0, 0))  # Clear screen
        
        # Create color-cycling "Press space to start" text
        menu_text = font.render("Press space to start", True, (x1, y1, z1))
        screen.blit(menu_text, (SCREEN_WIDTH/2-200, (SCREEN_HEIGHT/2)+250))
        
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
    animation_speed = 40  # Higher number = faster animation
    target_x = SCREEN_WIDTH / 3  # Target position

    while testimonyPosX > target_x:
        testimonyPosX = max(target_x, testimonyPosX - animation_speed)
        drawBackground()
        drawImage(testimony, testimonyPosX, testimonyPosY)
        drawImage(table, 0, 0)
        pygame.display.flip()
        clock.tick(60)  
  

    text = "\n".join([f"{key}: {value}" for key, value in culprit_id.items()])
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
    thickness = 3
    last_thickness = thickness
    previous_pos = pygame.mouse.get_pos()
    deltaX, deltaY = 0, 0
    D = False
    while drawing:
        current_pos = pygame.mouse.get_pos()
        deltaX, deltaY = pygame.mouse.get_rel()
        distance = sqrt(deltaX**2 + deltaY**2)
        thickness = max(3, distance * 0.29) 
        


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
                if event.key == pygame.K_SPACE:
                    canvas.fill(WHITE)
            elif event.type == pygame.MOUSEBUTTONDOWN:

                D = True
                x, y = event.pos
                previous_pos = current_pos
        
                if button_done.collidepoint(x, y):
                    drawing = False
                    
                elif button_color_black.collidepoint(x, y):
                    brush_color = BLACK
                elif button_color_white.collidepoint(x, y):
                    brush_color = WHITE
                elif button_size_up.collidepoint(x, y):
                    last_thickness = min(30, last_thickness + 1)  # Increase brush size with upper limit
                elif button_size_down.collidepoint(x, y):
                    last_thickness = max(2, brush_size - 1)  # Decrease brush size with lower limit
            elif event.type ==pygame.MOUSEBUTTONUP:
                D = False
                

                
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                x, y = event.pos
                
                if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT and D:
                    if distance > 0.1:
                        # Convert screen coordinates to canvas coordinates
                        canvas_x1, canvas_y1 = previous_pos[0] - screenX, previous_pos[1] - screenY
                        canvas_x2, canvas_y2 = x - screenX, y - screenY
            
            # Draw on the canvas with canvas coordinates
                        pygame.draw.line(canvas, brush_color, (canvas_x1, canvas_y1), (canvas_x2, canvas_y2), int(last_thickness))
                        previous_pos = (x, y)
                        last_thickness = last_thickness * 0.7 + thickness * 0.3
                      
        
        
        # Redraw the scene each frame
        drawBackground()
        txt = font.render(str(current_pos),True,(255,255,255))
        
        screen.blit(drawText, (textX, textY))
        
        screen.blit(canvas, (screenX, screenY))
        screen.blit(txt, (0, 0))
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
        selected_culprit = None
        for i,p in enumerate(culprits):

            p.build(((i%4) * (SCREEN_WIDTH / 4)),(i//4)*(SCREEN_HEIGHT/2),difficulty)

        for i,p in enumerate(culprits):
            p.clickGlow(difficulty)
       
        
        '''
        culprit.build(0,0)
        culprit1.build(SCREEN_WIDTH/3, 0)
        culprit2.build(SCREEN_WIDTH/3*2, 0)
        
'''
        
        screen.blit(lastDrawing, (screenX, screenY))
        drawDone()
        if not selected_culprit ==None:
            break
        #doCriminal()  # Show the criminal image for comparison
        

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
                if button_done.collidepoint(x, y) and not selected_culprit == None:
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
    text = f"Nice Job, you chose: {selected_culprit.name} "
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

    drawing = True  # Drawing mode state
    isCriminal = True  # Criminal comparison state
    bossSpeech = True  # Boss feedback state
    playAgain = True  # Play again prompt state
    difficulty +=1
# Quit pygame when game is done
pygame.quit()