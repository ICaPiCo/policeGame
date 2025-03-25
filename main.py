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
streak = 0
combo = 0
Space = 20
# Screen settings
overSize = 4  # Scaling factor for canvas relative to screen size
pygame.display.set_caption("Drawn To Justice")
screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
CANVAS_WIDTH, CANVAS_HEIGHT = SCREEN_WIDTH/overSize, SCREEN_HEIGHT/overSize
CANVAS_WIDTH, CANVAS_HEIGHT = CANVAS_WIDTH*1.35,CANVAS_HEIGHT*1.25
borderPatrol = ((10*SCREEN_HEIGHT)/100)  # Border padding
screenX, screenY = (((3*SCREEN_WIDTH)/overSize)-95)-borderPatrol, (((3*SCREEN_HEIGHT)/overSize)-175)-borderPatrol  # Canvas position
button_color_black = pygame.Rect((screenX+Space), (screenY+10), 100, 40)  # Black color button
button_color_white_outline = pygame.Rect(screenX+100+Space, (screenY+10), 100, 40)  # White color button outline
button_color_white = pygame.Rect(screenX+100+Space+5, screenY+10+5, 90, 30)  # White color button inner part
button_size_up = pygame.Rect(screenX+200+Space, screenY+10, 100, 40)  # Increase brush size button
button_size_down = pygame.Rect(screenX+300+Space, screenY+10, 100, 40)  # Decrease brush size button
button_done = pygame.Rect(screenX+400+Space, screenY+350, 100, 40)
def load_random_font(folder_path):
    """
    Load a random font from the specified folder.

    Args:
        folder_path (str): Path to the folder containing fonts

    Returns:
        Font: Randomly selected font, or None if failed
    """
    fonts = [f for f in os.listdir(folder_path)]
    random_font = choice(fonts)
    return (os.path.join(folder_path, random_font))

def load_random_image(folder_path):
    """
    Load a random image from the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing images
        
    Returns:
        Surface: Randomly selected image as pygame Surface, or None if failed
    """    
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
background = pygame.transform.scale(background, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT )))
# Load and scale mugshot image
mugshot = pygame.image.load("images/mugshot.jpg")
mugshot = pygame.transform.scale(mugshot, (SCREEN_WIDTH, SCREEN_HEIGHT))

speech_bubble = pygame.image.load("images/speech_bubble.png")
speech_bubble = pygame.transform.scale(speech_bubble, (SCREEN_WIDTH, SCREEN_HEIGHT/20))

empty = pygame.image.load("images/empty.png")
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
  # Done/Continue button


def drawBackground():
    """Draw the background image to the screen."""
   
    screen.blit(background, (0,0))

def drawImage(image, positionX, positionY,layer):
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
    

    screen.blit(font.render("+", True, WHITE), (screenX+200+(Space*3) , screenY+10 ))
    screen.blit(font.render("-", True, WHITE), (screenX+300+(Space*3) , screenY+10 ))
    

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
        base = pygame.transform.scale(base, (SCREEN_WIDTH/4-1,3* SCREEN_HEIGHT/6))
        image = pygame.transform.scale(image, (SCREEN_WIDTH/4-1,3* SCREEN_HEIGHT/6))
        hair = pygame.transform.scale(hair, (SCREEN_WIDTH/4-1, 3*SCREEN_HEIGHT/6))
        surface = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT/2))
        surface.blit(empty,(0,0))
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
        text = "Face: ",id['face'],", Hair: ",id['hair']
        return text
    def clickGlow(self,difficulty):
        global selected_culprit
        if difficulty>4:
            difficulty = 4
        chr_rect = pygame.Rect(self.posX, self.posY, SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/6)
        mouse_pos = pygame.mouse.get_pos()
        if chr_rect.collidepoint(mouse_pos) and not button_done.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), chr_rect, 5)
            if  pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, (255, 255, 0), chr_rect, 5)
                selected_culprit = self
                return selected_culprit

def generate_wild_description(id_dict):
    """
    Generate a chaotic yet somewhat coherent character description.
    Includes intentional clutter and randomness.
    """
  

    # Mood and hair base descriptors
    mood_desc = {
        "angry": ["fiery", "seething", "rage-filled", "volcanic"],
        "happy": ["jubilant", "beaming", "sunshine-infused", "grinning"],
        "dumb": ["bewildered", "perplexed", "mind-foggy", "slightly derailed"],
        "sunglasses": ["cool", "shadowy", "mysteriously smooth", "enigmatic"]
    }

    hair_desc = {
        "fluffy": ["cloud-like", "cotton-candy", "puffball", "marshmallow"],
        "spicky": ["razor-edged", "electric", "lightning-struck", "geometric"],
        "pea": ["rounded", "spherical", "vegetable-inspired", "carrot-like"],
        "judge": ["precise", "authoritative", "wigged", "structured"]
    }

    # Clutter phrases to add randomness
    clutter_phrases = [
        "while juggling invisible unicorns",
        "under a microscope of paradox",
        "during a quantum hiccup",
        "amidst theoretical background noise",
        "navigating bureaucratic daydreams",
        "with a soundtrack of static",
        "in a dimension of mild confusion",
        "tracing probability shadows",
        "at 9:31 and thirty three seconds"
    ]

    # Verb modifiers
    verb_modifiers = [
        "awkwardly", "mysteriously", "accidentally", "theoretically",
        "hypothetically", "inexplicably", "coincidentally","quaquaversally"
    ]

    # Obtain mood and hair, with fallback
    mood = id_dict.get('face', choice(list(mood_desc.keys())))
    hair = id_dict.get('hair', choice(list(hair_desc.keys())))

    # Randomly select descriptors
    selected_mood = choice(mood_desc.get(mood, ["undefined"]))
    selected_hair = choice(hair_desc.get(hair, ["bizarre"]))

    # Generate wild description
    description = [
        f"a {selected_mood} character {choice(verb_modifiers)} "
        f"sporting {selected_hair} hair, "
        f"{choice(clutter_phrases)}"
    ]
    shuffle(description)
    return description

