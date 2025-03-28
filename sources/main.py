#Drawn to Justice, par: Leo, Ioanis, Samuel, Simon et Yahya (Lycee jules Guesde, 1e -- prof de NSI: M.Even)
import pygame
from math import *
from random import *
import time
import os
from random import randint
import sys
from math import hypot

os.system("cls")  # Clear console screen
# Initialize pygame
pygame.init()
pygame.mixer.music.load("sources/music/suspense.mp3")
pygame.mixer.music.play(loops=-1)
font = pygame.font.Font(None, 36)

drawing = False
streak = 0
combo = 0
Space = 20

# Screen settings
overSize = 4  # Scaling factor for canvas relative to screen size
pygame.display.set_caption("Drawn To Justice!")
screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = 1920,1200
CANVAS_WIDTH, CANVAS_HEIGHT = 655,380
borderPatrol = ((10*SCREEN_HEIGHT)/100)  # Border padding
screenX, screenY = 1200, 565  # Canvas position

gallery_button = pygame.image.load("sources/ui/default/Levels.png")
gallerySurface = pygame.Surface((100,40))
gallery_button = pygame.transform.scale(gallery_button, (100,40))
gallerySurface.blit(gallery_button, (0, 0))  # Blit at (0,0)

button_color_black = pygame.image.load("sources/ui/default/buttons/color_black.png")
blackSurface = pygame.Surface((100,40))
button_color_black = pygame.transform.scale(button_color_black, (100,40))
blackSurface.blit(button_color_black, (0, 0))  # Blit at (0,0)

# White button surface
button_color_white = pygame.image.load("sources/ui/default/buttons/color_white.png")
whiteSurface = pygame.Surface((100,40))
button_color_white = pygame.transform.scale(button_color_white, (100,40))
whiteSurface.blit(button_color_white, (0, 0))  # Blit at (0,0)

# Size up button surface
button_size_up = pygame.image.load("sources/ui/default/buttons/size_plus.png")
upSurface = pygame.Surface((100,40))
button_size_up = pygame.transform.scale(button_size_up, (100,40))
upSurface.blit(button_size_up, (0, 0))  # Blit at (0,0)

# Size down button surface
button_size_down = pygame.image.load("sources/ui/default/buttons/size_minus.png")
downSurface = pygame.Surface((100,40))
button_size_down = pygame.transform.scale(button_size_down, (100,40))
downSurface.blit(button_size_down, (0, 0))  # Blit at (0,0)

# Done button surface
button_done = pygame.image.load("sources/ui/default/buttons/done.png")
doneSurface = pygame.Surface((100,40))
button_done = pygame.transform.scale(button_done,(100,40))
doneSurface.blit(button_done, (0, 0))  # Blit at (0,0)


screen.fill((0, 0, 0))  # Clear screen
loading_text = font.render("Loading...", True, (255, 255, 255))
screen.blit(loading_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
pygame.display.update()  # Refresh the screen
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
def load_animation(folder_path):
    files = os.listdir(folder_path)
    AnimationSurfaces = []
    for i in files:
        image = pygame.image.load(os.path.join(folder_path, i))
        image = pygame.transform.scale(image, (600, 900))
        imageSurface = pygame.Surface((600,900), pygame.SRCALPHA)
        imageSurface.blit(image,(0,0))
        AnimationSurfaces.append(imageSurface)
        print(f"Loaded {i}")
    return AnimationSurfaces


# Load game images
menu_screen = pygame.image.load("sources/images/menu_screen.png")
menu_screen = pygame.transform.scale(menu_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))


icon = pygame.image.load("sources/images/icon.png")
pygame.display.set_icon(icon)

testimony = load_random_image("sources/images/testimonials")  # Random testimony image
boss = load_random_image("sources/images/boss")  # Random boss image
criminal = load_random_image("sources/images/criminals")  # Random criminal image

end = pygame.image.load("sources/ui/default/Exit.png")
end = pygame.transform.scale(end, (200, 120))
endSurface = pygame.Surface((200,120))
endSurface.blit(end, (0, 0))
# Load and scale background image
background = pygame.image.load("sources/images/background.png")
background = pygame.transform.scale(background, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT )))
# Load and scale mugshot image
mugshot = pygame.image.load("sources/images/mugshot.jpg")
mugshot = pygame.transform.scale(mugshot, (SCREEN_WIDTH, SCREEN_HEIGHT))

