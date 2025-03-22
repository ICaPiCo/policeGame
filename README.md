# Interactive Portrait Drawing Game with Criminal Investigation Theme

This Pygame-based application provides an engaging drawing experience where users create portraits based on witness testimonies and participate in a criminal investigation narrative. The game combines creative drawing mechanics with an immersive storyline featuring animated characters and dynamic visual effects.

The application features a sophisticated drawing system with adjustable brush settings, parallax background effects, and a complete game flow from menu to final evaluation. Users progress through different stages including witness testimony, portrait creation, criminal identification, and boss evaluation, making it both an artistic tool and an entertaining game experience.

## Repository Structure
```
.
├── main.py                 # Main game entry point with core game loop and state management
├── oldWithParallax/        # Legacy version of drawing system with parallax effects
│   └── drawing.py         # Original implementation of drawing mechanics
├── SAMUEL TEST STOP PUTTING THINGS EVERYWHERE!!!!/ # Development test directory
│   ├── drawing.py         # Drawing system implementation with UI and animations
│   ├── Intro to classes.py # Class definitions for game items and weapons
│   ├── test2class.py      # Drawing canvas implementation with thickness controls
│   └── tests.py           # Testing implementation of drawing and animation features
└── resumeProjet.txt       # Project documentation and notes
```

## Usage Instructions
### Prerequisites
- Python 3.x
- Pygame library
- Operating system with graphical interface support
- Minimum screen resolution: 1920x1200

To install required packages:
```bash
pip install pygame
```

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Ensure required image directories exist:
```bash
mkdir -p images/testimonials images/boss images/criminals saved_drawings
```

3. Run the application:
```bash
python main.py
```

### Quick Start
1. Launch the game by running `main.py`
2. Press Space at the title screen to begin
3. Watch the testimony animation
4. Use the drawing canvas to create a portrait:
   - Left mouse button to draw
   - Use UI buttons to change colors (black/white)
   - Adjust brush size with +/- buttons
5. Click the green "Done" button when finished
6. View your drawing in the criminal lineup
7. Receive feedback from the boss character

### More Detailed Examples
Drawing System Features:
```python
# Change brush color
button_color_black = pygame.Rect(650, 100, 100, 40)  # Black color
button_color_white = pygame.Rect(650, 160, 100, 40)  # White color

# Adjust brush size
brush_size = min(20, brush_size + 2)  # Increase size
brush_size = max(2, brush_size - 2)    # Decrease size
```

### Troubleshooting
Common Issues:
1. Missing Image Files
   - Error: "Error: The directory 'images/testimonials' does not exist!"
   - Solution: Create required directories and populate with image files
   ```bash
   mkdir -p images/testimonials images/boss images/criminals
   ```

2. Display Resolution Issues
   - Error: Screen size mismatch
   - Solution: Adjust screen resolution or modify SCREEN_WIDTH/SCREEN_HEIGHT in main.py

3. Performance Issues
   - Enable debug information by uncommenting debug text renders
   - Monitor frame rate using the built-in clock
   - Default target: 60 FPS

## Data Flow
The application processes user input through multiple stages, from menu interaction to drawing creation and final evaluation.

```ascii
[Menu Screen] -> [Testimony] -> [Drawing Canvas] -> [Save Drawing] -> [Criminal Display] -> [Boss Evaluation]
     |              |               |                      |                |                  |
     v              v               v                      v                v                  v
User Input -> Animation -> Drawing Input -> File Storage -> Image Display -> Final Animation
```

Component Interactions:
1. Menu system manages game state transitions
2. Drawing canvas captures and processes mouse input
3. Image loading system handles random selection from directories
4. File system manages drawing storage and retrieval
5. Animation system coordinates character and UI movements
6. Event system handles user input and state changes
7. Rendering system manages layered display of game elements