# Demonstration function


# If you want to use it directly with genid()

mood_options = ["angry", "happy","dumb","sunglasses"]
hair_options = ["fluffy", "spicky", "pea","judge"]
difficulty = 3

# Main game loop
while running:
    
    person.alle = []
    selected_culprit = None
    culprit = person(choice(mood_options), choice(hair_options),"badguy")
    culprit_id  = culprit.genid()
    description = generate_wild_description(culprit_id)
    print(description)
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
    
    font = pygame.font.Font(load_random_font("fonts"), int(SCREEN_HEIGHT/20))

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
    animation_speed = 40 # Higher number = faster animation
    target_x = SCREEN_WIDTH / 3  # Target position
    font = pygame.font.Font(load_random_font("fonts"), int(SCREEN_HEIGHT/20))

    while testimonyPosX > target_x:
        testimonyPosX = max(target_x, testimonyPosX - animation_speed)
        testimonyPosY =(SCREEN_HEIGHT/2)*(0.06*sin(testimonyPosX))
        drawBackground()
        drawImage(testimony, testimonyPosX, testimonyPosY,1)
        drawImage(table, 0, 0,2)
        pygame.display.flip()
        clock.tick(60)  
        
  
    text = f"I saw {description}"
    line_length = 30  # Number of characters per line
    textX, textY = SCREEN_WIDTH/4, SCREEN_HEIGHT/3

    # Break text into lines of specified length
    lines = [text[i:i+line_length] for i in range(0, len(text), line_length)]
    
    # Variable to track current line being typed
    current_line_index = 0
    current_line_text = ""

    for line in lines:
        # Reset current line text and position for each line
        current_line_text = ""
        current_y = textY + (current_line_index * 50)
        
        for char in line:
            # Add next character to current line
            current_line_text += char
            
            # Render current line text
            drawText = font.render(current_line_text, True, (255, 255, 255), (0, 0, 0))
            screen.blit(drawText, (textX, current_y))
            
            # Random typewriter-like delay
            time.sleep(randint(1, 10)/200)
            pygame.display.flip()
        
        
        current_line_index += 1
    # Create canvas for drawing
    time.sleep(0.5)
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    # Draw initial canvas and UI
    drawBackground()
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
        
        
        #((my / SCREEN_HEIGHT) - 0.5) * 0.05*SCREEN_HEIGHT*layer


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
        drawImage(testimony, testimonyPosX, testimonyPosY,1)
        drawImage(table, 0, 0,2)
        mx,my = pygame.mouse.get_pos()
        
        canvasX = screenX + int((-((mx / SCREEN_WIDTH) - 0.5) * 0.05*SCREEN_WIDTH*2))
        canvasY = screenY + int((-((my / SCREEN_HEIGHT) - 0.5) * 0.05*SCREEN_HEIGHT*2))
        screen.blit(canvas, (screenX, screenY))
       
        #txt = font.render(str(current_pos),True,(255,255,255))
        #screen.blit(drawText, (textX, textY))
        #screen.blit(canvas, (screenX, screenY))
        
        #screen.blit(txt, (0, 0))
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
        if not selected_culprit == None:
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
        drawImage(boss, bossPosX, bossPosY,1)
        clock.tick(60)  # Limit to 60 FPS
        pygame.display.flip()

    # Display boss feedback text letter by letter
    print(selected_culprit.name)
    if selected_culprit.name == "badguy":
        streak += 1
        combo += 1
        score = streak*(combo)
        text = f"Nice Job, you chose the right culprit and you have a score of: {score}"
    else: 
        combo = 0
        score = streak*(combo)
        text = f"Are you dumb or what, you chose the wrong guy: {selected_culprit.name} and thus have a score of: {score}"
    
    

    newtext = ""
    textX, textY = SCREEN_WIDTH/6, SCREEN_HEIGHT/4
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

'''
CHEKLIST TO DO ULTRA IMPORTANT BEFORE TOMORROW:
- MAKE A BEAUTIFUL MENU - Ioanis 
- ADD MUSI AND SOUND EFFECTS- ADD SPEECH BUBBLE - Ioanis
- ADD ANIMATIONS (WALKING CHARACTERS) -Samuel
- MAKE BUTTONS MORE BEAUTIFUL (UI) -Ioanis
- PAUSE MENU ? - AAAAAAAAAAAAAh
- STORY - EVERYBODY
- CATCH LINES TESTIMONIES -TEXT GEN - Samuel
- PUT ALL OF LEO'S IMAGES - Leo /Ioanis

'''