text_bubble = pygame.image.load("sources/images/text_bubble.png")
text_bubble = pygame.transform.scale(text_bubble, (SCREEN_WIDTH, SCREEN_HEIGHT/2.1))

empty = pygame.image.load("sources/images/empty.png")
# Load and scale table image
table = pygame.image.load("sources/images/table.png")
table = pygame.transform.scale(table, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (60,60,60)
LIGHT_GREY = (90,90,90)
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
    
    screen.blit(blackSurface,(screenX,screenY))
    screen.blit(whiteSurface,(screenX+100,screenY))
    screen.blit(upSurface,(screenX+200,screenY))
    screen.blit(downSurface,(screenX+300,screenY))
    screen.blit(doneSurface,(screenX+400,screenY))
    

  
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
animation = load_animation("sources/images/animation")
print(f"Loaded {len(animation)}/31 animation frames")

class person:
    alle = []
    
    def __init__(self,face,hair,mouth,eyes,ears,nose,name,arms,eyebrows,pants,accessories,scar,tattoo,tshirt):
        self.scar = scar
        self.tattoo = tattoo
        self.tshirt = tshirt # get all stuff
        self.pants = pants
        self.accessories = accessories
        self.face = face
        self.arms = arms
        self.eyebrows = eyebrows
        self.face = face
        self.hair = hair
        self.mouth = mouth 
        self.eyes = eyes
        self.ears = ears 
        self.name = name 
        self.nose = nose
        self.surface = None  # Store pre-built sprite
        screen.fill((0, 0, 0))  # Clear screen
        loading_text = font.render("Loading...", True, (255, 255, 255))
        screen.blit(loading_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        pygame.display.update()  # Refresh the screen
        person.alle.append(self)

        # Load and scale assets once
        self.load_assets()

    def load_assets(self):
        """Loads and scales assets once to improve performance."""
        self.images = {
            "ears": pygame.image.load(f"sources/images/Civilians/ears/ears_{self.ears}.png").convert_alpha(),
            "face": pygame.image.load(f"sources/images/Civilians/face/face_{self.face}.png").convert_alpha(),
            "hair": pygame.image.load(f"sources/images/Civilians/hair/hair_{self.hair}.png").convert_alpha(),
            "nose": pygame.image.load(f"sources/images/Civilians/nose/nose_{self.nose}.png").convert_alpha(),
            "mouth": pygame.image.load(f"sources/images/Civilians/mouth/mouth_{self.mouth}.png").convert_alpha(),
            "eyes": pygame.image.load(f"sources/images/Civilians/eyes/eyes_{self.eyes}.png").convert_alpha(),
            "eyebrows": pygame.image.load(f"sources/images/Civilians/eyebrows/eyebrows_{self.eyebrows}.png").convert_alpha(),
            "pants": pygame.image.load(f"sources/images/Civilians/pants/pants_{self.pants}.png").convert_alpha(),
            "arms": pygame.image.load(f"sources/images/Civilians/arms/arms_{self.arms}.png").convert_alpha(),
            "tshirt": pygame.image.load(f"sources/images/Civilians/tshirt/tshirt_{self.tshirt}.png").convert_alpha(),
            "scar": pygame.image.load(f"sources/images/Civilians/scar/{self.scar}.png").convert_alpha(),
            "tattoo": pygame.image.load(f"sources/images/Civilians/tattoo/tattoo_{self.tattoo}.png").convert_alpha(),
            "accessories": pygame.image.load(f"sources/images/Civilians/accessories/accessories_{self.accessories}.png").convert_alpha(),
        }

        # Scale images once
        
   
        # Pre-render the character's surface
        self.render_character()

    def render_character(self):
        """Creates and stores the character's final surface."""
        self.surface = pygame.Surface((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw all parts
        for img in self.images.values():
            self.surface.blit(img, (-100, 0))

    def build(self, posX, posY, difficulty):
        """EFFICITENTY renders the character to the screen."""
        self.posX = posX
        self.posY = posY
        if difficulty > 4:
            difficulty = 4

        screen.blit(self.surface, (posX, posY))

        # Draw culprit text if needed debug / 
        '''
        if self in [culprit, culprit1]:
            label = "Culprit" if self == culprit else "Culprit 1"
            ct = font.render(label, True, (128, 0, 128))
            screen.blit(ct, (posX + 200, posY + 400))
        '''

    def genid(self):
        #Generer une id pour objet pour text etc
        id = {"face":self.face,"hair":self.hair,"eyes":self.eyes,"ears":self.ears,"mouth":self.mouth,"scar":self.scar,"eyebrows":self.eyebrows}
        return id
    def calculate_similarity(self,id2):
        id1 = self.genid()  
        id2 = id2.genid()
        matches = sum(1 for thing in id1 if id1[thing] == id2[thing])  # Count matching keys
        return (matches / 2) * 100 
    def clickGlow(self,difficulty):
        global selected_culprit
        if difficulty>4:
            difficulty = 4
        chr_rect = pygame.Rect(self.posX, self.posY, SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/6)
        mouse_pos = pygame.mouse.get_pos()
        if chr_rect.collidepoint(mouse_pos) and not button_d.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), chr_rect, 5)
            if  pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen, (255, 255, 0), chr_rect, 5)
                selected_culprit = self
                return selected_culprit

score = 0
def generate_wild_description(id_dict):
    """
    Gen a chaotic  somewhat coherent character description.
    includes  clutter and randomness.
    """
    
    # Face, eyes, mouth, and hair base descriptors
    face_desc = {
        "angry": [ "rage-filled", "volcanic","angry"],
        "sad": ["melancholy", "sad" , "mournful"],
        "normal_white": ["plain", "neutral", "calm"],
        "round_white": ["big", "fat", "plump", "round"]
    }
    
    eyes_desc = {
        "angry": ["mefiant","angry", "intense", "furious"],
        "sad": ["crying", "looking down", "melancholic","sad"],
        "normal": ["calm", "observant"]
    }
    eyebrows_desc = {
    # Angry expressions with color hints
    "angry_black": ["angry and dark", "dark and annoyed", "ink-black and menacing"],
    "angry_blond": ["golden and tensed", "sand-like and mefiant", "honey looking and fronced"],
    "angry_brown": ["chestnut dark and mefiant", "walnut fronced", "bronze annoyed", "earth-brown thunderous"],
    "angry_orange": ["orange and intense", "orange and piercing", "flame-like menacing", "amber and annoyed", "ginger and fronced"],
    
    # Sad expressions with color hints
    "sad_black": ["black worried", "ink-dark and sad", "obsidian dark and worried"],
    "sad_blond": ["blond and sad","honey-colored worried", "pale and crying"],
    "sad_brown": ["chestnut-like and sad", "bronze color and melancholic"],
    "sad_orange": ["copper subdued", "rust soft", "gentle ginger"],
    "normal_black": [ "dark straight", "normal and dark","steady dark"],
    "normal_blond": ["golden", "yellow colored"],
    "normal_brown": ["flat brown","muddy and normal","unexpressive brownish"],
    "normal_orange": ["unexpressive orange","normal orange","honey like"]
    }
    mouth_desc = {
        "up": ["smirking", "mocking", "amused", "playful"],
        "up_big": ["enormous", "joyful", "dumb-looking","crazy-big"],
        "down": ["frowning", "sad", "worried","downturned"]
    }
    
    hair_desc = {
        "bald": ["shiny", "reflective", "bare", "bald","egg-like","eggish"],
        "buzzcut": ["closely cut", "military-style", "closely shaved", "very very short", "buzzcut"],
        "short_pointy_black": ["spiky dark", "messy dark", "messy black"],
        "short_pointy_brown": ["wood-toned pointy", "brown messy"],
        "short_pointy_orange": ["flame-like", "orange and pointy", "electric orange"],
        "short_pointy_blond": ["golden and pointy", "bright and messy", "radiantly spiky"]
    }
    
    # Clutter phrases for randomness
    clutter_phrases = [
        "while he was criming",
        "thinking he was a racecar",
        "amongst theoretical background noise",
        "with a hiphop sound",
        "in a flash",
        "while I was eating",
        "at 9:31 and thirty-three seconds"
        
    ]
    
    # Verb modifiers
    verb_modifiers = [
         "mysteriously", "inexplicably", "coincidentally",
    ]
    withe = ["with"]
    wiwth = choice(withe)
    # Get character traits with fallback
    eyes = id_dict.get('eyes', 'normal')
    face_type = id_dict.get('face', 'normal_white')
    hair_type = id_dict.get('hair', 'bald')
    mouth = id_dict.get("mouth", 'neutral')
    scar = id_dict.get("scar","no scar")
    
    eyebrows = id_dict.get('eyebrows', 'normal_black')
    # Select descriptors
    selected_face = choice(face_desc.get(face_type, ["undefined"]))
    selected_eyes = choice(eyes_desc.get(eyes, ["undefined"]))
    selected_mouth = choice(mouth_desc.get(mouth, ["undefined"]))
    selected_hair = choice(hair_desc.get(hair_type, ["bizarre"]))
    selected_eyebrows = choice(eyebrows_desc.get(eyebrows, ["undefined"]))
    # Generate description
    description = (
        f"A {selected_face} guy {choice(verb_modifiers)} "
        f"with {selected_eyes} eyes, {selected_eyebrows} eyebrows, and a {selected_mouth} mouth, "
        f"{wiwth} {selected_hair} hair, {choice(clutter_phrases)}."
        f" He had {scar}"
    
    )
    
    return description

def create_gallery():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN)
    pygame.display.set_caption("Drawing Gallery")
    clock = pygame.time.Clock()

    # Load frame image
    frame = pygame.image.load("sources/images/frame.png")
    frame = pygame.transform.scale(frame, (800, 600))  # Adjust size as needed

    # Load saved drawings
    saved_drawings_path = "sources/saved_drawings"
    drawings = [os.path.join(saved_drawings_path, f) for f in os.listdir(saved_drawings_path) 
                if f.endswith('.png')]
    
    if not drawings:
        print("No drawings found in the gallery!")
        return True  # Return True to continue game loop

    # Current drawing index
    current_index = 0

    # Scrolling variables
    scroll_x = 0
    scroll_speed = 20
    
    # Correctly set done button rectangle to match blitted position
    done_button_rect = doneSurface.get_rect(topleft=(SCREEN_WIDTH-100, SCREEN_HEIGHT-100))

    # Gallery loop
    gallery_running = True
    while gallery_running:
        screen.fill((255, 255, 255))  # White background
        screen.blit(doneSurface, (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game completely
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    gallery_running = False  # Exit gallery, return to main game
                    return True
                    
                elif event.key == pygame.K_RIGHT:
                    # Move to next drawing
                    current_index = (current_index + 1) % len(drawings)
                    scroll_x = -screen.get_width()  # Start off-screen
                elif event.key == pygame.K_LEFT:
                    # Move to previous drawing
                    current_index = (current_index - 1) % len(drawings)
                    scroll_x = screen.get_width()  # Start off-screen
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if done_button_rect.collidepoint(pos):
                    gallery_running = False
                    return True

        # Load current drawing
        try:
            current_drawing = pygame.image.load(drawings[current_index])
            current_drawing = pygame.transform.scale(current_drawing, (600, 400))  # Adjust size to fit frame
        except:
            print(f"Error loading drawing: {drawings[current_index]}")
            continue

        # Smooth scrolling
        if scroll_x < 0:
            scroll_x += scroll_speed
        elif scroll_x > 0:
            scroll_x -= scroll_speed

        # Calculate drawing position
        draw_x = (screen.get_width() - current_drawing.get_width()) // 2 + scroll_x
        draw_y = (screen.get_height() - current_drawing.get_height()) // 2

        # Draw frame
        frame_x = draw_x - 100  # Adjust to center the drawing in the frame
        frame_y = draw_y - 100
        screen.blit(frame, (frame_x, frame_y))

        # Draw current drawing
        screen.blit(current_drawing, (draw_x, draw_y))

        # Draw gallery navigation text
        font = pygame.font.Font(None, 36)
        nav_text = font.render(f"Drawing {current_index + 1} of {len(drawings)}", True, (0, 0, 0))
        screen.blit(nav_text, (screen.get_width() // 2 - nav_text.get_width() // 2, 50))

        pygame.display.flip()
        clock.tick(60)
    
    return True
# If you want to use it directly with genid()

tshirt_options = ["white"]
tattoo_options = ["neck_left","none"]
scar_options = ["a scarred neck","no scar"]
accessories_options = ["earing","none"]
pants_options = ["blue","cyan","green","grey","red","yellow"]
face_options = ["normal_white","round_white"]
eyebrows_options = ["angry_black","angry_blond","angry_brown","sad_black","sad_blond","sad_brown"]
arms_options = ["white"]
hair_options = ["bald", "buzzcut", "short_pointy_black","short_pointy_blond","short_pointy_brown","short_pointy_orange"]
mouth_options = ["up_big","up","down"]
eyes_options = ["angry","sad"]
ears_options = ["normal_white","round_white"]
nose_options = ["big","normal"]
difficulty = 3

# Main game loop

while running:
    #Eviter lag en loadant tout avant le Menu, sur des surfaces puisque blitter des images sur une surface impacte perf. 
    person.alle = []
    selected_culprit = None
    culprit = person(
        choice(face_options), 
        choice(hair_options),
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Right Culprit",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )
    
    culprit_id  = culprit.genid()
    description = generate_wild_description(culprit_id)
    print(description)
    face_weights = [difficulty if face == culprit_id["face"] else 1 for face in face_options]
    hair_weights = [difficulty if hair == culprit_id["hair"] else 1 for hair in hair_options]
    face_weights1 = [difficulty-1 if face == culprit_id["face"] else 1 for face in face_options]
    hair_weights2 = [difficulty-1 if hair == culprit_id["hair"] else 1 for hair in hair_options]
    #print(f"culprit: {culprit_id}")
    culprits = []
    
    culprit1 = person(
        choices(face_options,(face_weights))[0],
        choices(hair_options,hair_weights)[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 1",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )
    
    culprit2 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 2",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )
    
    culprit3 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 3",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )

    culprit4 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 4",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )

    culprit5 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 5",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )

    culprit6 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 6",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )

    culprit7 = person(
        choices(face_options,(face_weights1))[0],
        choices(hair_options,(hair_weights2))[0],
        choice(mouth_options),
        choice(eyes_options),
        choice(ears_options),
        choice(nose_options),
        "Wrong Culprit 7",
        choice(arms_options),
        choice(eyebrows_options),
        choice(pants_options),
        choice(accessories_options),
        choice(scar_options),
        choice(tattoo_options),
        choice(tshirt_options)
        )

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
    
    font = pygame.font.Font(load_random_font("sources/fonts"), int(SCREEN_HEIGHT/20))
    a=0
    frame_counter=0
    animation_frame_delay = 5
    while menu:
        color += 0.01  # Increment color animation parameter
        frame_counter += 1
        if frame_counter >= animation_frame_delay:
            a = (a + 1) % len(animation)
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(menu_screen, (0, 0)) # Display game menu_screen
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
                
                   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                surf_rect = endSurface.get_rect(topleft = (100,100))
                pso = pygame.mouse.get_pos()
                if surf_rect.collidepoint(pso):
                    menu = False
                    running = False
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                running = False
                menu = False
        
        # Calculate color-cycling RGB values with sine waves
        x1 = int((sin(color) * 127.5) + 127.5)         # Red (0–255)
        y1 = int((sin(color + 2) * 127.5) + 127.5)     # Green (0–255)
        z1 = int((sin(color + 4) * 127.5) + 127.5)     # Blue (0–255)
        screen.blit(endSurface,(100,100))
        screen.blit(animation[a],(1150,450))
        pygame.display.flip()  # Update display

    # Testimony scene animation - slide in from right
    testimony = load_random_image("sources/images/testimonials")
    testimonyPosX, testimonyPosY = -testimony.get_width(), 0  # Start from far left
    animation_speed = 20  # Higher number = faster animation
    target_x = SCREEN_WIDTH / 3.3  # Target position
    font = pygame.font.Font(load_random_font("sources/fonts"), int(SCREEN_HEIGHT / 20))

    # Store the background if it doesn't change often
    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_surface.blit(background,(0,0))
    drawBackground()  # Ensure background is rendered into background_surface

    while testimonyPosX < target_x:
        # Update the position
        testimonyPosX = min(target_x, testimonyPosX + animation_speed)
        testimonyPosY = (SCREEN_HEIGHT / 2) * (0.03 * sin(testimonyPosX))

        # Clear the screen by blitting the background only once per frame
        screen.blit(background_surface, (0, 0))

        # Draw the moving testimony and static table images
        screen.blit(testimony, (testimonyPosX, testimonyPosY))
        screen.blit(table, (0, 0))

        # Update the display
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
        current_y = textY + (current_line_index * 60)
        
        for char in line:
            
            current_line_text += char
            
            drawText = font.render(current_line_text, True, (255, 255, 255), (0, 0, 0))
            screen.blit(drawText, (textX, current_y))
            
            if char==",":
                time.sleep(0.5)
            time.sleep(randint(1, 10)/200)
            pygame.display.flip()
        
        
        current_line_index += 1
    # Create canvas for drawing
    screen.blit(drawText, (textX, current_y))
    time.sleep(0.8)
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    # Draw initial canvas and UI
    drawBackground()
    screen.blit(testimony, (testimonyPosX, testimonyPosY))
    drawImage(table, 0, 0)
   
    drawButtons()
    pygame.display.flip()

    # Drawing interface loop
    thickness = 3
    last_thickness = thickness
    previous_pos = pygame.mouse.get_pos()
    deltaX, deltaY = 0, 0
    D = False
    #drawBackground()
    #drawImage(table, 0, 0)
    while drawing:
        current_pos = pygame.mouse.get_pos()
        deltaX, deltaY = pygame.mouse.get_rel()
        distance = hypot(deltaX, deltaY)
        thickness = max(3, distance * 0.29)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                drawing = False
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drawing = False  
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
                button_d = doneSurface.get_rect(topleft=(screenX+400, screenY))
                button_u = upSurface.get_rect(topleft=(screenX+200, screenY))
                button_s = downSurface.get_rect(topleft=(screenX+300, screenY))
                button_b = blackSurface.get_rect(topleft=(screenX, screenY))
                button_w = whiteSurface.get_rect(topleft=(screenX+100, screenY))
                if button_d.collidepoint(x, y):
                    drawing = False
                    isCriminal = True
                elif button_b.collidepoint(x, y):
                    brush_color = BLACK
                elif button_w.collidepoint(x, y):
                    brush_color = WHITE
                elif button_u.collidepoint(x, y):
                    last_thickness = min(50, last_thickness + 3)
                elif button_s.collidepoint(x, y):
                    last_thickness = max(2, last_thickness - 3)  

            elif event.type == pygame.MOUSEBUTTONUP:
                D = False

        # Drawing logic
        if pygame.mouse.get_pressed()[0]:  
            x, y = current_pos
            if screenX <= x <= screenX + CANVAS_WIDTH and screenY <= y <= screenY + CANVAS_HEIGHT and D:
                if distance > 0.1:
                    canvas_x1, canvas_y1 = previous_pos[0] - screenX, previous_pos[1] - screenY
                    canvas_x2, canvas_y2 = x - screenX, y - screenY

                    pygame.draw.line(canvas, brush_color, (canvas_x1, canvas_y1), (canvas_x2, canvas_y2), int(last_thickness))
                    previous_pos = (x, y)
                    last_thickness = last_thickness * 0.7 + thickness * 0.3

        # Optimized display update
       
        screen.blit(canvas, (screenX, screenY))
       

        drawButtons()
        pygame.display.update((screenX, screenY, CANVAS_WIDTH, CANVAS_HEIGHT))
        #pygame.display.update()
        clock.tick(60)


    # Save the drawing when exiting the drawing loop
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    latest_drawing = os.path.join("sources\saved_drawings", f"drawing_{timestamp}.png")
    drawings.append(latest_drawing)
    
    # Create directory if it doesn't exist
    os.makedirs("sources\saved_drawings", exist_ok=True)

    # Save the canvas as a PNG file
    pygame.image.save(canvas, latest_drawing)
    print(f"Drawing saved to {latest_drawing}")
    lastDrawing = pygame.image.load(latest_drawing)
    lastDrawing = pygame.transform.scale(lastDrawing, (300, 300))
    selected_culprit = None
    # Criminal comparison screen loop
    

    while isCriminal:
        screen.fill((0, 0, 0))
        screen.blit(mugshot, (0, 0)) 
        
        for i,p in enumerate(culprits):
            p.build(((i%4) * (SCREEN_WIDTH / 4)),(i//4)*(SCREEN_HEIGHT/2),difficulty)
            p.render_character()
        
        for i,p in enumerate(culprits):
            p.clickGlow(difficulty)
       
        
      
        #culprit.build(0,0)
        #culprit1.build(SCREEN_WIDTH/3, 0)
        #culprit2.build(SCREEN_WIDTH/3*2, 0)
        

        
        screen.blit(lastDrawing, (screenX+400, screenY))
        

        if not selected_culprit == None:
            playAgain =True
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
                if button_d.collidepoint(x, y) and not selected_culprit == None:
                    isCriminal = False
        pygame.display.flip()

    # Update display
    pygame.display.flip()
    
    # Boss feedback scene animation - slide in from right
    

    bossPosX, bossPosY = SCREEN_WIDTH, SCREEN_HEIGHT/3  # Fixed vertical starting position

    for i in range(int(SCREEN_WIDTH*2/20)):
        bossPosX -= 10  # Move boss image left
        bossPosY = SCREEN_HEIGHT/3 + sin(bossPosX*0.1)*10  # Subtle vertical oscillation
        screen.fill((20, 20, 20))

        drawImage(boss, bossPosX, bossPosY)
        clock.tick(60)  # Limit to 60 FPS
        pygame.display.flip()
        # Display boss feedback text letter by letter
    
    if selected_culprit == culprit:
        streak += 1
        combo += 1
        score = streak*(combo)
        text = f"Nice Job, you chose the {culprit.name}"
        scr =  f"Your score is {score}"

    else: 
        streak = 0
        score = score + streak*(combo)
        text = f"Are you dumb or what, you chose the wrong guy: {selected_culprit.name}."
        scr =  f"Your score is {score}"
    clt = "The criminal was:"
    cl = font.render(clt,True,(255,255,255))
    screen.blit(cl, (SCREEN_WIDTH-1000,SCREEN_HEIGHT-800))
    culprit.build(SCREEN_WIDTH-800,SCREEN_HEIGHT-600,difficulty)
    newtext = ""
    newtext2 = ""
    textX, textY = SCREEN_WIDTH/7, SCREEN_HEIGHT/6
    textX2,textY2 = textX, textY+50
    for p,i in enumerate(text):
        newtext += i
        drawText = font.render(newtext, True, (255,255,255))
        screen.blit(drawText, (textX, textY))
        time.sleep(randint(1, 10)/200)  # Random delay for typewriter effect
        pygame.display.flip()   
    for n in scr:
        newtext2 += n
        drawText2 = font.render(newtext2, True, (255,255,255))
        screen.blit(drawText2, (textX2, textY2))
        screen.blit(drawText,(textX,textY))
        time.sleep(randint(1, 10)/200)  # Random delay for typewriter effect
        pygame.display.flip()   
    # Draw done button for play again screen
    
    screen.blit(gallery_button,(SCREEN_WIDTH/2,SCREEN_HEIGHT/1.2))
    screen.blit(doneSurface,  (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
    pygame.display.flip()
    
    # Play again prompt loop
    while playAgain:
        button_d = doneSurface.get_rect(topleft=(SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
        button_g = gallerySurface.get_rect(topleft=(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2))
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
                if button_d.collidepoint(x, y):
                    playAgain = False
                elif button_g.collidepoint(x, y):
                    create_gallery()

    #screen.blit(button_done,(SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
    relX=0
    
    
    screen.fill((0,0,0))

    drawing = True  # Reset drawing mode state
    isCriminal = True  # Reset criminal comparison state
    bossSpeech = True  # Reset boss feedback state
    playAgain = True  # Reset play again state
    menu = False  # Ensure menu is not reset to True
    selected_culprit = None  # Explicitly reset selected culprit
    culprits = []  # Clear the culprits list
    difficulty += 1
# Quit pygame when game is done
pygame.quit()